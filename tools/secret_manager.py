import configparser
from cryptography.fernet import Fernet
import datetime
import jwt

from tools.common import TELESERVER_DIR


class SecretManager():
    """Class for managing passwords to teleserver
    """
    def __init__(self, secret_file=f'{TELESERVER_DIR}/secret.ini'):
        """Init method for SecretManager class

        :param secret_file: Absolut path to file where to store secrets
        :type secret_file: str
        """
        self.secret_file = secret_file

    @staticmethod
    def decrypt(key, var):
        """Decrypt variable with a key
        :param key: key to decrypt
        :type key: str
        :param var: variable to decrypt
        :type var: str
        :return: decrypted variable
        :rtype: str
        """
        f = Fernet(key)
        return f.decrypt(bytes(var, 'utf-8')).decode('utf-8')

    @staticmethod
    def encrypt(key, var):
        """Encrypt variable with key
        :param key: Key to use to encrypt
        :type key: str
        :param var: Variable to encrypt
        :type var: str
        :return: Encrypted variable
        :rtype: str
        """
        f = Fernet(key)
        return f.encrypt(bytes(var, 'utf-8')).decode('utf-8')

    @staticmethod
    def get_current_secrets(file_location):
        """Read secrets from specific location
        If there's missing any section of secrets file then add it

        :param file_location: Location of secret file
        :type file_location: str

        :return: configparser with read secrets
        :rtype: configparser.ConfigParser
        """
        config = configparser.ConfigParser()
        config.read(file_location)
        if 'PASS' not in config:
            config['PASS'] = {}
        if 'SERVICE_PRINCIPAL' not in config:
            config['SERVICE_PRINCIPAL'] = {}
        if 'TOKEN_COOKIES' not in config:
            config['TOKEN_COOKIES'] = {}
        if 'KEY' not in config:
            config['KEY'] = {}
            config['KEY']['key'] = Fernet.generate_key().decode('utf-8')
        return config

    def set_gui_credentials(self, user, password, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Set user, password credentials in file

        :param user: username
        :type user: str
        :param password: password
        :type password: str
        :param file_loc: Location of secret file
        :type file_loc: str
        """
        secrets = self.get_current_secrets(file_loc)
        secrets['PASS'][user] = self.encrypt(secrets['KEY']['key'], password)
        with open(file_loc, 'w') as secret_file:
            secrets.write(secret_file)

    def verify_credentials(self, user, password, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Verify user, password credentials in file

        :param user: username
        :type user: str
        :param password: password
        :type password: str
        :param file_loc: Location of secret file
        :type file_loc: str

        :return: Result whether credentials are correct
        :rtype: bool
        """
        secrets = self.get_current_secrets(file_loc)
        if user not in secrets['PASS']:
            return False
        else:
            return self.decrypt(secrets['KEY']['key'], secrets['PASS'][user]) == password

    def delete_credentails_for_user(self, user, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Delete user credentials from database

        :param user: username
        :type user: str
        :param file_loc: Location of secret file
        :type file_loc: str
        """
        secrets = self.get_current_secrets(file_loc)
        if user in secrets['PASS']:
            del secrets['PASS'][user]
        with open(file_loc, 'w') as secret_file:
            secrets.write(secret_file)

    def get_credentials_for_GUI(self, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Get list of credentials pair for GUI purposes

        :param file_loc: Location of secret file
        :type file_loc: str

        :return: Dictionary of user-password pair
        :rtype: dict
        """
        credentials = {}
        secrets = self.get_current_secrets(file_loc)
        for user in secrets['PASS']:
            credentials[user] = self.decrypt(secrets['KEY']['key'], secrets['PASS'][user])
        return credentials

    def create_service_principal(self, name=None, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Create service principal token for automated login
        This token is designed to last for 1000 days and be used by bots to utilize teleserver API

        :param name: Name of service principal
        :type name: str
        :param file_loc: Location of secret file
        :type file_loc: str

        :return: Generated token
        :rtype: str
        """
        if name is None:
            date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            name = f'token_{date}'
        secrets = self.get_current_secrets(file_loc)
        token = jwt.encode({'user': name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1000)},
                           key=self.get_secret_key())
        secrets['SERVICE_PRINCIPAL'][name] = token.decode('utf-8')
        with open(file_loc, 'w') as secret_file:
            secrets.write(secret_file)
        return token.decode('utf-8')

    def get_secret_key(self, file_loc=f'{TELESERVER_DIR}/secret.ini'):
        """Return secret key to decode credentials

        :param file_loc: Location of secret file
        :type file_loc: str

        :return: Secret key
        :rtype: str
        """
        secrets = self.get_current_secrets(file_loc)
        return secrets['KEY']['key']
