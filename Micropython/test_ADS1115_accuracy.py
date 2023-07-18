'''Test CH0 of ADS1115 for accuracy'''

nb = 3                  # nb of points for mean value
rate = 2                # 0...7     # 0 = slowest and with most accuracy
maxpoints = 50          # nb of analized conversions, there seems to be no great difference if using >= 30
pausetime = 0.001

from ADC_ADS1115_03 import ADS1115
import time
from machine import Pin, I2C
from OLED_03 import OLED

d15 = Pin(15, Pin.OUT)
i2c_channel = 0
sclpin = 9
sdapin = 8
i2c = I2C(i2c_channel, scl=Pin(sclpin), sda=Pin(sdapin))
adc = ADS1115(i2c, address = 72, gain = 1)
oled = OLED(128, 64, i2c, rotate = 180)


min = 3.3
max = 0


for i in range(0, maxpoints):

    #v = read(0, nb, rate)
    d15.on()
    #v = adc.read_meanvalue(rate = rate, channel1 = 0, nb = nb)
    v = adc.read_all_meanvalue(rate = rate,  nb = nb)
    v = v[0]
    d15.off()
    
    # store min and max values
    if v < min:
        min = v
    if v>max:
        max = v
    
    
    #print(i, "    ", v, "   ", min, "    ", max, "    ", (max - min)*1000, "mV")
    e = (max - min)*1000
    print( '%2.2f' % e)
    oled.print('%2.4f' % e)
    
    time.sleep(pausetime)
    
