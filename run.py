import tools.system_calls as system
import flask
import dash
import tools.classic_gui_functions as classic_gui
from tools.dash_gui import gui_layout
from dash.dependencies import Input, Output, State


OPENMEET_var = "http://www.google.com"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets)
app.layout = gui_layout()
app.config['suppress_callback_exceptions'] = True


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


@server.route('/update')
def update():
    system.update()
    return "updating...\n"


@server.route('/classic_gui', methods=['GET', 'POST'])
def gui():
    return classic_gui.gui_web()


@app.callback(Output('open-output-message', 'children'),
              [Input('url-button', 'n_clicks')],
              [State('url', 'value')])
def app_open(n_clicks, value):
    if n_clicks != 0:
        system.web_open(value)
    return u'opened'


@app.callback(Output('close-output-message', 'children'),
              [Input('url-close-button', 'n_clicks')])
def app_close(n_clicks):
    if n_clicks != 0:
        system.close()
    return u'closed'


@app.callback(Output('screenshot-output-message', 'children'),
              [Input('screenshot-button', 'n_clicks')])
def app_screenshot(n_clicks):
    if n_clicks != 0:
        system.screenshot()
    return u'screenshot taken'


@app.callback(Output('reboot-output-message', 'children'),
              [Input('reboot-button', 'n_clicks')])
def app_reboot(n_clicks):
    if n_clicks != 0:
        system.reboot()
        pass
    return u'reboot'


@app.callback(Output('poweroff-output-message', 'children'),
              [Input('poweroff-button', 'n_clicks')])
def app_poweroff(n_clicks):
    if n_clicks != 0:
        system.poweroff()
        pass
    return u'poweroff'


@app.callback(Output('volume-slider', 'value'),
              [Input('set-volume-button', 'n_clicks')],
              [State('volume-slider', 'value')])
def app_volume(n_clicks, value):
    if n_clicks != 0:
        system.volume(value)
    return value


@app.callback(Output('volume-indicator', 'children'),
              [Input('volume-slider', 'value')])
def app_volume_indicate(value):
    return u'Selected Value: {val} | System Volume: {sys}'\
            .format(val=value, sys=system.get_volume())


@app.callback(Output('mute-output-message', 'children'),
              [Input('mute-button', 'n_clicks')])
def app_mute(n_clicks):
    if n_clicks != 0:
        system.mute()
    return u'muted'


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
