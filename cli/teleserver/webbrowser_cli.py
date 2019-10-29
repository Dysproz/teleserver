import click
import logging

from teleserver.requests_handler import make_request

logger = logging.getLogger(__name__)


@click.group()
def webbrowser():
    """Manage teleserver web browser
    """
    pass


@webbrowser.command('openmeet')
def openmeet():
    """Open well-known Google Meet link
    """
    logger.info('Opening meet...')
    response = make_request('webbrowser/openmeet')
    logger.info(f"Server response: {response['message']}")


@webbrowser.command('open')
@click.option('--url', default='github.com/Dysproz/teleserver', help='URL to open')
def open(url):
    """Open specific URL on teleserver
    """
    logger.info('Opening URL...')
    logger.debug(f'args: url: {url}')
    response = make_request('webbrowser/open', {'url': url})
    logger.info(f"Server response: {response['message']}")


@webbrowser.command('close')
def close():
    """Close web browser on teleserver
    """
    logger.info('Closing webbrowser...')
    response = make_request('webbrowser/close')
    logger.info(f"Server response: {response['message']}")
