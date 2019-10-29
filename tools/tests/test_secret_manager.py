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
        self.assertIn('PASS', secrets)
        self.assertIn('SERVICE_PRINCIPAL', secrets)
        self.assertIn('TOKEN_COOKIES', secrets)
        self.assertIn('KEY', secrets)
        self.assertIn('key', secrets['KEY'])
        self.assertNotEqual(secrets['KEY']['key'], '')
        self.assertIsInstance(secrets['KEY']['key'], str)
        self.assertEqual(secrets['PASS'], {})
        self.assertEqual(secrets['SERVICE_PRINCIPAL'], {})
        self.assertEqual(secrets['TOKEN_COOKIES'], {})

    def test_get_secret_key(self):
        self.assertNotEqual(self.manager.get_secret_key(), '')
        self.assertIsInstance(self.manager.get_secret_key(), str)

    def test_set_gui_credentials_for_one_user(self):
        self.manager.set_gui_credentials(user='test', password='secret')
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertIn('test', secrets['PASS'])
        decrypted_password = self.manager.decrypt(secrets['KEY']['key'],
                                                  secrets['PASS']['test'])
        self.assertEqual('secret', decrypted_password)

    def test_set_gui_credentials_for_multiple_user(self):
        self.manager.set_gui_credentials(user='test', password='secret')
        self.manager.set_gui_credentials(user='test2', password='secret2')
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertIn('test', secrets['PASS'])
        decrypted_password = self.manager.decrypt(secrets['KEY']['key'],
                                                  secrets['PASS']['test'])
        self.assertEqual('secret', decrypted_password)
        self.assertIn('test2', secrets['PASS'])
        decrypted_password = self.manager.decrypt(secrets['KEY']['key'],
                                                  secrets['PASS']['test2'])
        self.assertEqual('secret2', decrypted_password)

    def test_verify_credentials(self):
        self.manager.set_gui_credentials(user='test', password='secret')
        self.manager.set_gui_credentials(user='test2', password='secret2')
        self.assertTrue(self.manager.verify_credentials(user='test', password='secret'))
        self.assertTrue(self.manager.verify_credentials(user='test2', password='secret2'))
        self.assertFalse(self.manager.verify_credentials(user='test', password='secret3'))
        self.assertFalse(self.manager.verify_credentials(user='test3', password='secret2'))

    def test_delete_credentials_for_user(self):
        self.manager.set_gui_credentials(user='test', password='secret')
        self.assertTrue(self.manager.verify_credentials(user='test', password='secret'))
        self.manager.delete_credentails_for_user(user='test')
        self.assertFalse(self.manager.verify_credentials(user='test', password='secret'))

    def test_get_credentials_fot_GUI(self):
        self.manager.set_gui_credentials(user='test', password='secret')
        self.manager.set_gui_credentials(user='test2', password='secret2')
        output = {'test': 'secret', 'test2': 'secret2'}
        self.assertDictEqual(self.manager.get_credentials_for_GUI(), output)

    def test_create_service_principal(self):
        token = self.manager.create_service_principal(name='test')
        self.assertNotEqual(token, '')
        self.assertIsInstance(token, str)
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertIn('test', secrets['SERVICE_PRINCIPAL'])
        self.assertNotEqual(secrets['SERVICE_PRINCIPAL']['test'], '')
        self.assertIsInstance(secrets['SERVICE_PRINCIPAL']['test'], str)

    def test_create_time_token_empty_data(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 1)

    def test_create_time_token_empty_password(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {'user': 'testuser'}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 1)

    def test_create_time_token_empty_lease(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {'user': 'testuser', 'password': 'testpass'}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 1)

    def test_create_time_token_partial_empty_lease(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {'user': 'testuser', 'password': 'testpass',
                     'lease_days': '3', 'lease_hours': '0'}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 1)

    def test_create_time_token_correct_data(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {'user': 'testuser', 'password': 'testpass',
                     'lease_days': '3', 'lease_hours': '0',
                     'lease_minutes': '0', 'lease_seconds': '0'}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 0)
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertEqual(len(secrets['TOKEN_COOKIES']), 1)
        test_data = {'user': 'testuser', 'password': 'testpass',
                     'lease_days': '0', 'lease_hours': '1',
                     'lease_minutes': '30', 'lease_seconds': '0'}
        out = self.manager.create_time_token(test_data)
        self.assertEqual(out['rc'], 0)
        secrets = configparser.ConfigParser()
        secrets.read(f'{TELESERVER_DIR}/secret.ini')
        self.assertEqual(len(secrets['TOKEN_COOKIES']), 2)

    def test_delete_time_token(self):
        self.manager.set_gui_credentials(user='testuser', password='testpass')
        test_data = {'user': 'testuser', 'password': 'testpass',
                     'lease_days': '3', 'lease_hours': '0'}
        self.manager.create_time_token(test_data)
        out = self.manager.delete_time_token({'token_name': 'testuser'})
        self.assertEqual(out['rc'], 0)
