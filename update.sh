#!/usr/bin/env bash
if [ `whoami` != "root" ] || [ "$UID" != 0 ]; then
  echo "I must be run with sudo."
  exit 1;
fi

cp x728-monitor.py /usr/bin/
systemctl restart x728Monitor.service
