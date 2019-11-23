#!/usr/bin/python3
import argparse
import flask
from flask import jsonify
from functools import wraps
import jwt


from data_drainer import get_data_for_variable, set_data_for_variale
from secret_manager import SecretManager


server = flask.Flask(__name__)
sec = SecretManager()
server.config['SECRET_KEY'] = sec.get_secret_key()


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
        post_args = flask.request.form.to_dict()
        if 'token' in post_args:
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


@token_required
@server.route('/get/<variable>', methods=['GET', 'POST'])
def get_variable(variable):
    """This route serves IoT devices data from server
    """
    return jsonify({'data': get_data_for_variable(variable),
                    'rc': 0,
                    'message': 'Data gathered successfully'})


@server.route('/demo/set', methods=['GET', 'POST'])
def get_variable(variable):
    """This route serves IoT devices data from server
    """
    if demo:
        data = flask.request.args
        set_data_for_variale(data)
    else:
        return jsonify({'rc': 1,
                        'message': 'Server not working in demo state'})


def parse_arguments():
        parser = argparse.ArgumentParser(description='Server run options')
        parser.add_argument('--demo', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    demo = args.demo
    server.run(host='0.0.0.0', port=8080)
