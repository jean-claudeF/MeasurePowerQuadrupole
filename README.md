# MeasurePowerQuadrupole
Measure input and output voltage, current and power for quadrupoles

![Picture](/measure_quadrupole.png)

I use this measuring device to design and control stepup or stepdown DC converters.
It uses an INA168 to measure current in the high side line, so that there can be a common ground for input and output.
With the configuration Rshunt = 10mOhm and Rout = 50kOhm for the INA168, there is a range 0...30A for the current.

The voltage range is 0...60V in the shown configuration.

The LM358 are selected for low offset voltage, it would be better to use special low offset opamps.



