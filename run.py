#!/usr/bin/python3
import dash
import dash_auth
from dash.dependencies import Input, Output, State
import flask
from flask import jsonify
from functools import wraps
import inspect
import jwt
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
VALID_USERNAME_PASSWORD_PAIRS = sec.get_credentials_for_GUI()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
server.config['SECRET_KEY'] = sec.get_secret_key()
app = dash.Dash(
    __name__, server=server, external_stylesheets=external_stylesheets)
app.layout = gui_layout()
app.title = 'teleserver'
app.config['suppress_callback_exceptions'] = True
if VALID_USERNAME_PASSWORD_PAIRS != {}:
    auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


def token_required(f):
    """This is a decorator to verify whether API user provided valid token
    Token is required to operate through API

    :param f: Function to decorate
    :type f: function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """Wrapper to parser token argument,
        check whether token is correct
        and return unchanged function when correct
        """
        url_args = flask.request.args.to_dict()
        post_args = flask.request.form.to_dict()
        if 'token' in url_args:
            token = url_args['token']
        elif 'token' in post_args:
            token = post_args['token']
        else:
            return jsonify({'message': 'Token is missing!'})

        try:
            jwt.decode(token, server.config['SECRET_KEY'])
        except jwt.exceptions.JWSDecodeError:
            return jsonify({'message': 'Token is invalid!'})
        return f(*args, **kwargs)
    return decorated


@server.route('/healthcheck')
def healthcheck():
    """This route is designed to check whether server is health
    """
    return jsonify({'message': 'Server is health', 'rc': 0})


@server.route('/login', methods=['GET', 'POST'])
def login():
    data = flask.request.form.to_dict()
    return jsonify(sec.create_time_token(data))


@server.route('/logout', methods=['GET', 'POST'])
def logout():
    data = flask.request.form.to_dict()
    return jsonify(sec.delete_time_token(data))


@server.route('/webbrowser/openmeet', methods=['GET', 'POST'])
@token_required
def API_openmeet():
    system.web_open(OPENMEET_var)
    return jsonify({'message': 'Meet opened', 'rc': 0})


@server.route('/webbrowser/open', methods=['GET', 'POST'])
@token_required
def API_open():
    url = flask.request.args.get('url')
    system.web_open(url)
    return jsonify({'message': 'URL opened', 'rc': 0})


@server.route('/webbrowser/close', methods=['GET', 'POST'])
@token_required
def API_close():
    system.close()
    return jsonify({'message': 'Webbrowser closed', 'rc': 0})


@server.route('/system/poweroff', methods=['GET', 'POST'])
@token_required
def API_poweroff():
    system.poweroff()
    return jsonify({'message': 'Machine is powering off...', 'rc': 0})


@server.route('/system/reboot', methods=['GET', 'POST'])
@token_required
def API_reboot():
    system.reboot()
    return jsonify({'message': 'Machine is rebooting', 'rc': 0})


@server.route('/system/screenshot', methods=['GET', 'POST'])
@token_required
def API_screenshot():
    system.screenshot()
    return jsonify({'message': 'Screenshot taken', 'rc': 0})


@server.route('/system/mute', methods=['GET', 'POST'])
@token_required
def API_mute():
    system.mute()
    return jsonify({'message': 'Volume muted', 'rc': 0})


@server.route('/system/grab_screen', methods=['GET', 'POST'])
@token_required
def API_grab_screen():
    return jsonify({'message': 'screen grabbed',
                    'rc': 0,
                    'screen': system.get_screen()})


@server.route('/system/set_volume', methods=['GET', 'POST'])
@token_required
def API_set_volume():
    level = flask.request.args.get('lvl')
    try:
        level = int(level)
    except ValueError:
        return jsonify({'message': f'ERROR: {level} is not int!', 'rc': 1})
    if not level <= 100 and not level >= 0:
        return jsonify({'message': f'ERROR: {level} is not in range 0-100', 'rc': 1})
    system.volume(level)
    return jsonify({'message': f'Volume set to {level}', 'rc': 0})


@server.route('/keyboard/call_key', methods=['GET', 'POST'])
@token_required
def API_call_key():
    key = flask.request.args.get('key')
    system.xdotool_key(key)
    return jsonify({'message': 'key called', 'rc': 0})


@server.route('/keyboard/call_word', methods=['GET', 'POST'])
@token_required
def API_call_word():
    word = flask.request.args.get('word')
    system.type_keyboard(word)
    return jsonify({'message': 'word called', 'rc': 0})


@app.callback(
    Output('open-output-message', 'children'),
    [Input('url-button', 'n_clicks')], [State('url', 'value')])
def GUI_app_open(n_clicks, value):
    if n_clicks != 0:
        system.web_open(value)
    return u'opened'


@app.callback(
    Output('close-output-message', 'children'),
    [Input('url-close-button', 'n_clicks')])
def GUI_app_close(n_clicks):
    if n_clicks != 0:
        system.close()
    return u'closed'


@app.callback(
    Output('screenshot-output-message', 'children'),
    [Input('screenshot-button', 'n_clicks')])
def GUI_app_screenshot(n_clicks):
    if n_clicks != 0:
        system.screenshot()
    return u'screenshot taken'


@app.callback(
    Output('reboot-output-message', 'children'),
    [Input('reboot-button', 'n_clicks')])
def GUI_app_reboot(n_clicks):
    if n_clicks != 0:
        system.reboot()
        pass
    return u'reboot'


@app.callback(
    Output('poweroff-output-message', 'children'),
    [Input('poweroff-button', 'n_clicks')])
def GUI_app_poweroff(n_clicks):
    if n_clicks != 0:
        system.poweroff()
        pass
    return u'poweroff'


@app.callback(
    Output('volume-slider', 'value'), [Input('set-volume-button', 'n_clicks')],
    [State('volume-slider', 'value')])
def GUI_app_volume(n_clicks, value):
    if n_clicks != 0:
        system.volume(value)
    return value


@app.callback(
    Output('volume-indicator', 'children'), [Input('volume-slider', 'value')])
def GUI_app_volume_indicate(value):
    return u'Selected Value: {val} | System Volume: {sys}'\
            .format(val=value, sys=system.get_volume())


@app.callback(
    Output('mute-output-message', 'children'),
    [Input('mute-button', 'n_clicks')])
def GUI_app_mute(n_clicks):
    if n_clicks != 0:
        system.mute()
    return u'muted'


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def GUI_render_content(tab):
    return tab_render(tab)


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')], [State('upload-data', 'filename')])
def GUI_upload_content(uploaded_file_contents, uploaded_filenames):
    return callback.upload(uploaded_filenames, uploaded_file_contents)


@app.callback(
    Output('download-files-output-message',
           'children'),
    [Input('download-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def GUI_download_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.download_files(files)
    return u'prepared'


@server.route('/download')
def GUI_download_flask():
    if os.path.exists('{}/teleserver_download.zip'.format(os.getcwd())):
        return flask.send_from_directory(os.getcwd(),
                                         'teleserver_download.zip')
    else:
        return u'No files selected'


@app.callback(
    Output('delete-files-output-message',
           'children'), [Input('delete-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def GUI_delete_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.delete_files(files)
    return u'deleted'


@app.callback(
    Output('open-files-output-message',
           'children'), [Input('open-files-button', 'n_clicks')],
    [State('files-checklist', 'value')])
def GUI_open_selected_files(n_clicks, files):
    if n_clicks != 0:
        callback.open_files(files)
    return u'opened'


@app.callback(
    Output('custom-shortcut-output-message', 'children'),
    [Input('key-control-button', 'n_clicks')], [State('key-control', 'value')])
def GUI_key_control(clicks, value):
    if clicks > 0:
        system.xdotool_key(value)
    return u'executed'


@app.callback(
    Output('native-shortcut-output-message', 'children'),
    [Input('native-key-control-button', 'n_clicks')], [State('native-key-control', 'value')])
def GUI_native_key_control(clicks, value):
    if clicks > 0:
        system.type_keyboard(value)
    return u'executed'


@app.callback(
    Output('shortcut-output-message', 'children'),
    [Input(name, 'n_clicks_timestamp') for name in SHORTCUT_NAMES])
def GUI_shortcuts_click(*SHORTCUT_NAMES):
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
def GUI_keyboard_click(*KEYBOARD_NAMES):
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
def GUI_grab_screen(n):
    return callback.get_screen_grab()


@app.callback(
    Output('service-principal-output-message', 'children'),
    [Input('service-principal-button', 'n_clicks')])
def GUI_generate_service_principal(clicks):
    if clicks > 0:
        return sec.create_service_principal()
    else:
        return ''


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
    server.run(debug=False, host='0.0.0.0', port=8080, ssl_context='adhoc')
