import tools.system_calls as system
import flask
import dash
import dash_html_components as html
import tools.classic_gui_functions as classic_gui

OPENMEET_var = "http://www.google.com"

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.layout = html.Div(children=['...'])


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


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
