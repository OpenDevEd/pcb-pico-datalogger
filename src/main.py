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

import time
import board
import alarm
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

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

from dataviews.Base import Color, Justify
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# --- default configuration, override in config.py on sd-card   --------------

TEST_MODE   = False       # set to FALSE for a productive setup
NET_UPDATE  = True        # update RTC from time-server if time is invalid
OFF_MINUTES = 1           # turn off for x minutes
BLINK_TIME  = 0.25        # blink time of LED
BLINK_START = 0           # blink n times before start of data-collection
BLINK_END   = 0           # blink n times after finish of data-collection

FORCE_CONT_MODE       = False
FORCE_SHUTDOWN_ON_USB = False
CONT_INT              = 30          #  interval in continuous mode (in seconds)

HAVE_SD      = False
HAVE_DISPLAY = True
HAVE_LORA    = False
HAVE_AHT20   = True
HAVE_LTR559  = True
HAVE_MCP9808 = True
HAVE_ENS160  = False

LOGGER_NAME  = 'Darasa Kamili'  # Perfect Classroom
LOGGER_ID    = 'N/A'            # Change this to your logger id
LOGGER_LOCATION = '6G5X46G4+XQ' # Plus Code for Dar airport
LOGGER_TITLE = LOGGER_NAME + " " + LOGGER_LOCATION

# --- pin-constants (don't change unless you know what you are doing)   ------

PIN_DONE = board.GP4   # connect to 74HC74 CLK
PIN_SDA  = board.GP2   # connect to RTC
PIN_SCL  = board.GP3   # connect to RTC

PIN_SD_CS   = board.GP22
PIN_SD_SCK  = board.GP18
PIN_SD_MOSI = board.GP19
PIN_SD_MISO = board.GP16

PIN_INKY_CS   = board.GP17
PIN_INKY_RST  = board.GP21
PIN_INKY_DC   = board.GP20
PIN_INKY_BUSY = board.GP26
FONT_INKY     = 'DejaVuSansMono-Bold-18-subset'

