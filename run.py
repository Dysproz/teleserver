'''
Flask server for teleserver
by Szymon Piotr Krasuski
2018
'''

from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import webbrowser
from subprocess import call

# url to your favourite website (e.g. Google Meet)
OPENMEET_var = "http://www.google.com"

# Form class for GUI purposes
class urlForm(Form):
    url = TextField('')

app = Flask(__name__)


# Method for providing full url (with http:// and www.)
def urlChecker(url):
   
    if not url.startswith('http'):
        if url.startswith('www'):
            url = "http://" + url
        else:
            url = "http://www." + url
    
    return url

# Method for interpreting different url codes from text field
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

# Close Google Chrome
def system_close():
    call(["pkill", "chrome"])

# Open url in web browser
def system_web_open(url):
    webbrowser.open(urlChecker(url), new=0)

# Power off computer
def system_poweroff():
    call(['systemctl', 'poweroff', '-i'])

# Reboot computer
def system_reboot():
    call(['systemctl', 'reboot', '-i'])

# Take screenshot
def system_screenshot():
    call(['gnome-screenshot'])

# Mute
def system_mute():
    call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%', 'unmute'])

# Set volume to <volume>%
def system_volume(volume):
    call(['amixer', '-D', 'pulse', 'sset', 'Master', str(volume)+'%', 'unmute'])

###############################
########### Routes ############
###############################


# Open predefined google meet webpage
@app.route('/openmeet')
def openmeet():
    system_web_open(OPENMEET_var)
    return 'Meet opened\n'

# Open any page provided as url argument (/open?url="<your-url>")
@app.route('/open', methods=['GET'])
def open():
    url = request.args.get('url')
    system_web_open(url)
    return "url opened.\n"

# Close web browser
@app.route('/close')
def close():
    system_close()
    return "closed\n"

# Method for powering off computer
@app.route('/poweroff')
def poweroff():
    system_poweroff()
    return "poweroff...\n"

# Method for rebooting computer
@app.route('/reboot')
def reboot():
    system_reboot()
    return "reboot...\n"

# Method for powering off computer
@app.route('/screenshot')
def screenshot():
    system_screenshot()
    return "screenshot taken\n"

# Method for muting computer
@app.route('/mute')
def mute():
    system_mute()
    return "muted\n"


# GUI webpage - graphical implementation of teleserver
@app.route('/gui', methods=['GET','POST'])
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

        elif request.form['action'] == "Power Off":
            system_poweroff()

        elif request.form['action'] == "Mute":
            system_mute()

       
        
    return render_template('cast.html', form=form)


# Define server to be available on broadcast via port 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
