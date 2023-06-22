#-----------------------------------------------------------------------------
# Sensor definition for SHT45.
#
# Naming convention:
#   - filenames in lowercase (sht45.py)
#   - class name the same as filename in uppercase (SHT45)
#   - the constructor must take five arguments (config,i2c0,ic1,spi0,spi1)
#     and probe for the device
#   - i2c1 is the default i2c-device and should be probed first
#   - the read-method must update the data and return a string with the
#     values for the csv-record
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

import adafruit_sht4x

class SHT45:
  formats = ["T/SHT:", "{0:.1f}°C","H/SHT:", "{0:.0f}%rH"]
  headers = 'T/SHT °C,H/SHT %rH'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """
    try:
      if i2c1:
        self.sht45 = adafruit_sht4x.SHT4x(i2c1)
    except:
      if i2c0:
        self.sht45 = adafruit_sht4x.SHT4x(i2c0)

  def read(self,data,values):
    """ read sensor """
    t = self.sht45.temperature
    h = self.sht45.relative_humidity
    data["sht45"] = {
      "temp": t,
      "hum":  h
    }
    values.extend([None,t])
    values.extend([None,h])
    return f"{t:0.1f},{h:0.0f}"
