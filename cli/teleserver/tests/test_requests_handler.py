import json
import mock
import os
from pyfakefs import fake_filesystem_unittest

from teleserver.requests_handler import make_request

target_url = 'https://127.0.0.1:8080/test/route?var1=val1&var2=val2'
target_data = {'postvar1': 'postval1',
               'postvar2': 'postval2',
               'postvar3': 'postval3',
               'token': 'secret'}


class MockResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def _mock_request(url=None, data=None):
    print(url)
    print(data)
    print(url == target_url)
    print(data == target_data)
    if url == target_url and data == target_data:
        return MockResponse({'message': 'success', 'rc': 0})
    else:
        return MockResponse({'message': 'failure', 'rc': 1})


class TestRequestsHandler(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    @mock.patch('requests.post', side_effect=_mock_request)
    def test_make_request(self, mock_post):
        test_credentials = {'token_name': 'testtoken',
                            'token': 'secret',
                            'server': '127.0.0.1'}
        os.makedirs('~/.teleserver')
        with open('~/.teleserver/credentials.json', 'w') as f:
            json.dump(test_credentials, f)
        url_args = {'var1': 'val1',
                    'var2': 'val2'}
        route = 'test/route'
        post_args = {'postvar1': 'postval1',
                     'postvar2': 'postval2',
                     'postvar3': 'postval3'}
        response = make_request(route=route, url_args=url_args, post_args=post_args)
        self.assertEqual(response['rc'], 0)
