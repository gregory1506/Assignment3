#!/bin/bash
app_path=/srv/app
mkdir $app_path
cp *.py $app_path

# install python3 stuff
apt -y update
apt -y install python3-bottle
apt -y install python3-pip
pip3 install azure-storage
pip3 install azure-servicebus
pip3 install aiohttp

# create worker service
touch /etc/systemd/system/worker.service
printf '[Unit]\nDescription=worker Service\nAfter=rc-local.service\n' >> /etc/systemd/system/worker.service
printf '[Service]\nWorkingDirectory=%s\n' $app_path >> /etc/systemd/system/worker.service
printf 'ExecStart=/usr/bin/python3 %s/worker.py\n' $app_path >> /etc/systemd/system/worker.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/worker.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=worker.service' >> /etc/systemd/system/worker.service

# create server service
touch /etc/systemd/system/server.service
printf '[Unit]\nDescription=server Service\nAfter=rc-local.service\n' >> /etc/systemd/system/server.service
printf '[Service]\nWorkingDirectory=%s\n' $app_path >> /etc/systemd/system/server.service
printf 'ExecStart=/usr/bin/python3 %s/server.py\n' $app_path >> /etc/systemd/system/server.service
printf 'ExecReload=/bin/kill -HUP $MAINPID\nKillMode=process\nRestart=on-failure\n' >> /etc/systemd/system/server.service
printf '[Install]\nWantedBy=multi-user.target\nAlias=server.service' >> /etc/systemd/system/server.service

systemctl start worker
systemctl start server





