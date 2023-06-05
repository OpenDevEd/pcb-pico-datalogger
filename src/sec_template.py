# ----------------------------------------------------------------------------
# Template file for secrets.py. Adapt to your needs and rename to secrets.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-datalogger
#
# ----------------------------------------------------------------------------

class Settings:
  pass

secrets = Settings()

secrets.ssid      = 'my_wlan_ssid'
secrets.password  = 'my_very_secret_password'
secrets.retry     = 2
secrets.debugflag = False
#secrets.channel   = 6         # optional
#secrets.timeout   = 10        # optional

secrets.time_url = 'http://worldtimeapi.org/api/ip'
