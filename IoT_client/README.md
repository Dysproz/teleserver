# teleserver IoT client

This is client for IoT devices to serve data with teleserver IoT master.

## Idea

The main idea behind this module it to provide full working API that may communicate with IoT master module (check the teleserver GitHub page).

API is supposed to serve data gathered from IoT devices - such as temperature, humidity or thermal camera image.

## Installation

In order to install IoT client run `install_IoT_client.sh` script.

At the end the script you will find information about token that should be saved to *clients.yml* file of IoT master tgoether with IP of client.
This informatino will be used to communicate with client.

## Usage

**THIS IS ONLY DEMO CODE**
Currently, client has route to gather any variable via route */get/<variable>*. If variable exists in YAML file /var/lib/teleserver_IoT/data.yml then it's value will be returned. Otherwise, message with return code 1 will be returned.

*IoT_run.py* script has flag `--demo` which starts client in demo state. Demo state means that user can set value of any variable with route */demo/set* and providing variable name with value as URL argument (e.g. */demo/set?myvar=myval* will set variable *myvar* to *myval* value).

In order to connect real sensor (e.g. thermal sensor or moisture sensor) contact application creators or try to implement your own logic in *data_drainer.py* file. With proper mechanism of gathering data from sensors teleserver will provide all other necessary mechanism to secure communication with IoT master.
