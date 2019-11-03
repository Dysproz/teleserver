import configparser
import os

from pyfakefs import fake_filesystem_unittest

from tools.common import TELESERVER_DIR
from tools.secret_manager import SecretManager


class TestSecretManager(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs(TELESERVER_DIR)
        self.manager = SecretManager()

    def test_empty_secret_file(self):
        self.manager.save_secrets()
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertIn('TOKEN', secrets)
        self.assertIn('KEY', secrets)
        self.assertIn('key', secrets['KEY'])
        self.assertNotEqual(secrets['KEY']['key'], '')
        self.assertIsInstance(secrets['KEY']['key'], str)
        self.assertEqual(secrets['TOKEN'], {})

    def test_get_secret_key(self):
        self.assertNotEqual(self.manager.get_secret_key(), '')
        self.assertIsInstance(self.manager.get_secret_key(), str)

    def test_create_token(self):
        token = self.manager.create_token(name='test')
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertIn('test', secrets['TOKEN'])
        self.assertEqual(token, secrets['TOKEN']['test'])
