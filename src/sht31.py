#-----------------------------------------------------------------------------
# Sensor definition for SHT31.
#
# Naming convention:
#   - filenames in lowercase (aht31.py)
#   - class name the same as filename in uppercase (AHT31)
#   - the constructor must take five arguments (config,i2c0,ic1,spi0,spi1)
#     and probe for the device
#   - i2c1 is the default i2c-device and should be probed first
#   - the read-method must update the data and return a string with the
#     values for the csv-record
#
# 
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

from log_writer import Logger
g_logger = Logger()

import adafruit_sht31d

class AHT31:
  formats = ["T/AHT:", "{0:.1f}°C","H/AHT:", "{0:.0f}%rH"]
  headers = 'T/AHT °C,H/AHT %rH'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """
    try:
      if i2c1:
        g_logger.print("testing aht31 on i2c1")
        self.aht31 = adafruit_aht31.AHT31(i2c1)
        g_logger.print("detected aht31 on i2c1")
    except Exception as ex:
      g_logger.print(f"exception: {ex}")
      if i2c0:
        g_logger.print("testing aht31 on i2c0")
        self.aht31 = adafruit_aht31.AHT31(i2c0)
        g_logger.print("detected aht31 on i2c0")

  def read(self,data,values):
    """ read sensor """
    t = self.aht31.temperature
    h = self.aht31.relative_humidity
    data["aht31"] = {
      "temp": t,
      "hum":  h
    }
    values.extend([None,t])
    values.extend([None,h])
    return f"{t:0.1f},{h:0.0f}"
