import time
import pycom
import machine
from machine import Pin
from hx711 import HX711
import ujson

def tare_sensor():
    # tare the sensor
    hx711.tare()
    # create a dictionnary with tare info 
    persistant_data = {'offset': hx711.OFFSET}
    # save it into persistant memory
    rtc.memory(ujson.dumps(persistant_data))

print("Wake up")

rtc = machine.RTC()
pycom.heartbeat(False)
Pin('P6', mode=Pin.IN, pull=Pin.PULL_DOWN)

# get the reason why MCU is waking up
(wake_reason, gpio_list) = machine.wake_reason()

# init the sensor
hx711 = HX711('P3','P4')

if wake_reason == machine.PWRON_WAKE:
    print("Woke up by reset button")
    pycom.rgbled(0x007f7f)
elif wake_reason == machine.PIN_WAKE:
    print("Woke up by external pin (external interrupt)")
    pycom.rgbled(0x00007f)
    print(*gpio_list, sep=", ")
    # call the function to tare 
    tare_sensor()
     
elif wake_reason == machine.RTC_WAKE:
    print("Woke up by RTC (timer ran out)")
    # Load data from persistant memory 
    raw_data = rtc.memory()
    # chech if the memory is not empty
    if raw_data  != b'':
        # display a green light 
        pycom.rgbled(0x007f00)
        # convert the data from the memory 
        persistant_data = ujson.loads(raw_data)
        # set the sensor correctly
        hx711.set_offset(persistant_data.offset)
        # do a measure
        value = hx711.get_value()
        print(int(value/394.786), " g")
        # send the information
        pybytes.send_signal(3, int(value/394.786))
    else:
        # if it is empty, display a red light for 5s 
        pycom.rgbled(0x00007f)
        time.sleep(5)

# wait several second just for development
time.sleep(5)

print("Deep sleep")
# setup the way to manually wake up. enable_pull= True disable ULP or capacitive touch wakeup
machine.pin_sleep_wakeup(('P6',), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

# start the deepsleep for a defined duration
machine.deepsleep(1000*60)