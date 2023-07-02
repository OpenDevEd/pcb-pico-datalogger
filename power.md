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
"off-time" (at 3V).


Pico-W Current vs. Voltage
--------------------------

The Pico (-W) does not follow Ohm's law. It is more of a constant
energy-device. The consequence is that the current draw is higher for
lower voltages than for higher voltages. Also, the current ripple is
higher for low voltages, probably due to the internal DC-DC converters
that try to maintain the internal 1.8V and 3.3V voltages.

Some measurements (Pico-W):

| Voltage (V)| Idle Current (mA)|
|------------|------------------|
|         3.2|                49|
|         3.0|                53|
|         2.8|                55|
|         2.6|                65|
|         2.4|                69|
|         2.2|                82|


Operation Voltage and Capacity
------------------------------

The Pico-W works down to 1.8V, even with attached sensors. The exact
threshold voltage probably depends on the current draw of the attached
sensors and maybe some other factors (e.g. sample variation). Since
alkalines are considered "empty" at about 0.9V, this means that the
datalogger can theoretically use the full capacity of the cells.


Current Measurements
--------------------

The test-setup uses a typical set of sensors for temperature, humidity,
light and noise (measured at 3V):

  - AHT20 (temperature/humidity)
  - LTR599 (light)
  - PDM-mic (noise)

The results for these sensors (including SD-card and e-ink display):

![](current-aht20-ltr599-pdm-sd-display.png)

Average current for "on-time" (18secs) is 57.26mA, used energy is
18/3600*57.26mA = 0.2863mAh.

Same data without the e-ink display:

![](current-aht20-ltr599-pdm-sd.png)

Average current for "on-time" (6 secs) is 68,08mA, used energy is
6/3600*68,08mA = 0.1135mAh.


Extrapolated Current Usage
--------------------------

The following calculations don't take the variable current draw into
account. I.e. the real current draw will be higher.

Four measurements per hour with display: 4 * 24 = 96 measurements a day
with a total on time of 96 * 18 secs = 1728 secs. Off time is 84672 secs.

  - on: 4 * 24 * 0.2863mAh = 27,4848mAh
  - off: 84672/3600 * 75µA = 1.764mAh

So per day the needed energy is 29.25mAh

Four measurements per hour without display: 4 * 24 = 96 measurements a day
with a total on time of 96 * 6 secs = 576 secs. Off time is 85824 secs.

  - on: 4 * 24 * 0.1135mAh = 10.89mAh
  - off: 85824/3600 * 75µA = 1.788mAh

So per day the needed energy is 12.68mAh.

