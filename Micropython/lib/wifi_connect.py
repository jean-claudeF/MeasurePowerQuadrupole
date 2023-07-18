import network
import time

'''Connect to existing WiFi'''
def connect_wifi(ssid, pwd):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)

    # Wait for connect or fail:
    max_wait = 15
    while max_wait > 0:
        if wlan.status() <0 or wlan.status() >=3:       # status 3 = link up, 0 = link down
            break
        max_wait -= 1
        
        print("Waiting to connect...")
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        ip = None
        print("WiFi connection failed!")
        #raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        ip = status[0]
        print( 'ip = ' + ip )

    return ip
