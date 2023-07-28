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
import busio
import digitalio

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


  def lora_range_test(PIN_LORA_CS,PIN_LORA_RST,PIN_LORA_EN,PIN_LORA_SCK,PIN_LORA_MOSI,PIN_LORA_MISO):
      transmit_interval = 10
      print("Hello World on Pico!")
      # Define radio parameters.
      RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
      # module! Can be a value like 915.0, 433.0, etc.

      # Define pins connected to the chip, use these if wiring up the breakout according to the guide:
      CS = digitalio.DigitalInOut(PIN_LORA_CS)
      RESET = digitalio.DigitalInOut(PIN_LORA_RST)
      # Or uncomment and instead use these if using a Feather M0 RFM69 board
      # and the appropriate CircuitPython build:
      # CS = digitalio.DigitalInOut(board.RFM69_CS)
      # RESET = digitalio.DigitalInOut(board.RFM69_RST)

      # Define the onboard LED
      EN = digitalio.DigitalInOut(PIN_LORA_EN)
      EN.direction = digitalio.Direction.OUTPUT
      EN.value = 1

      # Initialize SPI bus, busio.SPI(SCK, MOSI, MISO)
      spi = busio.SPI(clock=PIN_LORA_SCK, MOSI=PIN_LORA_MOSI, MISO=PIN_LORA_MISO)

      # Initialze RFM radio
      rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

      # set node addresses
      rfm9x.node = 1
      rfm9x.destination = 100
      # initialize counter
      counter = 0
      # send a broadcast message from my_node with ID = counter
      rfm9x.send(
      bytes("Startup message {} from node {}".format(counter, rfm9x.node), "UTF-8")
      )
      # Wait to receive packets.
      print("Waiting for packets...")
      now = time.monotonic()
      while True:
          # Look for a new packet: only accept if addresses to my_node
          packet = rfm9x.receive(with_header=True)
          # If no packet was received during the timeout then None is returned.
          if packet is not None:
              # Received a packet!
              # Print out the raw bytes of the packet:
              print("Received (raw header):", [hex(x) for x in packet[0:4]])
              print("Received (raw payload): {0}".format(packet[4:]))
              print("Received RSSI: {0}".format(rfm9x.last_rssi))
          if time.monotonic() - now > transmit_interval:
              now = time.monotonic()
              counter = counter + 1
              # send a  mesage to destination_node from my_node
              rfm9x.send(
                  bytes(
                      "message number {} from node {}".format(counter, rfm9x.node), "UTF-8"
                  ),
                  keep_listening=True,
              )
              button_pressed = None