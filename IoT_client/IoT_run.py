#!/usr/bin/python3
import flask

from data_drainer import get_data_for_variable

server = flask.Flask(__name__)


@server.route('/healthcheck')
def healthcheck():
    return 'OK'


@server.route('/get/<variable>', methods=['GET'])
def get_variable(variable):
    return get_data_for_variable(variable)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
