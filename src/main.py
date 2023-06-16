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
import array
import math

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

from dataviews.DisplayFactory import DisplayFactory
from dataviews.Base import Color, Justify
from dataviews.DataView  import DataView
from dataviews.DataPanel import DataPanel, PanelText

# --- default configuration is in config.py on the pico.
#     You can override it also with a config.py on the sd-card   -------------

def import_config():
  """ import config-module and make variables global """
  import config
  for var in dir(config):
    if var[0] != '_':
      print(f"{var}={getattr(config,var)}")
      globals()[var] = getattr(config,var)
  config = None
  gc.collect()

import_config()

# --- pin-constants (don't change unless you know what you are doing)   ------

PIN_DONE = board.GP4   # connect to 74HC74 CLK
PIN_SDA  = board.GP2   # connect to sensors and RTC via I2C interface
PIN_SCL  = board.GP3   # connect to sensors and RTC via I2C interface

# SD-card interface (SPI)
PIN_SD_CS   = board.GP22
PIN_SD_SCK  = board.GP18
PIN_SD_MOSI = board.GP19
PIN_SD_MISO = board.GP16

# PDM-mic
PIN_PDM_CLK = board.GP5
PIN_PDM_DAT = board.GP28

# display interface (SPI, Inky-Pack)
PIN_INKY_CS   = board.GP17
PIN_INKY_RST  = board.GP21
PIN_INKY_DC   = board.GP20
PIN_INKY_BUSY = board.GP26

FONT_INKY     = 'DejaVuSans-16-subset'

class DataCollector():
  """ main application class """

  # --- hardware-setup   -----------------------------------------------------

  def setup(self):
    """ create hardware-objects """

    # Initialse i2c bus for use by sensors and RTC
    i2c = busio.I2C(PIN_SCL,PIN_SDA)

    # If our custom PCB is connected, we have an RTC. Initialise it.
    if HAVE_PCB:
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
        sys.path.insert(0,"/sd")
        import_config()
        sys.path.pop(0)
      except:
        print("no configuration found in /sd/config.py")

    # display
    global HAVE_DISPLAY
    if HAVE_DISPLAY:

      displayio.release_displays()

      # spi - if not already created
      if not HAVE_SD:
        self._spi = busio.SPI(PIN_SD_SCK,PIN_SD_MOSI)

      if HAVE_DISPLAY == "Inky-Pack":
        self.display = DisplayFactory.inky_pack(self._spi)
      elif HAVE_DISPLAY == "Display-Pack":
        self.display = DisplayFactory.display_pack(self._spi)
        self.display.auto_refresh = False
      else:
        print(f"unsupported display: {HAVE_DISPLAY}")
        HAVE_DISPLAY = None
      self._view = None

    # sensors
    self._formats = ["Bat:","{0:0.1f}V"]
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
      self._formats.extend(["L/LTR:", "{0:.1f}lx"])
    if HAVE_BH1750:
      import adafruit_bh1750
      self.bh1750 = adafruit_bh1750.BH1750(i2c)
      self._sensors.append(self.read_bh1750)
      self._formats.extend(["L/bh1750:", "{0:.1f}lx"])
    if HAVE_MCP9808:
      import adafruit_mcp9808
      self.mcp9808 = adafruit_mcp9808.MCP9808(i2c)
      self._sensors.append(self.read_MCP9808)
      self._formats.extend(["T/MCP:", "{0:.1f}°C"])
    if HAVE_ENS160:
      import adadruit_ens160
      self.ens160 = adafruit_ens160.ENS160(i2)
      self._sensors.append(self.read_ENS160)
      self._formats.extend(["AQI:", "{0}"])
      self._formats.extend(["TVOC:", "{0} ppb"])
      self._formats.extend(["eCO2:", "{0} ppm eq."])
    if HAVE_MIC_PDM_MEMS:
      import audiobusio
      self.mic = audiobusio.PDMIn(PIN_PDM_CLK,PIN_PDM_DAT,
                                  sample_rate=16000, bit_depth=16)
      self._sensors.append(self.read_PDM)
      self._formats.extend(["Noise:", "{0:0.0f}"])

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

  def blink(self, count=1, blink_time=0.25):
    for _ in range(count):
      self._led.value = 1
      time.sleep(blink_time)
      self._led.value = 0
      time.sleep(blink_time)

  # --- check for continuous-mode   ------------------------------------------

  def continuous_mode(self):
    """ returns false if on USB-power """

    return FORCE_CONT_MODE or (
            self.vbus_sense.value and not FORCE_STROBE_MODE)

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

  # --- read bh1750   --------------------------------------------------------

  def read_bh1750(self):
    lux = self.bh1750.lux
    self.data["bh1750"] = {
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

  # --- read PDM-mic    ------------------------------------------------------

  def read_PDM(self):
    samples = array.array('H', [0] * 160)
    self.mic.record(samples, len(samples))

    mean_samples = int(sum(samples)/len(samples))
    sum2_samples = sum(
        float(sample - mean_samples) * (sample - mean_samples)
        for sample in samples
    )
    mag = math.sqrt(sum2_samples / len(samples))
    self.data["pdm"] = {
      "mag": mag
    }
    self.record += f",{mag:0.0f}"
    self.values.extend([None,mag])

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
    YMD = self.data["ts"].split("T")[0]
    outfile = f"log_{LOGGER_ID}-{YMD}.csv"
    if HAVE_SD:
        outfile = "/sd/" + outfile
        with open(outfile, "a") as f:
            f.write(f"{self.record}\n")
    
  # --- send data   ----------------------------------------------------------

  def send_data(self):
    """ send data using LORA """
    print(f"not yet implemented!")

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
    self._footer.text = f"at {dt} {ts}"
    self.display.root_group = self._panel
    self.display.refresh()
    print("finished refreshing display")

    if not self.continuous_mode():
      time.sleep(3)              # refresh returns before it is finished

  # --- set next wakeup   ----------------------------------------------------

  def configure_wakeup(self):
    """ configure rtc for next wakeup """
    if HAVE_PCB:
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
    app.blink(count=BLINK_START, blink_time=BLINK_TIME_START)

  app.collect_data()
  try:
    app.save_data()
  except:
    print("exception during save_data()")
    app.cleanup()
    raise

  if TEST_MODE:
    app.blink(count=BLINK_END, blink_time=BLINK_TIME_END)

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
