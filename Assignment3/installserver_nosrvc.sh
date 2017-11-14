#!/bin/bash
# install python3 stuff
apt-get -y update
apt-get -y install python3-bottle
apt-get -y install python3-pip
pip3 install azure-storage
pip3 install azure-servicebus
chmod +x workserver.py








