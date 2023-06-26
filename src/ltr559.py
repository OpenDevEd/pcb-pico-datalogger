#-----------------------------------------------------------------------------
# Sensor definition for LTR559.
#
# Naming convention:
#   - filenames in lowercase (ltr559.py)
#   - class name the same as filename in uppercase (LTR559)
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

from pimoroni_circuitpython_ltr559 import Pimoroni_LTR559

class LTR559:
  formats = ["L/LTR:", "{0:.0f}lx"]
  headers = 'L/LTR lx'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """

    try:
      if i2c1:
        self.ltr559 = Pimoroni_LTR559(i2c1)
    except:
      if i2c0:
        self.ltr559 = Pimoroni_LTR559(i2c0)

  def read(self,data,values):
    lux = self.ltr559.lux
    data["ltr559"] = {
      "lux": lux
    }
    values.extend([None,lux])
    return f"{lux:.0f}"
