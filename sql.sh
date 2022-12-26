#!/bin/bash

sudo apt install git
git clone https://github.com/thanhnguyen287/SQL-Vulnerable.git
cd SQL-Vulnerable
sudo apt-get install python3-pip -y
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install email_validator
sudo cp flask.service /etc/systemd/system/
chmod +x flask.sh
sudo systemctl enable flask.service
