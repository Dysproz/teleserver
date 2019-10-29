import click
import getpass
import json
import logging
import requests
import os

logger = logging.getLogger(__name__)


def convert_time_unit_to_variables(time):
    time_value = time[:-1]
    units = {'d': 0,
             'h': 1,
             'm': 2,
             's': 3}
    target_unit = units[time[-1]]
    output = [0, 0, 0, 0]
    output[target_unit] = time_value
    return tuple(output)


@click.group()
def log():
    """Create or delete login token
    """
    pass


@log.command('in')
@click.option('--username', default=None, help='Username registered in GUI')
@click.option('--lease', default='30m', help='Lease time for token. Format: <number><time unit> where time unit'
                                             'is "d" for days, "h" for hours, "m" for minutes, "s" for seconds')
@click.option('--server', default='127.0.0.1', help='IP of teleserver')
def login_in(username, lease, server):
    """Log into teleserver

    This command will send request to teleserver to create login token
    and will save token under ~/.teleserver/credentials.json
    """
    logger.info('Started loggin in process.')
    logger.debug("args: username: {username}, lease: {lease}, server: {server}")
    if username is None:
        logger.error('Username was not provided')
        return
    else:
        p = getpass.getpass('Please enter password: ', stream=None)
        lease_days, lease_hours, lease_minutes, lease_seconds = convert_time_unit_to_variables(lease)
        response = requests.post(url=f'http://{server}:8080/login', data={'user': username, 'password': p,
                                                                          'lease_days': lease_days,
                                                                          'lease_hours': lease_hours,
                                                                          'lease_minutes': lease_minutes,
                                                                          'lease_seconds': lease_seconds})
        if int(response.json()['rc']) != 0:
            error_message = response.json()['message']
            logger.error(f'Error while loggin in: {error_message}')
            return
        else:
            token_name = response.json()['name']
            token = response.json()['token']
            credentials_data = {'token_name': token_name,
                                'token': token,
                                'server': server}
            os.makedirs('~/.teleserver')
            with open('~/.teleserver/credentials.json', 'w') as credentials_file:
                json.dump(credentials_data, credentials_file)
            logger.info('Log in successful!')


@log.command('out')
def login_out():
    """Log out from teleserver

    This command will call teleserver to delete saved token
    and delete file with credentials.
    """
    logger.info('Logging out...')
    with open('~/.teleserver/credentials.json', 'r') as secret_file:
        data = json.load(secret_file)
        token_name = data['token_name']
        server = data['server']
    response = requests.post(url=f'http://{server}:8080/logout', data={'token_name': token_name})
    if int(response.json()['rc']) != 0:
        error_message = response.json()['message']
        logger.error(f'Error while deleting token: {error_message}')
        return
    os.remove('~/.teleserver/credentials.json')
    logger.info('Loged out successful!')
