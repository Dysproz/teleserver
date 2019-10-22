#!/bin/sh

# Kill teleserver process
pkill -f teleserver

# Remove project files
sudo rm -rf /var/lib/teleserver

# Remove teleserver from profile
sed -i '/teleserver/d' ~/.profile
