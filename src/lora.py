#-----------------------------------------------------------------------------
# LoRa TX and RX using adafruit_rfm9x.py in /lib folder.
#
# Naming convention:
#   - filenames in lowercase (lora.py)
#   - class name the same as filename but in uppercase (LORA)
#   - the constructor must take five arguments (config,i2c0,ic1,spi0,spi1)
#     and probe for the device
#   - i2c1 is the default i2c-device and should be probed first
#   - the read-method must update the data and return a string with the
#     values for the csv-record
#
# Author: Syed Omer Ali
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

import time
import adafruit_rfm9x
import config
from log_writer import Logger
g_logger = Logger()
#import board
#import busio
#import digitalio

class LORA:

  def __init__(self, freq=433.0, spi=None, CS=None, RESET=None, ENABLE=None):
    """ constructor """
    try:
        if spi:
            # Define pins connected to the chip, use these if wiring up the breakout according to the guide:            
            g_logger.print("Enabling rfm9x on SPI1")
            ENABLE.value = 1
            time.sleep(config.LORA_ENABLE_TIME)
            g_logger.print("Initializing rfm9x on SPI1")
            self.rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, freq, baudrate=100000)
            g_logger.print("Detected rfm9x on spi")

            self.rfm9x.node = config.NODE_ADDRESS                    # node or this device
            self.rfm9x.destination = config.BASE_STATION_ADDRESS  # base station or destination
    except Exception as ex:
        g_logger.print(f"exception: {ex}")


  def broadcast(self):
    g_logger.print('staring broadcasting...')
    # Send a broadcast message from this node with ID
    self.rfm9x.send(
        bytes("Lora test: logger_id={}, node_address={}".format(config.LOGGER_ID, self.rfm9x.node), "UTF-8")
    )
    # TODO: change this to send_with_ack

  def transmit(self, string):
    # Transmit a UTF-8 formatted string as bytes
    self.rfm9x.send(bytes(string, "UTF-8"))
    # TODO: change this to send_with_ack
