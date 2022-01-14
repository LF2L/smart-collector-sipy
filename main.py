import time
import pycom
import machine
from machine import Pin
from hx711 import HX711
import ujson
from microWebCli import MicroWebCli
# required for Sigfox
from network import Sigfox, WLAN
import socket
import ubinascii

# Micro-controller settings
uplink_intervalle = 30              # minutes #time between two messages
calibration_factor = 43.57          # callibration factor that is specific to each load cell
sleeping_time = 0.4                 # time to wait before doing any measurement to be sure voltage is stable to have a correct measurment
production = True                   # disable print commands for on-field deployement, should be false for debug 
communicationEnabled = True         # enable/ disable communication with distant server. usefull while testing the firmware
MCUid = "1B2A0F9"                   # ID that will be send through API request

# API
apiURL = "" # URL of the API that will collect the data 
APIuser= ""
APIpassword = ""

# Wifi Parameters
WifiEnabled = True                  # enable/ disable the use of the WIFI connectity. Effective only if "communicationEnabled" is True. 
WiFi_SSID = ""
Wifi_pass= ''
NB_TRYWIFI = 20

def sleep():
    wakeupPin = Pin('P23', mode=Pin.IN, pull=Pin.PULL_DOWN)
    # setup the way to manually wake up. enable_pull= True disable ULP or capacitive touch wakeup
    machine.pin_sleep_wakeup(
    (wakeupPin,), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

    # start the deepsleep for a defined duration
    machine.deepsleep(1000*60*uplink_intervalle)

def sendDataWifi(weightData, batteryData):
    _try = 0
    wlan = WLAN(mode=WLAN.STA)

    wlan.connect(ssid=WiFi_SSID, auth=(WLAN.WPA2, Wifi_pass))

    while not wlan.isconnected():  # ou timeout
        machine.idle()
        
        _try +=1
        if _try >= NB_TRYWIFI:
           print("Impossible to connect WiFi network, go to deep sleep")
           sleep()

    if not production: print("WiFi connected succesfully")

    data_in_int = int(weightData)
    data_in_bytes = data_in_int.to_bytes(2, 'big')
    weight_hex = ubinascii.hexlify(data_in_bytes)

    # convert battery data
    batt_data_in_int = int(batteryData)
    batt_data_in_bytes = batt_data_in_int.to_bytes(2, 'big')
    batt_hex = ubinascii.hexlify(batt_data_in_bytes)

    payload = {
        "device": MCUid,
        "payload": weight_hex + batt_hex
    }

    print("payload: {}".format(payload))

    auth   = MicroWebCli.AuthBasic(APIuser, APIpassword)
    
    response = MicroWebCli.JSONRequest(apiURL+MCUid, o=payload, auth= auth )    

    if(response != None):
        if not production : print("Success {}".format(response))
    else:
         if not production : print("Request failed: {}".format(response))
    


def sendDataSigfox(weightData, batteryData):
    # init Sigfox for RCZ1 (Europe)
    Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

    # create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    # make the socket blocking
    s.setblocking(True)

    # configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    # convert weight data
    data_in_int = int(weightData)
    data_in_bytes = data_in_int.to_bytes(2, 'big')

    # convert battery data
    batt_data_in_int = int(batteryData)
    batt_data_in_bytes = batt_data_in_int.to_bytes(2, 'big')

    # send the data through sigfox
    s.send(data_in_bytes + batt_data_in_bytes)


def tare_sensor(loadCellRef):
    # tare the sensor
    loadCellRef.tare()

    # create a dictionnary with tare info
    persistant_data = {'offset': loadCellRef.OFFSET}

    # save it into persistant memory
    rtc.memory(ujson.dumps(persistant_data))


def weight_measure(loadCellRef):
    # get the data from the persistant memory
    raw_data = rtc.memory()

    # if the memory is not empty
    if raw_data != b'':

        pycom.rgbled(0x007f00)  # green light
        if not production:
            print("Something in the persistant memory")

        # convert the data from the memory
        persistant_data = ujson.loads(raw_data)

        # set the offset of the sensor (tare)
        loadCellRef.set_offset(persistant_data['offset'])

        # weight_measure the weight
        weight = loadCellRef.get_units(10)

        if weight < 0:
            weight = 0

        # weight_measure the battery state
        battVal = 0 #apin.voltage()
        if not production:
            print("weight: {} g".format(weight))
            print("battery: {} v".format(battVal))
            data_in_int = int(weight)
            data_in_bytes = data_in_int.to_bytes(2, 'big')
            batt_data_in_int = int(battVal)
            batt_data_in_bytes = batt_data_in_int.to_bytes(2, 'big')
            print("Weight Data: {} ".format(data_in_bytes))
            print("Battery Data: {} ".format(batt_data_in_bytes))

        # call the function to send data
        if communicationEnabled and not WifiEnabled:
            sendDataSigfox(int(weight), battVal)
        elif communicationEnabled and WifiEnabled:
            sendDataWifi(int(weight), battVal)

        pycom.rgbled(0x000000)  # black light

    else:
        pycom.rgbled(0x7f0000)  # RED light
        # if it is empty, display a red light for 5s
        if not production:
            print("Nothing in the persistant memory: No tare")


##############  MAIN #############
# start = time.ticks_us()
if not production:
    print("Wake up")
# disable LED blinking
pycom.heartbeat(False)

# Initialize RTC
rtc = machine.RTC()

# Initialize ADC
adc = machine.ADC()

# Affect the pin
apin = adc.channel(pin='P16')

# init the sensor
loadCell = HX711('P3', 'P4')
# time.sleep(sleeping_time)
loadCell.set_scale(calibration_factor)

# get the reason why MCU is waking up
(wake_reason, gpio_list) = machine.wake_reason()

# MCU woke up through the reset button on the Lopy4 board
if wake_reason == machine.PWRON_WAKE:
    pycom.rgbled(0x007f7f)
    if not production:
        print("Woke up by reset button")
    time.sleep(sleeping_time)
    weight_measure(loadCell)

# MCU woke up through the external tare button
elif wake_reason == machine.PIN_WAKE:
    pycom.rgbled(0x00007f)
    if not production:
        print("Woke up by external pin (external interrupt)")

    # wait several microsec that power supply stabilize in order to do a correct tare
    time.sleep(sleeping_time)

    # call the function to tare
    tare_sensor(loadCell)
    weight_measure(loadCell)

elif wake_reason == machine.RTC_WAKE:
    pycom.rgbled(0xFFF81B)
    if not production:
        print("Woke up by RTC (timer ran out)")

    # wait several microsec that power supply stabilize in order to do correct measure
    time.sleep(sleeping_time)

    weight_measure(loadCell)

if not production:
    print("Deep sleep")

sleep()