class DataCollector():
  """ main application class """

  # --- hardware-setup   -----------------------------------------------------

  def setup(self):
    """ create hardware-objects """

    # i2c - RTC and sensors
    i2c = busio.I2C(PIN_SCL,PIN_SDA)
    self.rtc = ExtRTC(i2c,net_update=NET_UPDATE)  # this will also clear interrupts
    self.rtc.rtc_ext.high_capacitance = True      # the pcb uses a 12.5pF capacitor
    self.rtc.update()                             # (time-server->)ext-rtc->int-rtc

    self.done           = DigitalInOut(PIN_DONE)
    self.done.direction = Direction.OUTPUT
    self.done.value     = 0

    self.vbus_sense           = DigitalInOut(board.VBUS_SENSE)
    self.vbus_sense.direction = Direction.INPUT

    # spi - SD-card and display
    if HAVE_SD:
      self._spi = busio.SPI(PIN_SD_SCK,PIN_SD_MOSI,PIN_SD_MISO)

    # SD-card
    if HAVE_SD:
      self.sd_cs = DigitalInOut(PIN_SD_CS)
      sdcard     = adafruit_sdcard.SDCard(self._spi,self.sd_cs)
      self.vfs   = storage.VfsFat(sdcard)
      storage.mount(self.vfs, "/sd")
      try:
        import sys
        sys.path.append("/sd")
        import config
        for var in dir(config):
          if var[0] != '_':
            print(f"{var}={getattr(config,var)}")
            globals()[var] = getattr(config,var)
        sys.path.pop()
      except:
        print("no configuration found in /sd/config.py")

    # display
    if HAVE_DISPLAY:

      displayio.release_displays()

      # spi - if not already created
      if not HAVE_SD:
        self._spi = busio.SPI(PIN_SD_SCK,PIN_SD_MOSI,PIN_SD_MISO)

      display_bus = displayio.FourWire(
        self._spi, command=PIN_INKY_DC, chip_select=PIN_INKY_CS,
        reset=PIN_INKY_RST, baudrate=1000000
      )
      self.display = InkyPack.InkyPack(display_bus,busy_pin=PIN_INKY_BUSY)
      self._view = None
 
    # sensors
    self._formats = ["Bat","{0:0.1f}V"]
    self._sensors = [self.read_battery]    # list of readout-methods
    if HAVE_AHT20:
      import adafruit_ahtx0
      self.aht20 = adafruit_ahtx0.AHTx0(i2c)
      self._sensors.append(self.read_AHT20)
      self._formats.extend(
        ["T/AHT:", "{0:.1f}°C","H/AHT:", "{0:.0f}%rH"])
    if HAVE_LTR559:
      from pimoroni_circuitpython_ltr559 import Pimoroni_LTR559
      self.ltr559 = Pimoroni_LTR559(i2c)
      self._sensors.append(self.read_LTR559)
      self._formats.extend(["L/LTR:", "{0:.1f}Lux"])
    if HAVE_MCP9808:
      import adafruit_mcp9808
      self.mcp9808 = adafruit_mcp9808.MCP9808(i2c)
      self._sensors.append(self.read_MCP9808)
      self._formats.extend(["T/MCP:", "{0:.1f}°C"])
    if HAVE_ENS160:
      import adadruit_ens160
      self.ens160 = adafruit_ens160.ENS160(i2)
      self._sensors.append(self.read_ENS160)
      self._formats.extend(["AQI (ENS160):", "{0}"])
      self._formats.extend(["TVOC (ENS160):", "{0} ppb"])
      self._formats.extend(["eCO2 (ENS160):", "{0} ppm eq."])

    # just for testing
    if TEST_MODE:
      self._led            = DigitalInOut(board.LED)
      self._led.direction  = Direction.OUTPUT

  # --- create view   ---------------------------------------------------------

  def _create_view(self):
    """ create data-view """

    # guess best dimension
    if len(self._formats) < 5:
      dim = (2,2)
    elif len(self._formats) < 7:
      dim = (3,2)
    else:
      dim = (3,4)
    self._formats.extend(
      ["" for _ in range(dim[0]*dim[1] - len(self._formats))])
    self._view = DataView(
      dim=dim,
      width=self.display.width-2-(dim[1]-1),
      height=int(0.6*self.display.height),
      justify=Justify.LEFT,
      fontname=f"fonts/{FONT_INKY}.bdf",
      formats=self._formats,
      border=1,
      divider=1,
      color=Color.BLACK,
      bg_color=Color.WHITE
    )

    for i in range(0,dim[0]*dim[1],2):
      self._view.justify(Justify.LEFT,index=i)
      self._view.justify(Justify.RIGHT,index=i+1)

    # create DataPanel
    title = PanelText(text=f"{LOGGER_TITLE}",
                      fontname=f"fonts/{FONT_INKY}.bdf",
                      justify=Justify.CENTER)

    self._footer = PanelText(text=f"Updated: ",
                             fontname=f"fonts/{FONT_INKY}.bdf",
                             justify=Justify.RIGHT)
    self._panel = DataPanel(
      width=self.display.width,
      height=self.display.height,
      view=self._view,
      title=title,
      footer=self._footer,
      border=1,
      padding=5,
      justify=Justify.RIGHT,
      color=Color.BLACK,
      bg_color=Color.WHITE
    )

  # --- blink   --------------------------------------------------------------

  def blink(self,count=1):
    for _ in range(count):
      self._led.value = 1
      time.sleep(BLINK_TIME)
      self._led.value = 0
      time.sleep(BLINK_TIME)

  # --- check for continuous-mode   ------------------------------------------

  def continuous_mode(self):
    """ returns false if on USB-power """

    return FORCE_CONT_MODE or (
            self.vbus_sense.value and not FORCE_SHUTDOWN_ON_USB)

  # --- collect data   -------------------------------------------------------

  def collect_data(self):
    """ collect sensor data """

    ts = time.localtime()
    ts_str = f"{ts.tm_year}-{ts.tm_mon:02d}-{ts.tm_mday:02d}T{ts.tm_hour:02d}:{ts.tm_min:02d}:{ts.tm_sec:02d}"
    print(ts)
    self.data = {
      "ts":   ts_str
      }
    self.record = ts_str
    self.values = []
    for read_sensor in self._sensors:
      read_sensor()

  # --- read battery level   -------------------------------------------------

  def read_battery(self):
    """ read battery level """

    adc = AnalogIn(board.VOLTAGE_MONITOR)
    level = adc.value *  3 * 3.3 / 65535
    adc.deinit()
    self.data["battery"] = level
    self.record += f",{level:0.1f}"
    self.values.extend([None,level])

  # --- read AHT20   ---------------------------------------------------------

  def read_AHT20(self):
    t = self.aht20.temperature
    h = self.aht20.relative_humidity
    self.data["aht20"] = {
      "temp": t,
      "hum":  h
    }
    self.record += f",{t:0.1f},{h:0.0f}"
    self.values.extend([None,t])
    self.values.extend([None,h])

  # --- read LTR559   --------------------------------------------------------

  def read_LTR559(self):
    lux = self.ltr559.lux
    self.data["ltr559"] = {
      "lux": lux
    }
    self.record += f",{lux:0.1f}"
    self.values.extend([None,lux])

  # --- read MCP9808   -------------------------------------------------------

  def read_MCP9808(self):
    t = self.mcp9808.temperature
    self.data["mcp9808"] = {
      "temp": t
    }
    self.record += f",{t:0.1f}"
    self.values.extend([None,t])

  # --- read ENS160   --------------------------------------------------------

  def read_ENS160(self):
    if HAVE_AHT20:
      self.ens160.temperature_compensation = self.data["aht20"]["temp"]
      self.ens160.humidity_compensation    = self.data["aht20"]["hum"]
    data   = self.ens160.read_all_sensors()
    status = self.ens160.data_validity
    self.data["ens160"] = data
    self.record += f",{status},{data['AQI']},{data['TVOC']},{data['eCO2']}"
    self.values.extend([None,data['AQI']])
    self.values.extend([None,data['TVOC']])
    self.values.extend([None,data['eCO2']])

  # --- save data   ----------------------------------------------------------

  def save_data(self):
    """ save data """
    print(self.record)
    if HAVE_SD:
      with open(f"/sd/{LOGGER_ID}.csv", "a") as f:
        f.write(f"{self.record}\n")

  # --- send data   ----------------------------------------------------------

  def send_data(self):
    """ send data using LORA """
    print(f"not yet implemented!")

  # --- update display   -----------------------------------------------------

  def update_display(self):
    """ update display """
    import re
    
    if not self._view:
      self._create_view()

    # fill in unused cells
    self.values.extend([None for _ in range(len(self._formats)-len(self.values))])

    self._view.set_values(self.values)
    ts = re.sub("T", " ", self.data['ts'])
    self._footer.text = f"at {ts}"
    self.display.root_group = self._panel
    self.display.refresh()

  # --- set next wakeup   ----------------------------------------------------

  def configure_wakeup(self):
    """ configure rtc for next wakeup """
    self.rtc.set_alarm(self.rtc.get_alarm_time(m=OFF_MINUTES))

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

print("main program start")
if TEST_MODE:
  time.sleep(5)                        # give console some time to initialize
print("setup of hardware")

app = DataCollector()
app.setup()

while True:
  if TEST_MODE:
    app.blink(count=BLINK_START)

  app.collect_data()
  try:
    app.save_data()
  except:
    print("exception during save_data()")
    app.cleanup()
    raise

  if TEST_MODE:
    app.blink(count=BLINK_END)

  if HAVE_DISPLAY:
    try:
      app.update_display()
    except:
      print("exception during update_display()")
      app.cleanup()
      raise

  if HAVE_LORA:
    app.send_data()

  # check if running on USB and sleep instead of shutdown
  if app.continuous_mode():
    print(f"continuous mode: next measurement in {CONT_INT} seconds")
    time.sleep(CONT_INT)
  else:
    break

app.configure_wakeup()
app.shutdown()

