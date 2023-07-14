#-----------------------------------------------------------------------------
# Sensor definition for SHT31.
#
# Naming convention:
#   - filenames in lowercase (sht31.py)
#   - class name the same as filename in uppercase (SHT31)
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

class SHT31:
  formats = ["T/A=SHT:", "{0:.1f}°C","H/SHT:", "{0:.0f}%rH"]
  headers = 'T/SHT °C,H/SHT %rH'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """
    try:
      if i2c1:
        g_logger.print("testing  on i2c1")
        self.sht31 = adafruit_sht31d.SHT31D(i2c1)
        g_logger.print("detected sht31 on i2c1")
    except Exception as ex:
      g_logger.print(f"exception: {ex}")
      if i2c0:
        g_logger.print("testing sht31 on i2c0")
        self.sht31 = adafruit_sht31d.SHT31D(i2c1)
        g_logger.print("detected sht31 on i2c0")

  def read(self,data,values):
    """ read sensor """
    t = self.sht31.temperature
    h = self.sht31.relative_humidity
    data["sht31"] = {
      "temp": t,
      "hum":  h
    }
    values.extend([None,t])
    values.extend([None,h])
    return f"{t:0.1f},{h:0.0f}"
