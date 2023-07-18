from ADC_ADS1115_02 import ADS1115
import time
from machine import Pin, I2C

i2c_channel = 0
sclpin = 9
sdapin = 8
i2c = I2C(i2c_channel, scl=Pin(sclpin), sda=Pin(sdapin))
adc = ADS1115(i2c, address = 72, gain = 1)

while True:
    
    #v = adc.read(rate = 0, channel1 = 0)
    #v = adc.read(channel1 = 2, channel2 = 3) 
    
    v = adc.read_all_as_string()
    
    print(v)
    time.sleep(1)
    
