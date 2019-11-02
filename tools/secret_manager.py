import configparser
from cryptography.fernet import Fernet
import datetime
import jwt
import os

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
        self.secrets = self.get_current_secrets(secret_file)

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

    def save_secrets(self):
        """Save current secrets to secret file
        """
        try:
            os.mknod(self.secret_file)
        except FileExistsError:
            pass
        with open(self.secret_file, 'w') as secret_file:
            self.secrets.write(secret_file)

    def set_gui_credentials(self, user, password):
        """Set user, password credentials in file

        :param user: username
        :type user: str
        :param password: password
        :type password: str
        """
        self.secrets['PASS'][user] = self.encrypt(self.secrets['KEY']['key'], password)
        self.save_secrets()

    def verify_credentials(self, user, password):
        """Verify user, password credentials in file

        :param user: username
        :type user: str
        :param password: password
        :type password: str

        :return: Result whether credentials are correct
        :rtype: bool
        """
        if user not in self.secrets['PASS']:
            return False
        else:
            return self.decrypt(self.secrets['KEY']['key'], self.secrets['PASS'][user]) == password

    def delete_credentails_for_user(self, user):
        """Delete user credentials from database

        :param user: username
        :type user: str
        """
        if user in self.secrets['PASS']:
            del self.secrets['PASS'][user]
        self.save_secrets()

    def get_credentials_for_GUI(self):
        """Get list of credentials pair for GUI purposes

        :return: Dictionary of user-password pair
        :rtype: dict
        """
        credentials = {}
        for user in self.secrets['PASS']:
            credentials[user] = self.decrypt(self.secrets['KEY']['key'], self.secrets['PASS'][user])
        return credentials

    def create_service_principal(self, name=None):
        """Create service principal token for automated login
        This token is designed to last for 1000 days and be used by bots to utilize teleserver API

        :param name: Name of service principal
        :type name: str

        :return: Generated token
        :rtype: str
        """
        if name is None:
            date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            name = f'token_{date}'
        token = jwt.encode({'user': name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1000)},
                           key=self.get_secret_key())
        self.secrets['SERVICE_PRINCIPAL'][name] = token.decode('utf-8')
        self.save_secrets()
        return token.decode('utf-8')

    def get_secret_key(self):
        """Return secret key to decode credentials

        :return: Secret key
        :rtype: str
        """
        return self.secrets['KEY']['key']

    def create_time_token(self, data):
        """Create user time token
        This token is designed ot serve for short time to CLI user
        At first, SecretManager checks whether provided GUI credentials are correct
        and then generates token with time based on passed lease variables
        Data must contain:
        * user - GUI username
        * password - GUI password
        * lease_days - Number of days to lease token for
        * lease_hours - Number of hours to lease token for
        * lease_minutes - Number of minutes to lease token for
        * lease_seconds - Number of seconds to lease token for

        :param data: Data with all variables specified
        :type data: dict

        :return: Dictionary with message and return code of function.
        When token is created it will be provided as token variable
        :rtype: dict
        """
        if 'user' not in data or 'password' not in data:
            return {'message': 'user or password was not passed', 'rc': 1}
        if ('lease_days' not in data or 'lease_hours' not in data or
           'lease_minutes' not in data or 'lease_seconds' not in data):
            return {'message': 'Lease time was not passed', 'rc': 1}
        logins = self.get_credentials_for_GUI()
        if data['user'] in logins:
            if data['password'] == logins[data['user']]:
                token = jwt.encode({'user': data['user'],
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(days=int(data['lease_days']),
                                                       hours=int(data['lease_hours']),
                                                       minutes=int(data['lease_minutes']),
                                                       seconds=int(data['lease_seconds']))},
                                   key=self.get_secret_key())
                token = token.decode('utf-8')
                date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
                name = f'token_{date}_{token[-1]}'
                self.secrets['TOKEN_COOKIES'][name] = token
                with open(self.secret_file, 'w') as secret_file:
                    self.secrets.write(secret_file)
                return {'message': 'Token created',
                        'token': token,
                        'name': name,
                        'rc': 0}
            else:
                return {'message': 'Wrong password', 'rc': 1}
        else:
            return {'message': 'User not in database', 'rc': 1}

    def delete_time_token(self, data):
        """Delete time token from secrets

        :param data: Dictionary with key token_name to delete
        :type data: dict

        :return: Operation status
        :rtype: dict
        """
        if 'token_name' not in data:
            return {'message': 'token does not exist', 'rc': 1}
        else:
            token_name = data['token_name']
            if token_name not in self.secrets['TOKEN_COOKIES']:
                return {'message': 'Token removed', 'rc': 0}
            else:
                del self.secrets['TOKEN_COOKIES'][token_name]
                self.save_secrets()
                return {'message': 'Token removed', 'rc': 0}
