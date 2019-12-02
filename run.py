#!/usr/bin/python3
import dash
import dash_auth
from dash.dependencies import Input, Output, State
import flask
import inspect
import os
import datetime

from layouts.keyboard_layout import FLAT_KEYBOARD_KEYS, KEYBOARD_NAMES
from layouts.key_control_layout import SHORTCUT_NAMES, SHORTCUTS
from layouts.main_layout import gui_layout, tab_render
import tools.app_callbacks as callback
from tools.common import OPENMEET_var
from tools.secret_manager import SecretManager
from tools.calendar_generation import sendToGoogleCalendar
import tools.system_calls as system


sec = SecretManager()
VALID_USERNAME_PASSWORD_PAIRS = [sec.get_credentials()]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(
    __name__, server=server, external_stylesheets=external_stylesheets)
app.layout = gui_layout()
app.title = 'teleserver'
app.config['suppress_callback_exceptions'] = True
if VALID_USERNAME_PASSWORD_PAIRS != ['', '']:
    auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


@server.route('/openmeet')
def openmeet():
    system.web_open(OPENMEET_var)
    return 'Meet opened\n'


@server.route('/open', methods=['GET'])
def open():
    url = flask.request.args.get('url')
    system.web_open(url)
    return "url opened.\n"


@server.route('/close')
def close():
    system.close()
    return "closed\n"


@server.route('/poweroff')
def poweroff():
    system.poweroff()
    return "poweroff...\n"


@server.route('/reboot')
def reboot():
    system.reboot()
    return "reboot...\n"


@server.route('/screenshot')
def screenshot():
    system.screenshot()
    return "screenshot taken\n"


@server.route('/mute')
def mute():
    system.mute()
    return "muted\n"


@app.callback(
    Output('open-output-message', 'children'),
    [Input('url-button', 'n_clicks')], [State('url', 'value')])
def app_open(n_clicks, value):
    if n_clicks != 0:
        system.web_open(value)
    return u'opened'


@app.callback(
    Output('close-output-message', 'children'),
    [Input('url-close-button', 'n_clicks')])
def app_close(n_clicks):
    if n_clicks != 0:
        system.close()
    return u'closed'


@app.callback(
    Output('screenshot-output-message', 'children'),
    [Input('screenshot-button', 'n_clicks')])
def app_screenshot(n_clicks):
    if n_clicks != 0:
        system.screenshot()
    return u'screenshot taken'


@app.callback(
    Output('reboot-output-message', 'children'),
    [Input('reboot-button', 'n_clicks')])
def app_reboot(n_clicks):
    if n_clicks != 0:
        system.reboot()
        pass
    return u'reboot'


@app.callback(
    Output('poweroff-output-message', 'children'),
    [Input('poweroff-button', 'n_clicks')])
def app_poweroff(n_clicks):
    if n_clicks != 0:
        system.poweroff()
        pass
    return u'poweroff'


@app.callback(
    Output('volume-slider', 'value'), [Input('set-volume-button', 'n_clicks')],
    [State('volume-slider', 'value')])
def app_volume(n_clicks, value):
    if n_clicks != 0:
        system.volume(value)
    return value


@app.callback(
    Output('volume-indicator', 'children'), [Input('volume-slider', 'value')])
def app_volume_indicate(value):
    return u'Selected Value: {val} | System Volume: {sys}'\
            .format(val=value, sys=system.get_volume())


@app.callback(
    Output('mute-output-message', 'children'),
    [Input('mute-button', 'n_clicks')])
def app_mute(n_clicks):
    if n_clicks != 0:
        system.mute()
    return u'muted'


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    return tab_render(tab)


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')], [State('upload-data', 'filename')])
def upload_content(uploaded_file_contents, uploaded_filenames):
    return callback.upload(uploaded_filenames, uploaded_file_contents)


@app.callback(
    Output('download-files-output-message',
           'children'),
    [Input('download-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def download_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.download_files(files)
    return u'prepared'


@server.route('/download')
def download_flask():
    if os.path.exists('{}/teleserver_download.zip'.format(os.getcwd())):
        return flask.send_from_directory(os.getcwd(),
                                         'teleserver_download.zip')
    else:
        return u'No files selected'


@app.callback(
    Output('delete-files-output-message',
           'children'), [Input('delete-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def delete_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.delete_files(files)
    return u'deleted'


@app.callback(
    Output('open-files-output-message',
           'children'), [Input('open-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def open_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.open_files(files)
    return u'opened'


@app.callback(
    Output('custom-shortcut-output-message', 'children'),
    [Input('key-control-button', 'n_clicks')], [State('key-control', 'value')])
def key_control(clicks, value):
    if clicks > 0:
        system.xdotool_key(value)
    return u'executed'


@app.callback(
    Output('shortcut-output-message', 'children'),
    [Input(name, 'n_clicks_timestamp') for name in SHORTCUT_NAMES])
def shortcuts_click(*SHORTCUT_NAMES):
    frame = inspect.currentframe()
    _, _, _, values = inspect.getargvalues(frame)
    vals = [int(val) for val in values['SHORTCUT_NAMES']]
    last_clicked_value = max(vals)
    if last_clicked_value > 0:
        clicked_button = SHORTCUTS[vals.index(max(vals))]
        system.xdotool_key(clicked_button[1])
    return u'clicked'


@app.callback(
    Output('keyboard-output-message', 'children'),
    [Input(name, 'n_clicks_timestamp') for name in KEYBOARD_NAMES])
def keyboard_click(*KEYBOARD_NAMES):
    frame = inspect.currentframe()
    _, _, _, values = inspect.getargvalues(frame)
    vals = [int(val) for val in values['KEYBOARD_NAMES']]
    last_clicked_value = max(vals)
    if last_clicked_value > 0:
        clicked_button = FLAT_KEYBOARD_KEYS[vals.index(max(vals))]
        system.xdotool_key(clicked_button)
    return u'clicked'


@app.callback(
    Output('live-screen', 'children'),
    [Input('screen-interval-component', 'n_intervals')])
def grab_screen(n):
    return callback.get_screen_grab()


@app.callback(
    [Output('confirm-good', 'displayed'),
     Output('confirm-bad', 'displayed')],
    [Input('time-submit-button', 'n_clicks')],
    [State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('hour-slider', 'value'),
     State('minute-slider', 'value'),
     State('event-title', 'value')])
def pick_datetime(clicks, start_date, end_date, hours, minutes, title):
    if start_date is not None and end_date is not None and title is not None:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        if clicks != 0:
            result = sendToGoogleCalendar(start_date, end_date, hours, minutes, title)
        if result:
            return True, False
        else:
            return False, True


if __name__ == '__main__':
    server.run(debug=False, host='0.0.0.0', port=8080)
