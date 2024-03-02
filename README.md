# UPS-Hat-for-Raspberry-Pi
<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/banner.png" />

## UPS Hat is a 5v power supply, It fit at the top of the raspberry pi, it gives power backup, while raspberry pi's USB power is cut off. It has various protections like short circuit protection, reverse battery protection and indicator, overcharge/discharge protection, and over current protection. It has a 5V USB output, convenient for powering other boards.
<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/inout-voltage.png" />

## Features
  * Two on board battery reverse indicator Led's 
  * Two on board USB power port for external devices
  * Onboard oled display, for displaying current, voltage,power and battery percentage of UPS HAT
  * Onboard Battery Pack Protection and Charge Balance IC 

## Specification:-
- **Output voltage :** 5V USB 
- **Charger :** 8.4V 2A (Recommended)
- **Commuincation :** I2C 
- **Power monitoring IC :** INA219
- **Battery Supported :** 18650 Li Battery
- Display=>
 	* **Type** : OLED
 	* **Screen Size** : 0.91"
 	* **Resolution** : 128x32 pixels
 	* **Color** : Monochrome
	 * **Interface** : I2C
    
## Code
### First of all, you need to enable I2C in raspberry pi, for this you need to go  ```sudo raspi-config ``` then go to "interface options->I2C->yes->press enter" 
### This folder contains two python files and Images, Fonts folder:-
   * **INA219_UPS.py**  -> This file you need to run, displays the load voltage, current, power, and battery percentage on the terminal as well as in OLED
   * **oled_091.py**    ->This is the OLED display library 
   * **Images folder** contains images which we display in OLED display
   * **Fonts folder** contain various fonts, which we use in the OLED display
   
## Steps To Use UPS HAT (Follow These Steps) (**Important** *)
### Connect the type c power to the raspberry pi first, then turn on the UPS HAT, then disconnect the type c power from the raspberry pi or turn off the raspberry pi external power (at this time raspberry pi restart due to sudden power drop)Then reconnect the type c power to the Raspberry Pi after that ( In this process your raspberry pi needs to restart one time if you use UPS backup), The Raspberry Pi now does not restart if the type c power is turned off or if the external power is turned off.
### You need to follow this process when you use UPS HAT. if you use this process, your OLED problem is also resolved(static noise pattern)

  * Fix UPS HAT at the top of the Raspberry Pi
  
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img1.JPG" />
   
  * Plug the Power cable to raspberry pi

    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img2.JPG" />
    
  * Now Switch on UPS HAT using slider switch,then disconnect the type c power from the raspberry pi or turn off the raspberry pi external power (at this time             raspberry pi restart due to sudden power drop)Then reconnect the type c power to the Raspberry Pi after that ( In this process your raspberry pi needs to restart       one time if you use UPS backup)
  
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img3.JPG" />
    
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img4.JPG" />
    
    **Disconnect the external power**
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img5.png" />
    
    **Reconnect the external power**
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img6.png" />
   
  
  
  
## Run a Program On Your Raspberry Pi At Startup (*optional)
Go to below directory

 ```sudo nano /etc/rc.local```
 
 ```sudo python3 /home/pi/UPS-Hat-RPi/INA219_UPS.py &```
 
 <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img_1.JPG" />
 
 Press Control+X then press Y to save

   
## Working
<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/giff.gif" />
