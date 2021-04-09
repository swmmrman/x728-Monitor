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
cp x728.py /home/$(whoami)/x728batt.py
chmod +x /home/$(whoami)/x728batt.py

#X728 AC Power loss / power adapter failture detection
#!/bin/bash

    sudo sed -e '/button/ s/^#*/#/' -i /etc/rc.local

cp x728pld.py  /home/$(whoami)/x728pld.py
chmod +x /home/$(whoami)/x728pld.py
