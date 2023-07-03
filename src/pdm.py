#-----------------------------------------------------------------------------
# Sensor definition for PDM.
#
# Naming convention:
#   - filenames in lowercase (pdm.py)
#   - class name the same as filename in uppercase (PDM)
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

import board
import audiobusio
import array
import math

# PDM-mic
PIN_PDM_CLK = board.GP5
PIN_PDM_DAT = board.GP28

class PDM:
  formats = ["Noise:", "{0:0.0f}"]
  headers = 'Noise'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """

    self.mic = audiobusio.PDMIn(PIN_PDM_CLK,PIN_PDM_DAT,
                                sample_rate=16000, bit_depth=16)

  def read(self,data,values):
    samples = array.array('H', [0] * 160)
    self.mic.record(samples, len(samples))

    mean_samples = int(sum(samples)/len(samples))
    sum2_samples = sum(
        float(sample - mean_samples) * (sample - mean_samples)
        for sample in samples
    )
    mag = math.sqrt(sum2_samples / len(samples))
    data["pdm"] = {
      "mag": mag
    }
    values.extend([None,mag])
    return f"{mag:0.0f}"
