# TokenPrinter

[![build status](
  http://img.shields.io/travis/mgarg1/TokenPrinter/master.svg?style=flat)](
 https://travis-ci.org/mgarg1/TokenPrinter

# Getting the sd card ready
* downloaded the buster lite image from [raspian website](https://www.raspberrypi.org/downloads/raspbian/)
* Burned the Image using Etcher for Windows (got from the same source)
* Memory card will have 2 partitions now - 
	* boot partition (Fat32)
	* Actual OS (Ext4)
* In Windows - only boot partition will be shown
* In Linux - boot partition will be read-only
* I created 2 files in boot partition for enabling ssh and wifi:
	*  ssh - empty content
	* wpa_supplicant.conf 

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=IN

network={
 ssid="<Name of your WiFi>"
 psk="<Password for your WiFi>"
}
```
Ref: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

# Connecting to raspi
* Boot up the raspi(and waited for sometime) and checked its entry in the router's Ip table to find out its ip (knowing their MAC in advance will also help)
* ssh pi@192.168.0.102 (ip found from the previous step)
* sudo apt-get update; sudo apt-get -y upgrade
* raspi-config -> Interface settings -> enable VNC (optional)
* raspi-config -> Localisation Options -> Change Timezone -> Asia -> Kolkata

# Setup Real Time Clock - DS3231
* Connect the I2C pins of RTC to pin 3(GPIO 8),5(GPIO 9) of rPi, Vcc and Gnd to pin 1,7 of rPi
* `sudo nano /etc/modules` # and append at the end 
 ```
 rtc-ds1307
 ```
* `sudo apt-get install i2c-tools`
* `sudo i2cdetect -y 1`
* `sudo nano /etc/rc.local` # and append before `exit 0`
```
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
hwclock -s
```
* `sudo reboot`
* check date
* to write the correct time to RTC `sudo hwclock -w`

Ref: https://www.raspberrypi-spy.co.uk/2015/05/adding-a-ds3231-real-time-clock-to-the-raspberry-pi/

# Code Setup
* github repo setup and installation
```
sudo apt-get install git virtualenv  #Install git and virtualenv
git clone https://github.com/mgarg1/TokenPrinter.git
cd TokenPrinter
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```
* python-escpos setup
	* Ref: https://python-escpos.readthedocs.io/en/latest/user/raspi.html
* python-escpos code needs usb persmissions:
```
# give permission to the user for usb:
sudo groupadd usbusers # create new usergroup
sudo usermod -a -G usbusers pi # add user pi to the usbusers group
sudo touch /etc/udev/rules.d/99-usbusers.rules # create this rules file
```
* contents of /etc/udev/rules.d/99-usbusers.rules
```
SUBSYSTEM=="usb", GROUP="usbusers", MODE="0660"
SUBSYSTEMS=="usb", GROUP="usbusers", MODE="0660"
```
* ```sudo init 6``` # restart the pi

Ref:https://www.odoo.com/documentation/user/9.0/point_of_sale/overview/setup.html

15. Connect the printer to another USB port of rPi zero
i. $ lsusb
Bus 001 Device 002: ID 0456:0808 Analog Devices, Inc.
ii. 
15. python3 main.py

# sudo apt-get install python3-rpi.gpio


## Installation on Raspi
```bash
sudo apt-get install libjpeg-dev zlib1g-dev
sudo apt-get install python3-rpi.gpio

pip install requirements.txt
```

## Pi Zero Pin Diagram
![Pi Zero Pin Diagram](https://pi4j.com/1.2/images/j8header-zero.png)


## References
* Stable version(2.20) which I am using - https://github.com/python-escpos/python-escpos/tree/cbe38648f50dd42e25563bd8603953eaa13cb7f6
* Docs for this version - https://python-escpos.readthedocs.io/en/v2.2.0/
* GPIO Docs - https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
* https://www.programiz.com/python-programming/datetime/strftime
* https://github.com/PyramidTechnologies/Phoenix-ESC-POS
* Backup using Win32 Disk Imager https://www.howtogeek.com/341944/how-to-clone-your-raspberry-pi-sd-card-for-foolproof-backup/

### Espson references
https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=118#dle_eot
https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=124#gs_lr
https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=205
https://reference.epson-biz.com/modules/ref_escpos/index.php?content_id=185#dle_enq
