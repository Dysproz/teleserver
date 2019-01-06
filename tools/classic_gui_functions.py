from flask import render_template, flash, request
from wtforms import Form, TextField
import tools.system_calls as system


class urlForm(Form):
    url = TextField('')


def gui_text_field_control(url):
    if url == 'close':
        system.close()
        return 0
    elif url.startswith('#'):
        if url == '#reboot':
            system.reboot()
            return 0
        elif url == '#poweroff':
            system.poweroff()
            return 0
        elif url == '#close':
            system.close()
            return 0
        elif url.startswith('#volume'):
            try:
                value = int(url[8:])
                if 0 <= value <= 100:
                    system.volume(value)
                    return 0
            except TypeError:
                pass
        elif url == '#mute':
            system.mute()
            return 0
        elif url == '#screenshot':
            system.screenshot()
            return 0
    return 1


def gui_web():
    form = urlForm(request.form)
    if request.method == 'POST':
        url = request.form['url']
        if request.form['action'] == "Submit":
            url_exit_code = gui_text_field_control(url)

            if url_exit_code == 1:
                if form.validate():
                    system.web_open(url)
                else:
                    flash('No URL')

        elif request.form['action'] == "Set Volume":
            vol = int(request.form['volume_slider'])
            system.volume(vol)

        elif request.form['action'] == "Screenshot":
            system.screenshot()

        elif request.form['action'] == "Reboot":
            system.reboot()
            return "Rebooting...\n"

        elif request.form['action'] == "Power Off":
            system.poweroff()
            return "Powering off...\n"

        elif request.form['action'] == "Mute":
            system.mute()

        elif request.form['action'] == "Close":
            system.close()
    return render_template('cast.html', form=form)
