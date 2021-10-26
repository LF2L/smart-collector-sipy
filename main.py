import time
import pycom
import machine
from machine import Pin
from hx711 import HX711
import ujson
from network import Sigfox
import socket

uplink_intervalle = 20 # minutes
calibration_factor = 423.6 #430.3
production = False

def measure(loadCell):
    value = loadCell.get_units(10)
    return value

def sendData(weightData, batteryData):
    if not production: print("Start the data sending procedure")
    # init Sigfox for RCZ1 (Europe)
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

    # create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    # make the socket blocking
    s.setblocking(True)

    # configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

    # convert weight data
    data_in_int= int(weightData)
    data_in_bytes = data_in_int.to_bytes(2,'big')

    # convert battery data
    batt_data_in_int = int(batteryData)
    batt_data_in_bytes = batt_data_in_int.to_bytes(2,'big')

    # send the data through sigfox
    s.send(data_in_bytes +batt_data_in_bytes )

def tare_sensor(loadCell):
    time.sleep(0.5)
    # tare the sensor
    loadCell.tare()

    if not production: print("Offset measured: "+ str(loadCell.OFFSET))

    # create a dictionnary with tare info 
    persistant_data = {'offset': loadCell.OFFSET}

    # save it into persistant memory
    rtc.memory(ujson.dumps(persistant_data))

def procedure(loadCell):
    # get the data from the persistant memory
    raw_data = rtc.memory()
    # if the memory is not empty
    if raw_data  != b'':

        pycom.rgbled(0x007f00) # green light
        if not production: print("Something in the persistant memory")
        
        # convert the data from the memory 
        persistant_data = ujson.loads(raw_data)

        if not production: print("Persistant offset = {}".format(persistant_data['offset']))
        # set the offset of the sensor (tare)
        loadCell.set_offset(persistant_data['offset'])
        if not production: print("scale: {}".format(loadCell.SCALE))
        if not production: print("offset: {}".format(loadCell.OFFSET))
        # measure the weight
        weight = measure(loadCell)

        # measure the battery state
        battVal = apin.voltage()
        if not production: print("weight: {} g".format(weight))
        
        # call the function to send data
        sendData(int(weight), battVal)
        pycom.rgbled(0x000000) # black light

    else:
        pycom.rgbled(0x7f0000) # RED light
        # if it is empty, display a red light for 5s 
        if not production: print("Nothing in the persistant memory: No tare")



##############  MAIN #############
# start = time.ticks_us()
if not production: print("Wake up")
# disable LED blinking
pycom.heartbeat(False)

# Initialize RTC
rtc = machine.RTC()

# Initialize ADC
adc = machine.ADC()

# Affect the pin
apin = adc.channel(pin='P16')
wakeupPin = Pin('P23', mode=Pin.IN, pull=Pin.PULL_DOWN)

# init the sensor
loadCell = HX711('P3','P4')
loadCell.set_scale(calibration_factor)

# get the reason why MCU is waking up
(wake_reason, gpio_list) = machine.wake_reason()

# MCU woke up through the reset button on the Lopy4 board
if wake_reason == machine.PWRON_WAKE:
    pycom.rgbled(0x007f7f)
    if not production: print("Woke up by reset button")
    procedure(loadCell)

# MCU woke up through the external tare button
elif wake_reason == machine.PIN_WAKE:
    pycom.rgbled(0x00007f)
    if not production: print("Woke up by external pin (external interrupt)")
    # print in log which button triggered the wakeup
    #if not production: print(*gpio_list, sep=", ")

    # call the function to tare 
    tare_sensor(loadCell)
    procedure(loadCell)
     
elif wake_reason == machine.RTC_WAKE:
    pycom.rgbled(0xFFF81B)
    if not production: print("Woke up by RTC (timer ran out)")
    procedure(loadCell)

if not production: print("Deep sleep")
# setup the way to manually wake up. enable_pull= True disable ULP or capacitive touch wakeup
machine.pin_sleep_wakeup((wakeupPin,), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

# print("process time: ", time.ticks_diff(time.ticks_us(), start))

# start the deepsleep for a defined duration
machine.deepsleep(1000*60*uplink_intervalle)