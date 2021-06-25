import time
import pycom
import machine
from machine import Pin
from hx711 import HX711
import ujson
from network import Sigfox
import socket

uplink_intervalle = 12 # minutes

def measure():
    value = hx711.get_value()/394.786
    print("{} g".format(int(value)))
    return value

def sendData(weightData, batteryData):
    print("Start the data sending procedure")
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

def tare_sensor():
    # tare the sensor
    hx711.tare()

    # create a dictionnary with tare info 
    persistant_data = {'offset': hx711.OFFSET}

    # save it into persistant memory
    rtc.memory(ujson.dumps(persistant_data))

def procedure():
    # get the data from the persistant memory
    raw_data = rtc.memory()
    # if the memory is not empty
    if raw_data  != b'':

        pycom.rgbled(0x007f00) # green light
        print("Something in the persistant memory")
        
        # convert the data from the memory 
        persistant_data = ujson.loads(raw_data)
        # set the offset of the sensor (tare)
        hx711.set_offset(persistant_data['offset'])

        # measure the weight
        weight = measure()

        # measure the battery state
        battVal = apin() 
        print("weight: {}".format(weight))

        # call the function to send data
        sendData(int(weight), battVal)

    else:
        pycom.rgbled(0x7f0000) # RED light
        # if it is empty, display a red light for 5s 
        print("Nothing in the persistant memory: No tare")



##############  MAIN #############
print("Wake up")

# Initialize RTC
rtc = machine.RTC()

# Initialize ADC
adc = machine.ADC()

# Affect the pin
apin = adc.channel(pin='P16')
Pin('P23', mode=Pin.IN, pull=Pin.PULL_DOWN)

# init the sensor
hx711 = HX711('P3','P4')

# disable LED blinking
pycom.heartbeat(False)

# get the reason why MCU is waking up
(wake_reason, gpio_list) = machine.wake_reason()

# MCU woke up through the reset button on the Lopy4 board
if wake_reason == machine.PWRON_WAKE:
    pycom.rgbled(0x007f7f)
    print("Woke up by reset button")
    procedure()

# MCU woke up through the external tare button
elif wake_reason == machine.PIN_WAKE:
    pycom.rgbled(0x00007f)
    print("Woke up by external pin (external interrupt)")
    # print in log which button triggered the wakeup
    print(*gpio_list, sep=", ")

    # call the function to tare 
    tare_sensor()
    procedure()
     
elif wake_reason == machine.RTC_WAKE:
    pycom.rgbled(0xFFF81B)
    print("Woke up by RTC (timer ran out)")

    procedure()

# wait several second just for development
time.sleep(5)

print("Deep sleep")
# setup the way to manually wake up. enable_pull= True disable ULP or capacitive touch wakeup
machine.pin_sleep_wakeup(('P23',), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

# start the deepsleep for a defined duration
machine.deepsleep(1000*60*uplink_intervalle) # 12 min