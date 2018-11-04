'''
Flask server for teleserver
by Szymon Piotr Krasuski
2018
'''

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField
import webbrowser
from subprocess import call

# url to your favourite website (e.g. Google Meet)
OPENMEET_var = "http://www.google.com"


class urlForm(Form):
    url = TextField('')


app = Flask(__name__)


def urlChecker(url):
    if not url.startswith('http'):
        if url.startswith('www'):
            url = "http://" + url
        else:
            url = "http://www." + url
    return url


def gui_text_field_control(url):
    if url == 'close':
        system_close()
        return 0
    elif url.startswith('#'):
        if url == '#reboot':
            system_reboot()
            return 0
        elif url == '#poweroff':
            system_poweroff()
            return 0
        elif url == '#close':
            system_close()
            return 0
        elif url.startswith('#volume'):
            try:
                value = int(url[8:])
                if 0 <= value <= 100:
                    system_volume(value)
                    return 0
            except:
                pass
        elif url == '#mute':
            system_mute()
            return 0
        elif url == '#screenshot':
            system_screenshot()
            return 0
    return 1


###############################
######## System Calls #########
###############################


def system_close():
    call(["pkill", "chrome"])


def system_web_open(url):
    webbrowser.open(urlChecker(url), new=0)


def system_poweroff():
    call(['systemctl', 'poweroff', '-i'])


def system_reboot():
    call(['systemctl', 'reboot', '-i'])


def system_screenshot():
    call(['gnome-screenshot'])


def system_mute():
    call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%', 'unmute'])


def system_volume(volume):
    call(['amixer',
          '-D',
          'pulse',
          'set',
          'Master',
          str(volume)+'%',
          'unmute'])


def system_update():
    call(['/usr/local/teleserver/update.sh'])

###############################
########### Routes ############
###############################


@app.route('/openmeet')
def openmeet():
    system_web_open(OPENMEET_var)
    return 'Meet opened\n'


@app.route('/open', methods=['GET'])
def open():
    url = request.args.get('url')
    system_web_open(url)
    return "url opened.\n"


@app.route('/close')
def close():
    system_close()
    return "closed\n"


@app.route('/poweroff')
def poweroff():
    system_poweroff()
    return "poweroff...\n"


@app.route('/reboot')
def reboot():
    system_reboot()
    return "reboot...\n"


@app.route('/screenshot')
def screenshot():
    system_screenshot()
    return "screenshot taken\n"


@app.route('/mute')
def mute():
    system_mute()
    return "muted\n"


@app.route('/gui', methods=['GET', 'POST'])
def gui():
    form = urlForm(request.form)
    if request.method == 'POST':
        url = request.form['url']
        if request.form['action'] == "Submit":
            url_exit_code = gui_text_field_control(url)

            if url_exit_code == 1:
                if form.validate():
                    system_web_open(url)
                else:
                    flash('No URL')

        elif request.form['action'] == "Set Volume":
            vol = request.form['volume_slider']
            system_volume(vol)

        elif request.form['action'] == "Screenshot":
            system_screenshot()

        elif request.form['action'] == "Reboot":
            system_reboot()
            return "Rebooting...\n"

        elif request.form['action'] == "Power Off":
            system_poweroff()
            return "Powering off...\n"

        elif request.form['action'] == "Mute":
            system_mute()

        elif request.form['action'] == "Close":
            system_close()

        elif request.form['action'] == "Update":
            system_update()
            return "updating...\n"
    return render_template('cast.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
