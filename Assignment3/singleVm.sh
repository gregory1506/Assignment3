#!/bin/bash
# install python3-bottle 
apt-get -y update
apt-get -y install python3-pip
pip install azure-storage
chmod +x queue_load.py
python3 queue_load.py




