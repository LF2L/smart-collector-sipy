# Smart Collector Sigfox version 

This project aims to create an open source smart collector. The objective of collector is to communicate the weight of its content.

## Features of the devices 
* Measure the weight of its content
* Measure the state of the battery
* Send the information to sigfox backend
* Tare weight

## Working principle
To have further hint about how the prgram of the device work, activity diagrams are available [here](doc/img/ActivityDiagrams.md).

## Hardware  
* [PYCOM LOPY 4](https://pycom.io/product/lopy4/)
* [PYCOM Expansion Board 3](https://pycom.io/product/expansion-board-3-0/)
* LiPo Battery
* [5 Kg Load cell](https://www.gotronic.fr/art-capteur-de-force-5-kg-czl635-5-17599.htm)
* [Analog digital converter - hx711](https://www.gotronic.fr/art-amplificateur-hx711-grove-101020712-31346.htm)


## Firmeware
This devices use the PyBytes 1.20.2.r4 firmeware.


## Documentation/ references 
[Pycom Hard reset when the microcontroller is not accessible](https://docs.pycom.io/gettingstarted/programming/safeboot/)  
[Pybytes](https://pybytes.pycom.io)

## Usefull command in REPL

Factory reset your module to remove your code
```
>>> import os
>>> os.fsformat('/flash')
```

## Notes
In order to update the firmeware without the board, the pin P2 has to be connected to GND. It is the bootloader mode [USB serial programming](https://docs.pycom.io/gettingstarted/programming/usbserial/)


## Color Code
![#007f00](https://via.placeholder.com/15/007f00/000000?text=+) `#007f00` Measuring the weight

![#7f0000](https://via.placeholder.com/15/7f0000/000000?text=+) `#7f0000` Tare data not found in the persistant memory

![#007f7f](https://via.placeholder.com/15/007f7f/000000?text=+) `#007f7f` Wake up from reset button

![#00007f](https://via.placeholder.com/15/00007f/000000?text=+) `#00007f` Wake up from tare button

![#FFF81B](https://via.placeholder.com/15/FFF81B/000000?text=+) `#FFF81B` Wake up from RTC time out