if [ `whoami` != "root" ] || [ "$UID" != 0 ]; then
  echo "I must be run with sudo."
  exit 1;
fi
apt-get install python3-smbus i2c-tools python3-rpi.gpio
echo -e 'i2c-dev' >> /etc/modules
modprobe -a i2c-dev
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
sed -i '$ i echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device' /etc/rc.local
sed -i '$ i hwclock -s' /etc/rc.local
hwclock -w

sudo cp /home/pi/x728-Monitor/x728Monitor.service  /etc/systemd/system/
sudo chmod u+rwx /etc/systemd/system/x728Monitor.service
sudo systemctl enable x728Monitor
