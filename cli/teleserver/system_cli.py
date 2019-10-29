import base64
import click
import logging

from teleserver.requests_handler import make_request
logger = logging.getLogger(__name__)


@click.group()
def system():
    """Manage system of teleserver
    """
    pass


@system.command('poweroff')
def poweroff():
    """Power off teleserver machine
    """
    logger.info('Powering off...')
    response = make_request('system/poweroff')
    logger.info(f"Server response: {response['message']}")


@system.command('reboot')
def reboot():
    """Reboot teleserver machine
    """
    logger.info('Rebooting...')
    response = make_request('system/reboot')
    logger.info(f"Server response: {response['message']}")


@system.command('screenshot')
def screenshot():
    """Take a screenshot of teleserver
    """
    logger.info('Making screenshot...')
    response = make_request('system/screenshot')
    logger.info(f"Server response: {response['message']}")


@system.command('mute')
def mute():
    """Mute the volume
    """
    logger.info('Muting...')
    response = make_request('system/mute')
    logger.info(f"Server response: {response['message']}")


@system.command('set_volume')
@click.option('--level', default=0, help='Volume level (0-100)')
def set_volume(level):
    """Set volume to specific level
    """
    logger.info('Setting volume...')
    logger.debug('args: level: {level}')
    response = make_request('system/set_volume', {'lvl': level})
    logger.info(f"Server response: {response['message']}")


@system.command('grab_screen')
@click.option('--output', default='~/teleserver_screen.jpg', help='Output file for grabbed screen')
def grab_screen(output):
    """Take a screenshot and save it to local files
    """
    logger.info(f'Grabbing screen and saving to {output}')
    logger.debug(f'args: output: {output}')
    response = make_request('system/grab_screen')
    logger.info(f"Server response: {response['message']}")
    imgdata = base64.b64decode(response['screen'])
    with open(output, 'wb') as f:
        f.write(imgdata)
    logger.info(f'Saved image to {output}')
