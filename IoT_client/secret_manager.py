#!/usr/bin/python3
import configparser
from cryptography.fernet import Fernet
import datetime
import jwt
import os

from common import TELESERVER_DIR


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
        if 'TOKEN' not in config:
            config['TOKEN'] = {}
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

    def get_secret_key(self):
        """Return secret key to decode credentials

        :return: Secret key
        :rtype: str
        """
        return self.secrets['KEY']['key']

    def create_token(self, name=None):
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
        token = jwt.encode({'user': name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10000)},
                           key=self.get_secret_key())
        self.secrets['TOKEN'][name] = token.decode('utf-8')
        self.save_secrets()
        return token.decode('utf-8')


if __name__ == '__main__':
    sec = SecretManager(secret_file='/tmp/secret.ini')
    token = sec.create_token()
    print(f'\nToken to access IoT client:\n\n{token}\n\n'
          'Save it to clients.yml file together with client IP')
