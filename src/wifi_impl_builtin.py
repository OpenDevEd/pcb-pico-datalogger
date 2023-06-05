# ----------------------------------------------------------------------------
# wifi_impl_builtin.py: Wifi-implementation for builtin wifi
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pico-e-ink-daily
#
# ----------------------------------------------------------------------------

import board
import time
import socketpool
import adafruit_requests

from secrets import secrets

class WifiImpl:
  """ Wifi-implementation for MCU with integrated wifi """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    if not hasattr(secrets,'channel'):
      secrets.channel = 0
    if not hasattr(secrets,'timeout'):
      secrets.timeout = None

  # --- initialze and connect to AP and to remote-port   ---------------------

  def connect(self):
    """ initialize connection """

    import wifi
    print("connecting to %s" % secrets.ssid)
    retries = secrets.retry
    while True:
      try:
        wifi.radio.connect(secrets.ssid,
                           secrets.password,
                           channel = secrets.channel,
                           timeout = secrets.timeout
                           )
        break
      except:
        print("could not connect to %s" % secrets.ssid)
        retries -= 1
        if retries == 0:
          raise
        time.sleep(1)
        continue
    print("connected to %s" % secrets.ssid)
    pool = socketpool.SocketPool(wifi.radio)
    self._requests = adafruit_requests.Session(pool)

  # --- execute get-request   -----------------------------------------------

  def get(self,url):
    """ process get-request """

    return self._requests.get(url)

  # --- no specific deep-sleep mode   ---------------------------------------

  def deep_sleep(self):
    """ disable radio """

    try:                                       # wifi might not be imported
      wifi.radio.enabled = False
    except:
      pass
