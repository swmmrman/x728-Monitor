if [ `whoami` != "root" ] || [ $UID == 0 ]; then
  echo "I must be run with sudo."
  exit 1;
fi
echo -e 'i2c-dev' >> /etc/modules
modprobe -a i2c-dev
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
sed -i '$ i echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device' /etc/rc.local
