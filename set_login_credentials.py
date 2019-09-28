#!/usr/bin/python3

from tools.secret_manager import SecretManager
import getpass
import sys

if __name__ == "__main__":
    sec = SecretManager()
    u = input('Please choose new username: ')
    p = getpass.getpass('Please choose new password: ', stream=None)
    p2 = getpass.getpass('Please confirm new password: ', stream=None)
    if p == p2:
        sec.set_credentials(u, p)
        sys.exit(0)
    else:
        sys.exit(1)
