#!/usr/bin/python3
import configparser
from cryptography.fernet import Fernet
import os

try:
    from tools.common import TELESERVER_DIR
except ModuleNotFoundError:
    from common import TELESERVER_DIR


class SecretManager():
    """Class for managing passwords to teleserver
    """
    def __init__(self, secret_file=f'{TELESERVER_DIR}/IoT_secret.ini'):
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
        if 'THERMAL_CAMERA' not in config:
            config['THERMAL_CAMERA'] = {}
        if 'KEY' not in config:
            config['KEY'] = {}
            config['KEY']['key'] = Fernet.generate_key().decode('utf-8')
        return config

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

    def create_secrets_for_thermal_camera(self, login, password, ip_address, channel):
        """Create service principal token for automated login
        This token is designed to last for 1000 days and be used by bots to utilize teleserver API

        :param login: Login to thermal camera
        :type login: str
        :param password: Password to thermal camera
        :type password: str
        :param ip_address: IP address of thermal camera
        :type ip_address: str
        :param channel: Default image channel of thermal camera (0 or 1)
        :type channel: str
        """
        self.secrets['THERMAL_CAMERA']['login'] = login
        self.secrets['THERMAL_CAMERA']['password'] = self.encrypt(self.get_secret_key(), password)
        self.secrets['THERMAL_CAMERA']['ip_address'] = ip_address
        self.secrets['THERMAL_CAMERA']['channel'] = channel
        self.save_secrets()

    def thermal_camera_credentials(self):
        """Functino to return all credentials to thermal camera from secrets
        as python dictionary

        :return: Dictionary with thermal camera credentials
        :trype: dict
        """
        output = dict(self.secrets['THERMAL_CAMERA'])
        output['password'] = self.decrypt(self.get_secret_key(), output['password'])
        return output
