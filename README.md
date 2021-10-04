# x728
Monitor for the x728 Pi UPS.
This will perform a safe shutdown after a specified timeout once the external is cut.
This is tested,and developed using Raspbian on a Raspberry Pi 4


Steps:
1.  Enable the ds1307 overlay, and i2c in the /boot/config.txt
  A. add ds1307 to the dtoverlay line
    ex. dtoverlay=vc4-fkms-v3d,ds1307
  B. Add/uncomment dtparam=i2c_arm=on.
2. reboot
3. Run sudo ./setup.sh
4. run with sudo ./x728-monitor.py or sudo ython3 x728-monitor.py
