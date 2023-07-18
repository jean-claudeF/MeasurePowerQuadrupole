'''Measure voltages, currents and power for a quadrupole'''

nb = 11                  # nb of points for mean value
rate = 4              # 0...7     # 0 = slowest and with most accuracy
pausetime = 0.01
raw = False

k0 = 1.02584814     #1.0014
k1 = 1.016    #0.969305
k3 = 21*1.007
k4 = 21*1.007
offset0 = 0.00085
offset1 = 0.0008

#--------------------------------------------------------------

from ADC_ADS1115_03 import ADS1115
import time
from machine import Pin, I2C
from OLED_03 import OLED
from pwmc import PWMc

d15 = Pin(15, Pin.OUT)          # for debugging purposes
i2c_channel = 0
sclpin = 9
sdapin = 8
i2c = I2C(i2c_channel, scl=Pin(sclpin), sda=Pin(sdapin))
adc = ADS1115(i2c, address = 72, gain = 1)
oled = OLED(128, 64, i2c, rotate = 180)
pw = PWMc(3, freq= 16E3)

#--------------------------------------------------------------

def print_oled(i1, i2, v1, v2, p1, p2):
    oled.clear()
    #oled.fill_rect(60, 0, 30, 64, 0)      # clear variables only
    s =  'I1/A = %2.2f' % i1
    s += '\tI2/A = %2.2f' % i2
    s += '\tV1/V = %2.2f' % v1
    s += '\tV2/V = %2.2f' % v2
    s += '\tP1/W = %2.2f' % p1
    s += '\tP2/W = %2.2f' % p2
    
    oled.print_s(s)
    
#--------------------------------------------------------------
    
def calculate(v):
    if raw == False:
        v[0] = v[0] - offset0
        v[1] = v[1] - offset1
                    
        i1 = v[0] *10 * k0 
        i2 = v[1] *10 * k1 
        v1 = v[2] * k3
        v2 = v[3] * k4
    else:
        i1 = v[0]
        i2 = v[1]
        v1 = v[2]
        v2 = v[3]
    
    if v1 <0:
        v1 = 0
    if v2 <0:
        v2 = 0    
        
    p1 = v1 * i1
    p2 = v2 * i2
    return i1, i2, v1, v2, p1, p2
#-------------------------------------------------------------
def progressbar(i):
    # progressbar on the right side of display
    i = i % 64
    if i == 0:
        #i = 0
        oled.fill_rect(120, 0, 8, 64, 0)
    oled.fill_rect(120, 0, 8, i, 1)
    oled.show()


#--------------------------------------------------------------
def continuous_measure():
    i = 0
    while True:
        
        progressbar(i)

        d15.on()
        v = adc.read_all_meanvalue(rate = rate,  nb = nb)
        i1, i2, v1, v2, p1, p2 = calculate(v)
        d15.off()
        
        print( i, '\t', '%2.4f' % i1, '\t', '%2.4f' % i2, '\t', '%2.4f' % v1, '\t', '%2.4f' % v2, '\t', '%3.0f' % p1, '\t', '%3.0f' % p2)
        print_oled(i1, i2, v1, v2, p1, p2)
               
        time.sleep(pausetime)
        i += 1
        
        

def measure_VIPpwm(p, nb = 3):
    # p = PWM in %
    pp = p/100
    pw.set_pwm(pp)
    #time.sleep(0.3)
    v = adc.read_all_meanvalue(rate = rate,  nb = nb)
    i1, i2, v1, v2, p1, p2 = calculate(v)
    if p1 > p2:
        eta = p2/p1
    else:
        eta = 0
        
    print( pp,'\t', '%2.4f' % i1, '\t', '%2.4f' % i2, '\t', '%2.4f' % v1, '\t', '%2.4f' % v2, '\t', '%3.0f' % p1, '\t', '%3.0f' % p2, '\t', '%1.2f' % eta)
    print_oled(i1, i2, v1, v2, p1, p2)
    

def pwm_sweep(min, max, step, nb = 3):
    for p in range(min, max, step):
        measure_VIPpwm(p,  nb = nb)
    measure_VIPpwm(0)
    
        
    
#--------------------------------------------------------------
if __name__ == '__main__':
    continuous_measure()
    #pwm_sweep(0, 90, 2)
    