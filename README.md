# Teleserver
### Control your ubuntu machine over Flask http server

## Intro
This is an ansible based tool to build http server on your ubuntu machine
which allows you to execute commands over web.

# Install
In order to install server you'll need ansible.

If you have it already installed on your machine or you know how to install it, just download systemSetup.yml and run it with:
```
sudo ansible-playbook systemSetup.yml
```
However, if you don't know what's going on, download *install.sh* ans run it as sudo.
It'll install ansible, download *systemSetup.yml* and run it.

After reboot, all you need to find IP address of your machine (for example with ifconfig).

The server is configured to start at the beginning of user sesison.

## Login feature

By default teleserver can be reached by anyone,
However, if you want to set password and login for GUI run this script:
```
python3 /usr/local/teleserver/set_login_credentials.py
```

You'll be asked for login and password which later should be used for login on GUI.

[If you didn't set login credentials and you are prompted for login już apply without entering any credentials.]

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
you can specify that link in /usr/local/teleserver/run.py by changing OPENMEET_var to your website.

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

In the top panel, you'll find simple text field where you can paste url that should appear on teleserver. Close button closes webbrowser.

In the bottom part of website you'll find some tabs that cover different types of features.

### System Options

In this tab are some buttons to control basic system options.

Slider allows to choose desired level of volume on teleserver.
Under the slider you'll find selected colume level with slider and current volume level set on teleserver.
With button *Set Volume* selected volume level will be applied on teleserver.
*Mute* button simply mutes the volume.

*Screenshot* button simply takes screenshot of teleserver screen and saves it to files (described in other paragraph).

*reboot* and *poweroff* buttons does the same as terminal commands with the same names.

### Files

Files is separate feature from teleserver that turns teleserver into mini file server.
By clicking on draging file into dashed area you upload file into teleserver that's visible in files list below.

By switching tabs you can download or delete files from list.
# Uninstall

In order to uninstall teleserver, run ansible script /usr/local/teleserver/uninstall.yml.
```
sudo ansible-playbook /usr/local/teleserver/uninstall.yml
```
