ROS2 package for RASA's new hand. Both C++ and Python in Single Package.

First, upload the firmware code in the Windows environment, and then run the launch file on the Ubuntu environment. I still don't know why I can't directly upload through WSL2 although I can give commands, but nevermind!

## WSL2 & USB Connection
I use `usbipd` to connect the USB on Windows environment to Ubuntu environment via WSL2.

```bash
usbipd list
```
```bash
usbipd usbipd attach --wsl --auto-attach --busid 1-2
```
Adjust the BUSID based on your case.

Next set the permissions on Ubuntu terminal:
```bash
lsusb
sudo chmod a+rw /dev/ttyUSB0
sudo usermod -a -G dialout $USER
```
Now everything is fine.