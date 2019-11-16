#!/usr/bin/python3
import click
import logging
import sys

import teleserver.keyboard_cli
import teleserver.login_cli
import teleserver.system_cli
import teleserver.webbrowser_cli

logging.basicConfig(filename='teleserver.log', level=logging.DEBUG)

loggers = [__name__,
           teleserver.keyboard_cli.__name__,
           teleserver.login_cli.__name__,
           teleserver.system_cli.__name__,
           teleserver.webbrowser_cli.__name__,
           teleserver.utils.lookup_utils.__name__
           ]

for logger_name in loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('cli.log')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


cli.add_command(teleserver.keyboard_cli.keyboard)
cli.add_command(teleserver.login_cli.log)
cli.add_command(teleserver.system_cli.system)
cli.add_command(teleserver.webbrowser_cli.webbrowser)
