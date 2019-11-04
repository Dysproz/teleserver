import getpass
from tools.secret_manager import SecretManager


if __name__ == '__main__':
    sec = SecretManager()
    print('Setting up credentials to thermal camera:\n')
    login = input('Please enter login: ')
    password = getpass.getpass('Please enter password: ', stream=None)
    ip = input('Please enter IP address of your camera: ')
    channel = input('Please enter default channel of your camera: ')
    sec.create_secrets_for_thermal_camera(login, password, ip, channel)
    print(f'Credentials to your thermal camera with IP: {ip} for login {login} are now saved')
