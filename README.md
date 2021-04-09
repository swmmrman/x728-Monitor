# x728
setup scripts for x728


Steps:
1.  Enable the ds1307 overlay, and i2c in the /boot/config.txt
  A. add ds1307 to the dtoverlay line
    ex. dtoverlay=vc4-fkms-v3d,ds1307
  B. Add/uncomment dtparam=i2c_arm=on.

2. reboot

2.  Install python3-smbus and i2c-tools
  A. sudo apt install python3-smbus i2c-tools

3. Install rpi.gpio

5. Run sudo ./setup.sh
10. reboot


Install python3-smbus,python3-rpi.gpio
