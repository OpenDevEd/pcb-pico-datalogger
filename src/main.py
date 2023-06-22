#-----------------------------------------------------------------------------
# Basic data-collection program. This program will
#
#   - initialize hardware
#   - update RTCs (time-server->) external-RTC -> internal-RTC
#   - collect data
#   - update the display
#   - save data
#   - set next wakeup alarm
#   - turn power off
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

import gc
import time
import board
import alarm
import os
import builtins

from digitalio import DigitalInOut, Direction, Pull

# import for SD-card
import storage
import adafruit_sdcard

# imports for i2c and rtc
import busio
from rtc_ext.pcf8523 import ExtPCF8523 as ExtRTC

# imports for the display
import displayio
import adafruit_display_text, adafruit_display_shapes, adafruit_bitmap_font
import InkyPack

from dataviews.DisplayFactory import DisplayFactory
from dataviews.Base import Color, Justify
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# --- early configuration of the log-destination   ---------------------------

try:
  from log_config import g_logger
except:
  from log_writer import Logger
  g_logger = Logger('console')

# --- default configuration is in config.py on the pico.
#     You can override it also with a config.py on the sd-card   -------------

class Settings:
  def import_config(self):
    """ import config-module and make variables attributes """
    import config
    for var in dir(config):
      if var[0] != '_':
        g_logger.print(f"{var}={getattr(config,var)}")
        setattr(self,var,getattr(config,var))
    config = None
    gc.collect()

g_config = Settings()
g_config.import_config()

# --- pin-constants (don't change unless you know what you are doing)   ------

PIN_DONE = board.GP4   # connect to 74HC74 CLK
PIN_SDA  = board.GP2   # connect to sensors and RTC via I2C interface
PIN_SCL  = board.GP3   # connect to sensors and RTC via I2C interface

# SD-card interface (SPI)
PIN_SD_CS   = board.GP22
PIN_SD_SCK  = board.GP18
PIN_SD_MOSI = board.GP19
PIN_SD_MISO = board.GP16

# display interface (SPI, Inky-Pack)
PIN_INKY_CS   = board.GP17
PIN_INKY_RST  = board.GP21
PIN_INKY_DC   = board.GP20
PIN_INKY_BUSY = board.GP26

# --- main application class   -----------------------------------------------

