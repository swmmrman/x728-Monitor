# x728
Monitor for the x728 Pi UPS.
This will perform a safe shutdown after a specified timeout once the external is cut.
This is tested,and developed using Raspbian on a Raspberry Pi 4.
Currently it also works on a Raspberry Pi 3b+.  However this support will not be guaranteed.
Compatible device list is below.

Steps:
1.  Enable the ds1307 overlay, and i2c in the /boot/config.txt
  * add ds1307 to the dtoverlay line
    * dtoverlay=vc4-fkms-v3d,ds1307
  * Add/uncomment dtparam=i2c_arm=on.
2. reboot
3. Run sudo ./setup.sh
4. run with sudo ./x728-monitor.py or sudo python3 x728-monitor.py
5. Optional,  To start as a servive.  Stop any running instance, and run
  sudo systectl start x728Monitor.service
  or
  sudo service x728Monitor.service start
6. x728.conf can be copied to /etc/x728.conf, if not coppied the local copy will be used.  If altered, it should be done in /etc/x728.conf

To disable the service to prevent starting at boot, run
  sudo systemctl disable x728Monitor.service
  or
  sudo service x728Monitor.service disable



# Coming soon
* Config file support.
  * Allowing setting of board version.
  * Configurable shutdown time.


Compatible Devices
Computer | x728 version
-------- | -----------
Raspberry Pi 4B|v1.3,v2.0
Raspberry PI 3B+*|v1.3,v2.0

*Support in the future is not guaranteed.

Devices that are not compatible

NanoPi M4 all versions all x728s.
The libraries are not available, and the needed pins are 1.8v.
