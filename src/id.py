#-----------------------------------------------------------------------------
# Sensor definition for the LOGGER_ID (pseudo-sensor)
#
# Naming convention:
#   - filenames in lowercase (aht20.py)
#   - class name the same as filename in uppercase (AHT20)
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

class ID:
  formats = []             # empty: don't show on display
  headers = 'ID'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """
    self._config = config

  def read(self,data,values):
    """ 'read' id """

    data["id"] = self._config.LOGGER_ID
    return f"{self._config.LOGGER_ID}"
