#!/bin/sh

# Installation of required apt packages
cat apt-requirements.txt | xargs sudo apt install -y
if [ $? -ne 0 ]; then
	echo "Could not install required packages. Please check your packages. Exitting..."
	exit 1
fi

# Setup of application files with respect to previous versions
sudo mkdir /var/lib/teleserver_IoT
sudo rm -rf /var/lib/teleserver_IoT/app > /dev/null
sudo chmod -R 777 /var/lib/teleserver_IoT/
sudo cp -rf $PWD /var/lib/teleserver_IoT/app/
sudo chmod -R +x /var/lib/teleserver_IoT/app

# Setup cron job that will run every 5 minutes
crontab -l > mycron
echo "5 * * * * python3 /var/lib/teleserver_IoT/app/IoT_master_run.py" >> mycron
crontab mycron
rm mycron

echo "Teleserver IoT master has been installed successfully."
exit 0
