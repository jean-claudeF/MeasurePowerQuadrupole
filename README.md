# MeasurePowerQuadrupole
Measure input and output voltage, current and power for quadrupoles

![Picture](/measure_quadrupole.png)

I use this measuring device to design and control stepup or stepdown DC converters.
It uses an INA168 to measure current in the high side line, so that there can be a common ground for input and output.
With the configuration Rshunt = 10mOhm and Rout = 50kOhm for the INA168, there is a range 0...30A for the current.

The voltage range is 0...60V in the shown configuration.

The LM358 are selected for low offset voltage, it would be better to use special low offset opamps.

There is a PWM output that can be used to control the stepup converter.
Using this I could measure the MPP curve of my solar panels:

![Picture](/solar_01.png)

The module mpptrack_xx.py contains a class Measure4pole that allows to use the measuring device as an object.
This allows MPP tracking and measuring:

```python
# Define object with or without connected OLED:
m4p = Measure4pole(adc, pwmgen, oled = oled)
#m4p = Measure4pole(adc, pwmgen, oled = None)

m4p.set_calibration(k0, k1, k2, k3, offset0, offset1)
m4p.set_pwm(0.3)

# Track MPP, set PWM accordingly in regular intervals
# Display values 
i = 0
while True:
    if i % 10 == 0:
        if oled:
            oled.print("MPP tracking")
        m4p.mpp_track()
        
    ##i1, i2, v1, v2, p1, p2, eta = m4p.measure()
    m4p.measure()
    m4p.print_values()
    m4p.print_oled()
    i += 1
    time.sleep(1)
```


