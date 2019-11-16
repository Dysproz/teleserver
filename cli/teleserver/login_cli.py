import click
import getpass
from ipaddress import ip_network
import json
import logging
import netifaces
import requests
import os

from teleserver.utils.lookup_utils import parse_interface, find_teleserver


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
        exit(1)
    os.remove('~/.teleserver/credentials.json')
    logger.info('Loged out successful!')


@log.command('lookup_server')
@click.option('--interface', default=None, help='Interface to check. (default looks up all interfaces)')
@click.option('--network', default=None, help='Network to check. (default looks up all networks on interfaces)')
def lookup_server(interface, network):
    """Lookup IP of teleserver

    This command looks up for teleserver in specified network, networks attached to interface
    or networks attached to all system interfaces.

    Lookup works only for IPv4.
    """
    logger.info('Looking up for teleserver...')
    logger.debug(f'args: interface: {interface}, network: {network}')
    if interface and network:
        logger.error('Found both network and interface. Please provide only one of them')
        exit(1)

    if interface:
        if interface in netifaces.interfaces():
            iface = interface
        else:
            log.error(f'Error: Itnerface {interface} not found!')
            exit(1)
    else:
        iface = None
    if network:
        networks = [ip_network(network, strict=False)]
    else:
        if iface:
            networks = parse_interface(iface)
        else:
            all_ifaces = netifaces.interfaces()
            networks = []
            for ifce in all_ifaces:
                networks.extend(parse_interface(ifce))
    found_ips = find_teleserver(networks)
    logger.info(f'Got response from these IP addresses: {found_ips}')
