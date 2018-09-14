# Teleserver
### Control your ubuntu machine over Flask http server

## Intro
This is an ansible based tool to build http server on your ubuntu machine
which allows you to execute commands over web

## Install
To install server you'll need ansible.

If you have it already on your machine or know how to install it, just download system_setup.yml and run it with:
```
sudo ansible-playbook system_setup.yml
```
However, if you don't know what's going on, download install.sh ans run it.
It'll install ansible, download system_setup.yml and run it.

After reboot, all you need to do is to find IP address of your machine (for example with ifconfig).

The server is configured to start at the beginning of user sesison.

## How to use it?

Firstly, you need IP of your machine.
When you get it then all the 'commands' will begin with
```
<IP address>:8080
```
where 8080 is a port that machine's server operates on.

Basic usage is to open web browser on desired website.
The easy way out is to enter into web browser of computer from which you want to control your server
```
<IP address>:8080/gui
```
and enter the simple website.

This website contains one field where you can paste url to your desired website and click Submit to open that page.
If you want to close web browser (e.g. because your boss is about to come in), simply enter 'close' into the field.

Another way is to use curl (or just paste url to web browser):
```
<IP address>:8080/open?url='<url of your website>'
```

That'll open the page too.

```
<IP address>:8080/close
```
will close the browser.

Other commands that are accessible is poweroff and reboot

```
<IP address>:8080/reboot
```

```
<IP address>:8080/poweroff
```
that works exactly like inserting these commands into terminal.

There's one more command.
If you have your favourite website (for example link to Google Meet),
you can specify that link in /usr/local/teleserver/run.py under @app.route('/openmeet') function.
Afterwards entering

```
<IP address>:8080/openmeet
```
will open link specified by you.
By default it's linked to Google.

