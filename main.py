import pycom
from microWebCli import MicroWebCli
import urequests
import machine
import network
import time


#Keep a list of various WiFi networks you would like to be able to connect to
#ex. "SSID": "PASSWORD",
dict_of_wifi = {
    "HUAWEI P smart 2019": "***********",
}#Function to connect to WiFi - with 10 retries
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    i = 1
    if not wlan.isconnected():
        pycom.rgbled(0xFF0000)
        for _ in range(10):
            print('connecting to network...' + str(i))
            #if not a new connection, just use cache
            wlan.connect()
            time.sleep(30)
            #If we are having trouble connecting (fifth try)
            #check available WiFi and try to connect
            #to WiFi specified in dict_of_wifi if available
            if not wlan.isconnected() and i == 5:
                ssid = wlan.scan()
                for x in ssid:
                    pycom.rgbled(0xFF00FF)
                    for wifi_ssid in dict_of_wifi:
                        if wifi_ssid in str(x):
                            wlan.connect(wifi_ssid, dict_of_wifi[wifi_ssid])
                            print('Trying ' + str(wifi_ssid))
                            time.sleep(30)
                            break
                        else:
                            pass
            i += 1
            if wlan.isconnected():
                print('Connected.')
                break
            time.sleep(30)
        else:
            print('Fail')
    print('network config:', wlan.ifconfig())

try:
   #This loops forever, so adjust this to your own needs
   while True:
        pycom.rgbled(0xFF0000)
        #Connect to WiFi
        wlan = network.WLAN(network.STA_IF)
        #If we aren't connected to WiFi, then connect
        if not wlan.isconnected():
            print("not connected to WiFi...")
            do_connect()
        #Wait after connecting to WiFi
        time.sleep(5)
        #Then put your code here:
        pycom.rgbled(0x00FF00)
        contentBytes = MicroWebCli.GETRequest('http://jsonplaceholder.typicode.com/posts/99')
        print(contentBytes)

        url = 'http://jsonplaceholder.typicode.com/posts/8'
        res = urequests.get(url)
        print(res.text)
        res.close()
        #....
        #....
        #Check WiFi connection every 15 min (will loop and check the connection)
        time.sleep(900)
        #machine.idle()
except Exception as error:
    #pycom.rgbled(0xFF0000)
    #text = str(e)
    print("There was a problem")
    print(error)
    #If there is an error, I like to reboot my ESP8266,
    #so I do that here
    time.sleep(600)
    #machine.idle()
    #machine.reset()