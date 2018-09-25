# Teleserver
### Control your ubuntu machine over Flask http server

## Intro
This is an ansible based tool to build http server on your ubuntu machine
which allows you to execute commands over web.

## Install
In order to install server you'll need ansible.

If you have it already installed on your machine or you know how to install it, just download system_setup.yml and run it with:
```
sudo ansible-playbook system_setup.yml
```
However, if you don't know what's going on, download install.sh ans run it as sudo.
It'll install ansible, download system_setup.yml and run it.

After reboot, all you need to find IP address of your machine (for example with ifconfig).

The server is configured to start at the beginning of user sesison.

## How to use it?

Firstly, you need IP of your machine.
When you get it then all the 'commands' will begin with
```
<IP address>:8080
```
where 8080 is a port that machine's server operates on.

Basic usage is to open web browser on desired website remotely.
The easy way is to enter 
```
<IP address>:8080/gui
```
into your web browser's url bar.

This website contains one field where you can paste url to your desired website and click Submit to open that page.
If you want to close web browser (e.g. because your boss is about to come in), simply enter 'close' or '#close' into the field.

Other commands available via field:
```
#reboot
#poweroff
#mute
#volume=X # where X is a percentage value of volume
#screenshot
```

Another way is to use curl (or just paste url to web browser):
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

## Updates

In order to update this application, run again system_setup.yml playbook.
Asnible will automatically skip installation of required packages and will download latest version of app to /usr/local/teleserver.
