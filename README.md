# Smart Collector WIFI version 

This project aims to create an open source smart collector. The objective of collector is to communicate the weight of its content.

## Features of the devices 
* Measure the weight of its content
* Send the information to a distant server

## Hardware  
PYCOM LOPY 4


## Documentation/ references 
[Pycom Hard reset when the microcontroller is not accessible](https://docs.pycom.io/gettingstarted/programming/safeboot/)

## Usefull command in REPL

Factory reset your module to remove your code
```
>>> import os
>>> os.fsformat('/flash')
```

In order to update the firmeware without the board, the pin P2 has to be connected to GND. It is the bootloader mode [USB serial programming](https://docs.pycom.io/gettingstarted/programming/usbserial/)