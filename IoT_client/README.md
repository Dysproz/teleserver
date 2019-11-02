# teleserver IoT client

This is client for IoT devices to serve data with teleserver IoT master.

## Idea

The main idea behind this module it to provide full working API that may communicate with IoT master module (check the teleserver GitHub page).

API is supposed to serve data gathered from IoT devices - such as temperature, humidity or thermal camera image.

## Installation

In order to install IoT client run `install_IoT_client.sh` script.

At the end the script you will find information about token that should be saved to *clients.yml* file of IoT master tgoether with IP of client.
This informatino will be used to communicate with client.
