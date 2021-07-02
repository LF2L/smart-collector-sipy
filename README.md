# Smart Collector Sigfox version 

This project aims to create an open source smart collector. The objective of collector is to communicate the weight of its content.

## Features of the devices 
* Measure the weight of its content
* Measure the state of the battery
* Send the information to sigfox backend

## Hardware  
PYCOM LOPY 4

## Firmeware
This devices use the PyBytes 1.20.2.r4 firmeware. However, it will not use. 


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