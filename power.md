Power
=====

The board needs to be powered with one of the following options:

  - Two or three AA or AAA batteries
  - Three AA or AAA rechargeables (take care to get the 'slow discharge' type)
  - A LiPo battery

The RTC requires a CR2032 cell. This cell is not used for operation, it
just keeeps the internal state of the RTC when the standard batteries
are not connected.

The power-management circuit has a leakage current of about 75µA during
"off-time".


Operation Voltage and Capacity
------------------------------

Experiments show that the system won't start up with an voltage below
2.55V (maybe subject to variation).

Normal AA/AAA batteries show a decline of voltage during life-time. Data
from <https://en.wikipedia.org/wiki/Alkaline_battery> suggest that the
threshold of 2.55V is reached at about 80% capacity given a load of
330mW. Given a nominal capacity of about 3000mAh for an AA-alkaline on
low drain, this would mean a usable capacity of about 600mAh.

A possible remediation of this problem is the usage of a boost-converter
that delivers constant voltage over the typical range of battery-voltages.
Since this is a common problem, these converters are available but no
ready to use component is known for the target voltage of 3-3.3V.


Current Measurements
--------------------

The test-setup uses a typical set of sensors for temperature, humidity,
light and noise:

  - AHT20 (temperature/humidity)
  - LTR599 (light)
  - PDM-mic (noise)

The results for these sensors (including SD-card and e-ink display):

![](current-aht20-ltr599-pdm-sd-display.png)

Average current for "on-time" (18secs) is 17.17mA.

Same data without the e-ink display:

![](current-aht20-ltr599-pdm-sd.png)

Average current for "on-time" (6 secs) is 6.8mA.
