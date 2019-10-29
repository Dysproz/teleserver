import json
import os
import requests


def make_request(route=None, url_args=None, post_args={}):
    """This is helping function to make requests with token provided
    in ~/.teleserver/credentials.json

    All arguments provided as url args or as variables in POST will be
    added to request.

    :param route: Teleserver route to make request to.
                  (String in url after e.g. https://127.0.0.1:8080/)
    :type route: str
    :param url_args: Arguments key-value to attach to url
                     (basically arguments provided in url as ?var1=val1&var2=val2)
    :type url_args: dict
    :param post_args: Arguments key-value to provide ad POST variables.
    :type post_args: dict

    :return: response from teleserver
    :rtype: dict
    """
    if not os.path.isfile('~/.teleserver/credentials.json'):
        raise Exception('NO CREDENTIALS! Please first log in.')
    with open('~/.teleserver/credentials.json', 'r') as secret_file:
        secrets = json.load(secret_file)
        token = secrets['token']
        server = secrets['server']
    if not route:
        return {'message': 'None route specified', 'rc': 1}
    url = f'http://{server}:8080/{route}'
    if url_args:
        url += '?'
        for argname in url_args:
            url += f'{argname}={url_args[argname]}&'
        else:
            url = url[:-1]
    post_args['token'] = token
    response = requests.post(url=url, data=post_args)
    return response.json()
