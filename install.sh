#! /bin/sh

# Installation of required apt packages
cat apt-requirements.txt | xargs sudo apt install -y
if [ $? -ne 0 ]; then
	echo "Could not install required packages. Please check your packages. Exitting..."
	exit 1
fi

# Chrome installation
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome*.deb
if [ $? -ne 0 ]; then
	echo "Could not install Chrome. Check your packaging manager. Exitting..."
	exit 1
fi
xdg-settings set default-web-browser google-chrome.desktop

# Installation of required pip packages
pip3 install requirements.txt
if [ $? -ne 0 ]; then
	echo "Could not install required pip packages. Exitting..."
	exit 1
fi

# Blocking autolock of screen
gsettings set org.gnome.desktop.screensaver lock-enabled false

# Setup of application files with respect to previous versions
sudo mkdir /var/lib/teleserver
sudo mkdir /var/lib/teleserver/data
rm -rf /var/lib/teleserver/app > /dev/null
sudo mkdir /var/lib/teleserver/data
sudo chmod +wrx /var/lib/teleserver/data
cp -rf $PWD /var/lib/teleserver/app/

# Adding teleserver trigger to user profile
if [[ $(grep -o "ccc" ~/.profile | wc -l) = 0 ]]; then
	echo "nohup python3 /var/lib/teleserver/app/run.py &" >> ~/.profile
fi

exit 0