import configparser
import os

from pyfakefs import fake_filesystem_unittest

from IoT_master.tools.common import TELESERVER_DIR
from IoT_master.tools.secret_manager import SecretManager


class TestSecretManager(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs(TELESERVER_DIR)
        self.manager = SecretManager()

    def test_empty_secret_file(self):
        self.manager.save_secrets()
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/IoT_secret.ini')
        self.assertIn('THERMAL_CAMERA', secrets)
        self.assertIn('KEY', secrets)
        self.assertIn('key', secrets['KEY'])
        self.assertNotEqual(secrets['KEY']['key'], '')
        self.assertIsInstance(secrets['KEY']['key'], str)
        self.assertEqual(secrets['THERMAL_CAMERA'], {})

    def test_get_secret_key(self):
        self.assertNotEqual(self.manager.get_secret_key(), '')
        self.assertIsInstance(self.manager.get_secret_key(), str)

    def test_create_secrets_for_thermal_camera(self):
        self.manager.create_secrets_for_thermal_camera('test', 'secret', '127.0.0.1', '1')
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/IoT_secret.ini')
        self.assertEqual('test', secrets['THERMAL_CAMERA']['login'])
        self.assertNotEqual('secret', secrets['THERMAL_CAMERA']['password'])
        self.assertEqual('127.0.0.1', secrets['THERMAL_CAMERA']['ip_address'])
        self.assertEqual('1', secrets['THERMAL_CAMERA']['channel'])
        decrypted_password = self.manager.decrypt(secrets['KEY']['key'],
                                                  secrets['THERMAL_CAMERA']['password'])
        self.assertEqual('secret', decrypted_password)

    def test_thermal_camera_credentials(self):
        self.manager.create_secrets_for_thermal_camera('test', 'secret', '127.0.0.1', '1')
        out = self.manager.thermal_camera_credentials()
        self.assertIn('login', out)
        self.assertIn('password', out)
        self.assertIn('ip_address', out)
        self.assertIn('channel', out)
        self.assertEqual(out['login'], 'test')
        self.assertEqual(out['password'], 'secret')
        self.assertEqual(out['ip_address'], '127.0.0.1')
        self.assertEqual(out['channel'], '1')
