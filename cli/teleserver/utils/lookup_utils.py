from ipaddress import ip_network, ip_address
import json
import logging
import multiprocessing
import netifaces
import requests

logger = logging.getLogger(__name__)


def parse_interface(iface):
    """Parse interface into list of networks

    :param iface: Interface name
    :type iface: str

    :return: List of ipaddress IPv4Network networks
    :rtype: list
    """
    if iface == 'lo':
        return [ip_network('127.0.0.1/32', strict=False)]
    else:
        iface = netifaces.ifaddresses(iface)
    networks = []
    for iface_vals in iface.values():
        for address in iface_vals:
            if 'addr' in address and 'netmask' in address:
                try:
                    address_version = ip_address(address['addr']).version
                except ValueError:
                    continue
                if address_version != 4:
                    continue
                else:
                    network = ip_network(
                        f"{address['addr']}/{address['netmask']}",
                        strict=False)
                    logger.debug(f'Found network {network}')
                    networks.append(network)
    return networks


def try_reach_ip(ip):
    """Try to reach IP address and handle all possible exceptions
    If exception is raised or return code is not 0.
    If teleserver weas reached under specified IP then IP will be returned.
    Otherwise, None will be returned.

    :param ip: IP address to test
    :type ip: str

    :return: IP address on success or None in case of failure
    :rtype: str or None
    """
    logger.debug(f'Trying to healthcheck IP: {ip}')
    try:
        response = requests.get(f'http://{ip}:8080/healthcheck', timeout=3)
        print(response.content)
        response = json.loads(response.content)
        print(response)
        if 'rc' in response and response['rc'] == 0:
            logger.debug(f'IP {ip} returned successful response')
            return ip
        else:
            logger.debug(f'IP {ip} returned wrong response: {response}')
            return None
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout):
        logger.debug(f'IP {ip} failed due to one of known requests exception')
        return None
    except json.decoder.JSONDecodeError:
        logger.debug(f'Parsing response from {ip} to json failed')
        return None


def find_teleserver(networks):
    """Find IP addresses with active teleserver in list of networks
    :param networks: List of ipaddress IPv4Network networks
    :type networks: list

    :return: List of IP addresses where teleserver is active
    :rtype: list
    """
    for network in networks:
        hosts = [host for host in network]
        pool = multiprocessing.Pool(processes=10)
        responses = pool.map(try_reach_ip, hosts)
        response = [str(ip) for ip in responses if ip]
    return response
