#-----------------------------------------------------------------------------
# This class implements a singleton for logging. The constructor takes
# a single argument:
#
#   - None: don't print logmessages
#   - 'console': use normal print-statements for logging
#   - logfile: log to logfile 
#   - uart: an uart-object to receive the log statements
#   - in case of exceptions the latter two fall back to normal print output
#
# Note: this is a singleton, i.e. the logger is only configured the
#       very first time the constructor is called. This should be done
#       early in the (main) program.
#
# Credits: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

import time

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
      instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

@singleton
class Logger():
  def __init__(self,target=None):
    """ constructor: save debug-target """
    self._target = target
    if target is None:
      self.print = lambda x: None
    elif isinstance(target,str):
      if target == 'console':
        self._print = self._print_to_console
      else:
        self._print = self._log_to_sd
    else:
      self._print = self._log_to_uart

  def print(self,msg):
    """ add timestamp and delegate to correct method """

    ts = time.localtime()
    ts_str = ("[%04d-%02d-%02d %02d:%02d:%02d]" %
              (ts.tm_year,ts.tm_mon,ts.tm_mday,
               ts.tm_hour,ts.tm_min,ts.tm_sec)
    )
    self._print(f"{ts_str} {msg}")

  def _print_to_console(self,msg):
    """ print to console """
    print(msg)

  def _log_to_sd(self,msg):
    """ write log to file """
    try:
      with open(self._target, "a") as f:
        f.write(f"{msg}\n")
    except:
      print(msg)

  def _log_to_uart(self,msg):
    """ write log to uart """
    try:
      self._target.write(bytes(f"{msg}\r\n",'utf-8'))
    except:
      print(msg)
