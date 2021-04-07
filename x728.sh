#X728 RTC setting up
sudo sed -i '$ i rtc-ds1307' /etc/modules
sudo sed -i '$ i echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device' /etc/rc.local
sudo sed -i '$ i hwclock -s' /etc/rc.local
sudo sed -i '$ i #Start power management on boot' /etc/rc.local

#x728 Powering on /reboot /full shutdown through hardware
#!/bin/bash

    sudo sed -e '/shutdown/ s/^#*/#/' -i /etc/rc.local

sudo cp x728pwr.sh /etc/x728pwr.sh
sudo chmod +x /etc/x728pwr.sh
sudo sed -i '$ i /etc/x728pwr.sh &' /etc/rc.local


#X728 full shutdown through Software
#!/bin/bash

    sudo sed -e '/button/ s/^#*/#/' -i /etc/rc.local

    echo '#!/bin/bash

BUTTON=13

echo "$BUTTON" > /sys/class/gpio/export;
echo "out" > /sys/class/gpio/gpio$BUTTON/direction
echo "1" > /sys/class/gpio/gpio$BUTTON/value

SLEEP=${1:-4}

re='^[0-9\.]+$'
if ! [[ $SLEEP =~ $re ]] ; then
   echo "error: sleep time not a number" >&2; exit 1
fi

echo "X728 Shutting down..."
/bin/sleep $SLEEP

#restore GPIO 13
echo "0" > /sys/class/gpio/gpio$BUTTON/value
' > /usr/local/bin/x728softsd.sh
sudo chmod +x /usr/local/bin/x728softsd.sh

#X728 Battery voltage & precentage reading
#!/bin/bash

sudo sed -e '/shutdown/ s/^#*/#/' -i /etc/rc.local
cp x728.py ~/x728.py
sudo chmod +x /home/pi/x728bat.py

#X728 AC Power loss / power adapter failture detection
#!/bin/bash

    sudo sed -e '/button/ s/^#*/#/' -i /etc/rc.local

    echo '#!/usr/bin/env python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

def my_callback(channel):
    if GPIO.input(6):     # if port 6 == 1
        print "---AC Power Loss OR Power Adapter Failure---"
    else:                  # if port 6 != 1
        print "---AC Power OK,Power Adapter OK---"

GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)

print "1.Make sure your power adapter is connected"
print "2.Disconnect and connect the power adapter to test"
print "3.When power adapter disconnected, you will see: AC Power Loss or Power Adapter Failure"
print "4.When power adapter disconnected, you will see: AC Power OK, Power Adapter OK"

raw_input("Testing Started")
' > /home/pi/x728pld.py
sudo chmod +x /home/pi/x728pld.py
