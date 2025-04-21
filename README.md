ROS2 package for RASA's new hand. Both C++ and Python in Single Package.

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