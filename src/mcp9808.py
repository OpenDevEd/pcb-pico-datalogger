#-----------------------------------------------------------------------------
# Sensor definition for MCP9808.
#
# Naming convention:
#   - filenames in lowercase (mcp9808.py)
#   - class name the same as filename in uppercase (MCP9808)
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

class MCP9808:
  formats = ["T/MCP:", "{0:.1f}°C"]
  headers = 'T/MCP °C'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """

    import adafruit_mcp9808
    try:
      if i2c1:
        self.mcp9808 = adafruit_mcp9808.MCP9808(i2c1)
    except:
      if i2c0:
        self.mcp9808 = adafruit_mcp9808.MCP9808(i2c0)

  def read(self,data,values):
    t = self.mcp9808.temperature
    data["mcp9808"] = {
      "temp": t
    }
    values.extend([None,t])
    return  f"{t:0.1f}"
