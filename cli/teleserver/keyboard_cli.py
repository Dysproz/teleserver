import click
import logging

from teleserver.requests_handler import make_request

logger = logging.getLogger(__name__)


@click.group()
def keyboard():
    """Input group to teleserver
    """
    pass


@keyboard.command('call_key')
@click.option('--key', default='', help='Key to call in xdotool format')
def call_key(key):
    """Call specific key in xdotool format
    """
    logger.info('Calling key...')
    logger.debug(f'args: key: {key}')
    response = make_request('keyboard/call_key', {'key': key})
    logger.info(f"Server response: {response['message']}")


@keyboard.command('call_word')
@click.option('--word', default='', help='Word to enter')
def call_word(word):
    """Call specific word or key string
    """
    logger.info('Calling word')
    logger.debug(f'args: word: {word}')
    response = make_request('keyboard/call_word', {'word': word})
    logger.info(f"Server response: {response['message']}")
