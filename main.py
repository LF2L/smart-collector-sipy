import time
import pycom
from machine import Timer
from hx711 import HX711

class Clock:

    def __init__(self):
        #self.seconds = 0
        self.__alarm = Timer.Alarm(self._seconds_handler, 60, periodic=True)

    def _seconds_handler(self, alarm):
        pycom.rgbled(0x007f00)
        value = hx711.get_value()
        print(int(value/394.786), " g")
        pybytes.send_signal(3, int(value/394.786))
        pycom.rgbled(0x000000)
        #self.seconds += 1
        #print("%02d seconds have passed" % self.seconds)
        #if self.seconds == 10:
        #    alarm.cancel() # stop counting after 10 seconds

val = 0;
hx711 = HX711('P3','P4')
hx711.tare()

pycom.heartbeat(False)
print("start")

clock = Clock()

print("after clock")


