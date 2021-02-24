# Update the microcontroller with the latest firmware

## Procedure with the Expansion board

* Install [Pycom Upgrade](https://pycom.io/downloads/) ([Windows](https://software.pycom.io/findupgrade?product=pycom-firmware-updater&type=all&platform=win32&redirect=true) - [Mac](https://software.pycom.io/findupgrade?product=pycom-firmware-updater&type=all&platform=macos&redirect=true)- [Linux](https://software.pycom.io/findupgrade?product=pycom-firmware-updater&type=all&platform=macos&redirect=true))

* Close all IDE or any other software that might be using the serial port

* Start Pycom Upgrade

* Start the procedure

![Beginning of the procedure](./img/pycom-upgrade.PNG)

* Instructions

![Instructions](./img/pycom-upgrade-2.PNG)

* Communication setup 

The has to correspond to those identified in VS Code.
Let the speed by default. 

![Beginning of the procedure](./img/pycom-upgrade-3.PNG)

* Choose the Pycom microcontroller used. In our experiment, we used the LoPy 4.

![Beginning of the procedure](./img/pycom-upgrade-4.PNG)

* Choose the Lora country

It is not used in our experimentation but it has to be configured.

![Beginning of the procedure](./img/pycom-upgrade-5.PNG)


* Choose the Sigfox region


![Beginning of the procedure](./img/pycom-upgrade-6.PNG)

* It summerize the parameters of the upgrade

I let the parameters as prompted. Once you press run, it will start the upgrade process, nothing to do except wait.

![Beginning of the procedure](./img/pycom-upgrade-7.PNG)

*  After around 2 minutes, you will see the results. 

If everything work properly, you will see 4 numbers you should keep somewhere because it will be necessary for activate Sigfox.

![Beginning of the procedure](./img/pycom-upgrade-8.PNG)