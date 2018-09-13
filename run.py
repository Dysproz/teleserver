from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import webbrowser
from subprocess import call

# Form class for GUI purposes
class urlForm(Form):
    url = TextField('URL', validators=[validators.required()])

app = Flask(__name__)


# Method for providing full url (with http:// and www.)
def urlChecker(url):
   
    if not url.startswith('http'):
        if url.startswith('www'):
            url = "http://" + url
        else:
            url = "http://www." + url
    
    return url

# Open predefined google meet webpage
@app.route('/openmeet')
def openmeet():
    webbrowser.open("http://www.google.com", new=0)
    return 'Meet opened\n'

# Open any page provided as url argument (/open?url="<your-url>")
@app.route('/open', methods=['GET'])
def open():
    url = request.args.get('url')
    webbrowser.open(urlChecker(url), new=0)
    return "url opened.\n"

# Close web browser
@app.route('/close')
def close():
    call(["pkill", "chrome"])
    return "Closed\n"

# GUI webpage - graphical implementation of /open and /close. Entering 'close'as url closes web browser
@app.route('/gui', methods=['GET', 'POST'])
def gui():
    form = urlForm(request.form)
    if request.method == 'POST':
        url = request.form['url']
        if url == 'close':
            call(["pkill", "chrome"])
        else:
            if form.validate():
                webbrowser.open(urlChecker(url), new=0)
            else:
                flash('No URL')
    return render_template('cast.html', form=form)

# Method for powering off computer
@app.route('/poweroff')
def poweroff():
    call(["poweroff"])
    return "poweroff...\n"

# Method for rebooting computer
@app.route('/reboot')
def reboot():
    call(["reboot"])
    return "reboot...\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
