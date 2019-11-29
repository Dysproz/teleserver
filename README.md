# Teleserver
### Control your ubuntu machine over Flask http server

<img src="https://github.com/Dysproz/teleserver/blob/master/images/logo.png" height="200" width="200">

## Intro
This is a client to open you ubuntu machine to local network and allow to control it over the web.

[![CircleCI](https://circleci.com/gh/Dysproz/teleserver/tree/master.svg?style=svg)](https://circleci.com/gh/Dysproz/teleserver/tree/master)
[![GitHub license](https://img.shields.io/github/license/Dysproz/teleserver.svg)](https://github.com/Dysproz/teleserver/blob/master/LICENSE)
[![Generic badge](https://img.shields.io/badge/ubuntu-18.04|18.10|19.04-e95420.svg)](https://[shields.io/](https://github.com/Dysproz/teleserver))
[![GitHub release](https://img.shields.io/github/release/Dysproz/teleserver.svg)](https://GitHub.com/Dysproz/Steleserver/releases/)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
# Install
In order to install teleserver clone project repo from github.
Afterwards, cd into project directory.

In order to install teleserver run script:
```
make install
```

This command will run script *install.sh*

After reboot or session restart, all you need to do is find IP address of your machine (for example with `ip a`).

The server is configured to start at the beginning of user sesison.

## Login feature

By default teleserver can be reached by anyone,
However, if you want to set password and login for GUI run this script:
```
/var/lib/teleserver/set_login_credentials.py
```

You'll be asked for login and password which later should be used for login on GUI.

[*If you didn't set login credentials and you are prompted for login już apply without entering any credentials.*]

# How to use it?

Firstly, you need IP of your machine.
When you get it then all the 'commands' will begin with
```
<IP address>:8080
```
where 8080 is a port that machine's server operates on.

## CLI interface
Basic usage is to open web browser on desired website remotely.

Use curl with this url (or just paste url to web browser):
```
<IP address>:8080/open?url='<url of your website>'
```

and

```
<IP address>:8080/close
```
will close the browser.

There's also reboot and poweroff:

```
<IP address>:8080/reboot
```

```
<IP address>:8080/poweroff
```
that works exactly as inserting these commands into terminal.
So:

```
<IP address>:8080/screenshot
```
will take a screenshot.


```
<IP address>:8080/mute
```
will mute computer.

There's one more command.
If you have your favourite website (for example Google Meet),
you can specify that link in /var/lib/teleserver/tools/common.py by changing OPENMEET_var to your website.

Afterwards

```
<IP address>:8080/openmeet
```
will open link specified by you.
By default it's linked to Google.
(Please be aware that after changing OPENMEET_var it's essential to restart server or simply reboot)

CLI interface may be convinient for automated apps that can't use GUI, but should operate somehow with teleserver.

## GUI
There's also GUI that covers features specified in previous paragraph and extends it to additional features.

![GUI](https://github.com/Dysproz/teleserver/blob/master/images/gui1.png)
![GUI](https://github.com/Dysproz/teleserver/blob/master/images/gui2.png)
![GUI](https://github.com/Dysproz/teleserver/blob/master/images/gui3.png)
![GUI](https://github.com/Dysproz/teleserver/blob/master/images/gui4.png)
![GUI](https://github.com/Dysproz/teleserver/blob/master/images/gui5.png)

In the top panel, you'll find simple text field where you can paste url that should appear on teleserver. Close button closes webbrowser.

In the bottom part of website you'll find some tabs that cover different types of features.

### System Options

In this tab are some buttons to control basic system options.

Slider allows to choose desired level of volume on teleserver.
Under the slider you'll find selected volume level with slider and current volume level set on teleserver.
With button *Set Volume* selected volume level will be applied on teleserver.
*Mute* button simply mutes the volume.

*Screenshot* button simply takes screenshot of teleserver screen and saves it to files (described in other paragraph).

*reboot* and *poweroff* buttons does the same as terminal commands with the same names.

### Files

Files is separate feature from teleserver that turns teleserver into mini file server.
By clicking on draging file into dashed area you upload file into teleserver that's visible in files list below.

By switching tabs you can download or delete files from list.

### Shortcuts

In this section user can execute some basic shortcuts to easily control web browser and windows active on teleserver.

There is also a textbox where user can write it's own command compatible with ```xdotool key``` command.
Ex.
```
super+h
```
Will execute clicking Super and h keys together which will result in minimalizing active window.

###

In this section user has on-screen keyboard that can be used to insert data on teleserver.
I works basically like normal keyboard.

There is also a textbox where user can insert commands compatible with ```xdotool key```
## Desk reservations in Google Calendar

In order to use a calendar feature you need a Google account and enabled API Calendar.
Here you can find more information about activating API Calendar:
![Link](https://developers.google.com/calendar)

Before you start using calendar, a configuration is needed. Configuration file is 
config.yml in /var/lib/teleserver/app directory.
There you have to provide iframe to display your calendar, path to a file with 
a api credentials and a calendarID.
Remember to put one space after name of the option in a file. 
Please do not change the order of options and do not put additional enters at the end 
of a file.

# Uninstall

In order to uninstall teleserver, run uninstall.sh script from teleserver project dir:
```
make uninstall
```

# Supported releases
* bionic (18.04)
* cosmic (18.10)
* disco (19.04)

