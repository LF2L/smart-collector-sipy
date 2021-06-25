from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='stanmeurthe-eqt', auth=(WLAN.WPA2, 'lk!?$08C=6V1odKWHbN'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())