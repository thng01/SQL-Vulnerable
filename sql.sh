#!/bin/bash

sudo apt install git
git clone https://github.com/thanhnguyen287/SQL-Vulnerable.git
cd SQL-Vulnerable
sudo apt get install python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install -r requirement.txt
python3 -m pip install email_validator