class DataCollector():
  """ main application class """

  # --- hardware-setup   -----------------------------------------------------

  def setup(self):
    """ create hardware-objects """

    # early setup of SD-card (in case we send debug-logs to sd-card)
    if g_config.HAVE_SD:
      self._spi = busio.SPI(PIN_SD_SCK,PIN_SD_MOSI,PIN_SD_MISO)
      self.sd_cs = DigitalInOut(PIN_SD_CS)
      sdcard     = adafruit_sdcard.SDCard(self._spi,self.sd_cs)
      self.vfs   = storage.VfsFat(sdcard)
      storage.mount(self.vfs, "/sd")
      try:
        import sys
        sys.path.insert(0,"/sd")
        g_config.import_config()
        sys.path.pop(0)
      except:
        g_logger.print("no configuration found in /sd/config.py")

    # Initialse i2c bus for use by sensors and RTC
    i2c = busio.I2C(PIN_SCL,PIN_SDA)

    # If our custom PCB is connected, we have an RTC. Initialise it.
    if g_config.HAVE_PCB:
      self.rtc = ExtRTC(i2c,
        net_update=g_config.NET_UPDATE)         # this will also clear interrupts
      self.rtc.rtc_ext.high_capacitance = True  # the pcb uses a 12.5pF capacitor
      self.rtc.update()                         # (time-server->)ext-rtc->int-rtc

    self.done           = DigitalInOut(PIN_DONE)
    self.done.direction = Direction.OUTPUT
    self.done.value     = 0

    self.vbus_sense           = DigitalInOut(board.VBUS_SENSE)
    self.vbus_sense.direction = Direction.INPUT

    # display
    if g_config.HAVE_DISPLAY:

      displayio.release_displays()

      # spi - if not already created
      if not g_config.HAVE_SD:
        self._spi = busio.SPI(PIN_SD_SCK,PIN_SD_MOSI)

      if g_config.HAVE_DISPLAY == "Inky-Pack":
        self.display = DisplayFactory.inky_pack(self._spi)
      elif g_config.HAVE_DISPLAY == "Display-Pack":
        self.display = DisplayFactory.display_pack(self._spi)
        self.display.auto_refresh = False
      else:
        g_logger.print(f"unsupported display: {g_config.HAVE_DISPLAY}")
        g_config.HAVE_DISPLAY = None
      self._view = None


    # just for testing
    if g_config.TEST_MODE:
      self._led            = DigitalInOut(board.LED)
      self._led.direction  = Direction.OUTPUT

    self.save_status = "__"

    #configure sensors
    self._configure_sensors(i2c)

  # --- configure sensors   ---------------------------------------------------

  def _configure_sensors(self,i2c):
    """ configure sensors """

    self._formats = []
    self.csv_header = f"#ID: {g_config.LOGGER_ID}\n#Location: {g_config.LOGGER_LOCATION}\n"
    self.csv_header += "#ts"

    self._sensors = []
    for sensor in g_config.SENSORS.split(' '):
      sensor_module = builtins.__import__(sensor,None,None,[sensor.upper()],0)
      sensor_class = getattr(sensor_module,sensor.upper())
      _sensor = sensor_class(g_config,None,i2c,None,None)
      self._sensors.append(_sensor.read)
      self._formats.extend(_sensor.formats)
      self.csv_header += f",{_sensor.headers}"

  # --- create view   ---------------------------------------------------------

  def _create_view(self):
    """ create data-view """

    # guess best dimension
    if len(self._formats) < 5:
      dim = (2,2)
    elif len(self._formats) < 7:
      dim = (3,2)
    elif len(self._formats) < 13:
      dim = (3,4)
    else:
      raise Exception("too many sensors")

    self._formats.extend(
      ["" for _ in range(dim[0]*dim[1] - len(self._formats))])

    border  = 1
    divider = 1
    padding = 5
    self._view = DataView(
      dim=dim,
      width=self.display.width-2*border-(dim[1]-1)*divider,
      height=int(0.6*self.display.height),
      justify=Justify.LEFT,
      fontname=f"fonts/{g_config.FONT_DISPLAY}.bdf",
      formats=self._formats,
      border=border,
      divider=divider,
      color=Color.BLACK,
      bg_color=Color.WHITE
    )

    for i in range(0,dim[0]*dim[1],2):
      self._view.justify(Justify.LEFT,index=i)
      self._view.justify(Justify.RIGHT,index=i+1)

    # create DataPanel
    title = PanelText(text=f"{g_config.LOGGER_TITLE}",
                      fontname=f"fonts/{g_config.FONT_DISPLAY}.bdf",
                      justify=Justify.CENTER)

    self._footer = PanelText(text=f"Updated: ",
                             fontname=f"fonts/{g_config.FONT_DISPLAY}.bdf",
                             justify=Justify.RIGHT)
    self._panel = DataPanel(
      width=self.display.width,
      height=self.display.height,
      view=self._view,
      title=title,
      footer=self._footer,
      border=border,
      padding=5,
      justify=Justify.CENTER,
      color=Color.BLACK,
      bg_color=Color.WHITE
    )

  # --- blink   --------------------------------------------------------------

  def blink(self, count=1, blink_time=0.25):
    for _ in range(count):
      self._led.value = 1
      time.sleep(blink_time)
      self._led.value = 0
      time.sleep(blink_time)

  # --- check for continuous-mode   ------------------------------------------

  def continuous_mode(self):
    """ returns false if on USB-power """

    return g_config.FORCE_CONT_MODE or (
            self.vbus_sense.value and not g_config.FORCE_STROBE_MODE)

  # --- collect data   -------------------------------------------------------

  def collect_data(self):
    """ collect sensor data """

    ts = time.localtime()
    ts_str = f"{ts.tm_year}-{ts.tm_mon:02d}-{ts.tm_mday:02d}T{ts.tm_hour:02d}:{ts.tm_min:02d}:{ts.tm_sec:02d}"
    self.data = {
      "ts":   ts_str
      }
    self.record = ts_str

    self.values = []
    for read_sensor in self._sensors:
      rec = read_sensor(self.data,self.values)
      self.record += f",{rec}"

  # --- check if file already exists   --------------------------------------

  def file_exists(self, filename):
    """ check if file exists """
    try:
      status = os.stat(filename)
      return True
    except OSError:
      return False

  # --- save data   ----------------------------------------------------------

  def save_data(self):
    """ save data """

    if g_config.SHOW_UNITS:
      self.pretty_print()
    else:
      g_logger.print(self.record)

    if g_config.HAVE_SD:
      YMD = self.data["ts"].split("T")[0]
      outfile = f"/sd/log_{g_config.LOGGER_ID}_{YMD}.csv"
      new_csv = not self.file_exists(outfile)
      self.save_status = ":("
      with open(outfile, "a") as f:
        if new_csv:
          f.write(f"{self.csv_header}\n")
        f.write(f"{self.record}\n")
        self.save_status = "SD"

  # --- pretty-print data to console   ---------------------------------------

  def pretty_print(self):
    """ pretty-print data to console """

    columns = self.csv_header.split('#')[-1].split(',')
    merged = zip(columns,self.record.split(','))
    for label,value in merged:
      space = '\t\t' if len(label) < 9 else '\t'
      g_logger.print(f"{label}:{space}{value}")
    
  # --- send data   ----------------------------------------------------------

  def send_data(self):
    """ send data using LORA """
    g_logger.print(f"not yet implemented!")

  # --- update display   -----------------------------------------------------

  def update_display(self):
    """ update display """

    gc.collect()
    if not self._view:
      self._create_view()

    # fill in unused cells
    self.values.extend([None for _ in range(len(self._formats)-len(self.values))])

    self._view.set_values(self.values)
    dt, ts = self.data['ts'].split("T")
    self._footer.text = f"at {dt} {ts} {self.save_status}"
    self.display.root_group = self._panel
    self.display.refresh()
    g_logger.print("finished refreshing display")

    if not self.continuous_mode():
      time.sleep(3)              # refresh returns before it is finished

  # --- set next wakeup   ----------------------------------------------------

  def configure_wakeup(self):
    """ configure rtc for next wakeup """
    if g_config.HAVE_PCB:
      self.rtc.set_alarm(self.rtc.get_alarm_time(m=g_config.OFF_MINUTES))

  # --- shutdown   -----------------------------------------------------------

  def shutdown(self):
    """ tell the power-controller to cut power """

    self.done.value = 1
    time.sleep(0.2)
    self.done.value = 0
    time.sleep(2)

  # --- cleanup   -----------------------------------------------------------

  def cleanup(self):
    """ cleanup ressources """

    self._spi.deinit()

# --- main program   ---------------------------------------------------------

g_logger.print("main program start")
if g_config.TEST_MODE:
  time.sleep(5)                        # give console some time to initialize
g_logger.print("setup of hardware")

app = DataCollector()
app.setup()

while True:
  if g_config.TEST_MODE:
    app.blink(count=g_config.BLINK_START, blink_time=g_config.BLINK_TIME_START)

  app.collect_data()
  try:
    app.save_data()
  except:
    g_logger.print("exception during save_data()")
    app.cleanup()
    raise
    
  if g_config.TEST_MODE:
    app.blink(count=g_config.BLINK_END, blink_time=g_config.BLINK_TIME_END)

  if g_config.HAVE_DISPLAY:
    try:
      app.update_display()
    except:
      g_logger.print("exception during update_display()")
      app.cleanup()
      raise

  if g_config.HAVE_LORA:
    app.send_data()

  # check if running on USB and sleep instead of shutdown
  if app.continuous_mode():
    g_logger.print(f"continuous mode: next measurement in {g_config.CONT_INT} seconds")
    time.sleep(g_config.CONT_INT)
  else:
    break

app.configure_wakeup()
app.shutdown()
