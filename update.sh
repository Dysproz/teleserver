#!/bin/sh
rm -rf /usr/local/teleserver/*
rm -rf /usr/local/teleserver/.git
git clone https://github.com/Dysproz/teleserver.git /usr/local/teleserver/
chmod 0777 /usr/local/teleserver/*
pkill -f teleserver
nohup python /usr/local/teleserver/run.py &
