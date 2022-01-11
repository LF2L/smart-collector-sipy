# Smart Collector - LoPy4 Sigfox version 

This project aims to create an open source smart collector. The objective of the collector is to collect plastic x=waste in the perspective to valorize it into a circular enconomy. The main function of the collector is to communicate the weight of its content.

## Features of the devices 
* Measure the weight of its content
* Measure the state of the battery
* Send the information to sigfox backend
* Tare weight the empty collector before being filled

## Working principle
To have further hint about how the prgram of the device work, activity diagrams are available [here](doc/img/ActivityDiagrams.md).

## Hardware  
* [PYCOM LOPY 4](https://pycom.io/product/lopy4/)
* [PYCOM Expansion Board 3](https://pycom.io/product/expansion-board-3-0/) OR [Battery Management system TP4056](https://www.amazon.fr/Greluma-Interface-Chargeur-Batterie-Protection/dp/B08XWZFPRB/ref=bmx_dp_qanayhuo_5/262-1009802-0928702?pd_rd_w=CqLMz&pf_rd_p=4bc5b1b7-6c70-40d0-a70a-3ed2ca409d95&pf_rd_r=4GV6H1HBT1N7D93DD10B&pd_rd_r=d61cc57d-de6f-49c7-85b7-10e0572cf781&pd_rd_wg=zi9uJ&pd_rd_i=B08XWZFPRB&psc=1)
* LiPo Battery
* [5 Kg Load cell](https://www.gotronic.fr/art-capteur-de-force-5-kg-czl635-5-17599.htm)
* [Analog digital converter - hx711](https://www.gotronic.fr/art-amplificateur-hx711-grove-101020712-31346.htm)

## Software 
* Install VS code 
* Install Pymakr add-on in VS Code
![PyMakr Add-on](./img/VScode-InstallPymakr.PNG)

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

## sources
[MicroWebCli](https://github.com/jczic/MicroWebCli)