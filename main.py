import pycom
import time
import machine
from network import WLAN
from microWebCli import MicroWebCli

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)

pycom.rgbled(0xFF0000)

SSID = "HUAWEI P smart 2019" #replace this value by the wifi access point name
KEY = '*************' #replace this value by the wifi access point key

wlan.connect(ssid=SSID, auth=(WLAN.WPA2, KEY))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

pycom.rgbled(0x00FF00)


contentBytes = MicroWebCli.GETRequest('https://jsonplaceholder.typicode.com/posts/99')
print(contentBytes)