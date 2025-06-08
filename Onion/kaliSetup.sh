#!/bin/bash

service_name="Oignon"

#! This script is intended to be run on a Kali Linux system to set up a Tor hidden service with Nginx.
echo starting kaliSetup.sh
sudo apt-get update && sudo apt-get upgrade -y && sudo apt install vim -y


#! dl and start the nginx service
sudo apt install nginx -y && sudo systemctl enable nginx && sudo systemctl start nginx && sudo systemctl status nginx

#!ensure nginx is running
sudo systemctl restart nginx

#! dl and start the tor service
sudo apt install tor -y && sudo systemctl enable tor && sudo systemctl start tor && sudo systemctl status tor

#! making a new service directory for tor
sudo mkdir -p /var/lib/tor/$service_name
sudo chown -R debian-tor:debian-tor /var/lib/tor/$service_name
sudo chmod 700 /var/lib/tor/$service_name

#!modify your page here
sudo vim /var/www/html/index.html

#!configure torrc file
sudo vim /etc/tor/torrc 
#?delete the # in front of the following lines
    #HiddenServiceDir /var/lib/tor/hidden_service/
    #HiddenServicePort 80 127.0.1:80
#?add the following lines
    # HiddenServicePort 4242 127.0.1:4242
sudo /etc/init.d/tor restart

#!configure ssh to listen on port 4242
sudo vim /etc/ssh/sshd_config
#?add the following line
    # Port 4242


clear && sudo cat /var/lib/tor/$service_name/hostname
