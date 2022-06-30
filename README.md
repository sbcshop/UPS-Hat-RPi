# UPS-Hat-for-Raspberry-Pi
<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/banner.png" />

The UPS Hat is a 5v power supply. It fits on top of the Raspberry Pi and gives power backup if the Pi's USB power supply is cut off. It has various protections like short circuit protection, reverse battery protection and indicator, overcharge/discharge protection, and overcurrent protection. It has a 5V USB output, convenient for powering other boards.

<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/inout-voltage.png" />

## Features
  * Two on board battery reverse indicator LEDs
  * Two on board USB power port for external devices
  * Onboard OLED display, for displaying current, voltage, power, and battery percentage of UPS HAT

## Code
### Setup

1. Enable I2C in raspberry pi. Run `sudo raspi-config` then go to "interface options->I2C->yes->press enter"
1. Install python libraries: `sudo -H pip3 install -r requirements.txt`

### folder contents

This folder contains two python files and Images, Fonts folders:
   * **INA219_UPS.py**  -> This file you need to run, displays the load voltage, current, power, and battery percentage on the terminal as well as in OLED
   * **oled_091.py**    -> OLED display library
   * **Images/**        -> images which we display in OLED display
   * **Fonts/**         -> various fonts, which we use in the OLED display

## Steps To Use UPS HAT (Follow These Steps) (**Important**)


You need to follow this process when you use UPS HAT. If you use this process, your OLED problem is also resolved (the static noise pattern).

  * Fix UPS HAT at the top of the Raspberry Pi

    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img1.JPG" />

  * Plug the Power cable to raspberry pi

    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img2.JPG" />

Now switch on the UPS HAT using slider switch, then disconnect the USB Type C power from the Raspberry Pi or turn off the Raspberry Pi external power. At this time the Pi may restart due to a sudden power drop.

Then, reconnect the Type C power to the Pi. The Pi needs to restart to use UPS backup. The Pi will now stay running if power is disconnected.

    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img3.JPG" />

    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img4.JPG" />

    **Disconnect the external power**
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img5.png" />

    **Reconnect the external power**
    <img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img6.png" />


## Run a Program On Your Raspberry Pi At Startup (optional)

Edit the following.

```sudo nano /etc/rc.local```

```python3 /home/pi/UPS-Hat-RPi/INA219_UPS.py &```

<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/img_1.JPG" />

Press Control+X then press Y to save


## Working
<img src= "https://github.com/sbcshop/UPS-Hat-for-Raspberry-Pi/blob/main/Images/giff.gif" />
