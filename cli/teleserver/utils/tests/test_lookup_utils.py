from ipaddress import ip_network
import json
from mock import patch, MagicMock
import requests
import unittest

import teleserver.utils.lookup_utils as utils


class TestParseInterface(unittest.TestCase):
    mock_interface = {
        17: [{
            'addr': '10.0.0.4',
            'netmask': '255.0.0.0'
        }],
        2: [{
            'addr': '192.168.1.12',
            'netmask': '255.255.255.0',
            'broadcast': '192.168.1.255'
        }],
        10: [{
            'addr': '54c8:1d2c:1e4a:96ef:d544:3fea:794d:1c2e',
            'netmask': 'ffff:ffff:ffff:ffff::/64'
        }]
    }

    def test_loopback_interface(self):
        expected = [ip_network('127.0.0.1/32', strict=False)]
        self.assertEqual(utils.parse_interface('lo'), expected)

    @patch('netifaces.ifaddresses')
    def test_interface_parsing(self, mock_ifaddresses):
        mock_ifaddresses.return_value = self.mock_interface
        expected = [ip_network('192.168.1.12/255.255.255.0', strict=False),
                    ip_network('10.0.0.4/255.0.0.0', strict=False)]
        self.assertListEqual(sorted(utils.parse_interface('wlp4s0')),
                             sorted(expected))


class TestTryReachIP(unittest.TestCase):
    @patch('requests.get')
    def test_successfull_request(self, mock_get):
        expected = {"message": "success", "rc": 0}
        mock_response = MagicMock()
        mock_response.content = (json.dumps(expected)+'\n').encode('utf-8')
        mock_get.return_value = mock_response
        self.assertEqual(utils.try_reach_ip('192.168.1.31'), '192.168.1.31')

    @patch('requests.get')
    def test_fail_request(self, mock_get):
        expected = {"message": "fail", "rc": 1}
        mock_response = MagicMock()
        mock_response.content = (json.dumps(expected)+'\n').encode('utf-8')
        mock_get.return_value = mock_response
        self.assertIsNone(utils.try_reach_ip('192.168.1.31'))

    @patch('requests.get')
    def test_wrong_json_parse(self, mock_get):
        expected = {'message': 'success', 'rc': 0}
        mock_response = MagicMock()
        mock_response.content = (str(expected)+'\n').encode('utf-8')
        mock_get.return_value = mock_response
        self.assertIsNone(utils.try_reach_ip('192.168.1.31'))

    @patch('requests.get', side_effect=requests.exceptions.ConnectionError)
    def test_connection_error(self, mock_get):
        self.assertIsNone(utils.try_reach_ip('192.168.1.31'))

    @patch('requests.get', side_effect=requests.exceptions.ReadTimeout)
    def test_read_timeout(self, mock_get):
        self.assertIsNone(utils.try_reach_ip('192.168.1.31'))

    @patch('requests.get', side_effect=requests.exceptions.ConnectTimeout)
    def test_connection_timeout(self, mock_get):
        self.assertIsNone(utils.try_reach_ip('192.168.1.31'))
