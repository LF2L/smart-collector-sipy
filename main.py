import pycom
from microWebCli import MicroWebCli
import urequests
import machine
import time
from network import WLAN

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)

pycom.rgbled(0xFF0000)

SSID = "HUAWEI P smart 2019" #replace this value by the wifi access point name
KEY = '*************' #replace this value by the wifi access point key

#wlan.connect(ssid='HUAWEI P smart 2019', auth=(WLAN.WPA2, '61547849cad7'))
#while not wlan.isconnected():
    #time.sleep_ms(50)
#    machine.sleep(50)
#print("WiFi connected succesfully")
#print(wlan.ifconfig())

nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        pycom.rgbled(0xFF00FF)
        print('Network found!')
        wlan.connect(net.ssid, auth=(WLAN.WPA2, KEY), timeout=5000)
        while not wlan.isconnected():
            pycom.rgbled(0x0000FF)
            #time.sleep_ms(1000)
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break




pycom.rgbled(0x00FF00)


contentBytes = MicroWebCli.GETRequest('http://jsonplaceholder.typicode.com/posts/99')
print(contentBytes)

url = 'http://jsonplaceholder.typicode.com/posts/8'
res = urequests.get(url)
print(res.text)
res.close()