from cryptography.fernet import Fernet
import configparser


class SecretManager():

    def __init__(self, secret_file='secret.ini'):
        self.secret_file = secret_file

    def get_credentials(self):
        config = configparser.ConfigParser()
        config.read(self.secret_file)
        key = config['KEY']['key']
        user_crypt = config['PASS']['user']
        pass_crypt = config['PASS']['pass']
        return [self.decrypt(key, user_crypt), self.decrypt(key, pass_crypt)]

    @staticmethod
    def decrypt(key, var):
        f = Fernet(key)
        return f.decrypt(bytes(var, 'utf-8')).decode('utf-8')

    def encrypt_credentials(self, user, password):
        key = Fernet.generate_key()
        user_crypt = self.encrypt(key, user)
        pass_crypt = self.encrypt(key, password)
        return user_crypt, pass_crypt, key.decode('utf-8')

    @staticmethod
    def encrypt(key, var):
        f = Fernet(key)
        return f.encrypt(bytes(var, 'utf-8')).decode('utf-8')

    def set_credentials(self, user, password, file_loc='secret.ini'):
        user_crypt, pass_crypt, key = self.encrypt_credentials(user, password)
        config = configparser.ConfigParser()
        config['PASS'] = {'user': user_crypt,
                          'pass': pass_crypt}
        config['KEY'] = {'key': key}
        with open(file_loc, 'w') as dest_file:
            config.write(dest_file)
