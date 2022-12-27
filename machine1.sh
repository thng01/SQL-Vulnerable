#!/bin/bash

#Creating user
cd
touch scriptPasswd.sh
sudo echo "echo 'debian:123' | chpasswd" > scriptPasswd.sh
sudo chmod +x scriptPasswd.sh
sudo ./scriptPasswd.sh

touch scriptPasswdUser1.sh
sudo useradd -m -s /bin/bash knight
sudo echo "echo 'knight:@s3cur3mdp' | chpasswd" > scriptPasswdUser1.sh
sudo chmod +x scriptPasswdUser1.sh
sudo ./scriptPasswdUser1.sh
sudo su -c 'mkdir /home/knight/.ssh' user1
sudo su -c 'touch /home/knight/.ssh/known_hosts' user1
sudo su -c "echo '172.30.150.12 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJwpC+ZDI9efM4CE98bzlg1O349YvPjGXP9IRtkpi9JnAyxloN+hdXyljAuP0vCnUauxfbYC1QUlYM4QFLOiP5w=' > /home/knight/.ssh/known_hosts" knight

sudo systemctl enable ssh
sudo apt-get install make

# les commandes de la partie Wordpress
##############################################################################################################
# I) Tools of WP
# Installation de docker 
sudo apt-get remove docker docker-engine docker.io containerd runc 
#Install using the repository
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release -y
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose -y
sudo docker run hello-world

#from wordpress on github
sudo git clone https://github.com/mouhssineEL/wordpress-docker-compose.git
sudo cd wordpress-docker-compose 
sudo chown $USER /var/run/docker.sock 
sudo cd wordpress-docker-compose
make autoinstall

#Onion web Sqli
cd
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

#Webshell login PGP
sudo cp msg /wordpress_docker/wordpress
sudo cp public /wordpress_docker/wordpress
sudo cp private /wordpress_docker/wordpress

#Hint for next machine
sudo su -c "echo 'tomy{8f3dbcbb884d161fb6eade138ed8c32e}' > /home/knight/flag4.txt" knight
sudo chmod 600 /home/knight/flag4.txt
sudo su -c "echo 'bishop - 02719440e19a8e087f16d1124defc9ace9e29b29' > /home/knight/login.txt" knight
sudo chmod 600 /home/knight/flag4.txt
#Remove scripts
cd 
sudo rm scriptPasswdUser1.sh
sudo rm scriptPasswd.sh
sudo rm machine1.sh*
