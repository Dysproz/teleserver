#!/bin/sh

# Installation of required apt packages
cat apt-requirements.txt | xargs sudo apt install -y
if [ $? -ne 0 ]; then
	echo "Could not install required packages. Please check your packages. Exitting..."
	exit 1
fi

# Chrome installation
FILE=google-chrome-stable_current_amd64.deb
if ! test -f "$FILE"; then
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
fi
sudo dpkg -i $FILE
if [ $? -ne 0 ]; then
	echo "Could not install Chrome. Check your packaging manager. Exitting..."
	exit 1
fi
xdg-settings set default-web-browser google-chrome.desktop

# Installation of required pip packages
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
	echo "Could not install required pip packages. Exitting..."
	exit 1
fi

# Blocking autolock of screen
gsettings set org.gnome.desktop.screensaver lock-enabled false

# Setup of application files with respect to previous versions
sudo mkdir /var/lib/teleserver
sudo chmod 777 /var/lib/teleserver
sudo mkdir /var/lib/teleserver/data
sudo rm -rf /var/lib/teleserver/app > /dev/null
sudo mkdir /var/lib/teleserver/data
sudo chmod 777 /var/lib/teleserver/data
sudo chmod -R +wx /var/lib/teleserver/app
sudo cp -rf $PWD /var/lib/teleserver/app/
sudo chmod -R +x /var/lib/teleserver/app
sudo chmod 777 /var/lib/teleserver/app/config_teleserver.yml


# Enable port 8080 in firewall
sudo ufw allow 8080

# Adding teleserver trigger to user profile
if [ $(grep -o "teleserver" ~/.profile | wc -l) = 0 ]; then
	echo "nohup python3 /var/lib/teleserver/app/run.py &" >> ~/.profile
fi

echo "Teleserver has been installed successfully. Now, restart your session to enjoy teleserver."
exit 0
