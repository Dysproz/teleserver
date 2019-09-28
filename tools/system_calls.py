import alsaaudio
import base64
from io import BytesIO
import pyscreenshot as ImageGrab
from subprocess import call
import webbrowser


URL_SCHEMES = ('file://',
               'ftp://',
               'gopher://',
               'hdl://',
               'http://',
               'https://',
               'imap://',
               'mailto://',
               'mms://',
               'news://',
               'nntp://',
               'prospero://',
               'rsync://',
               'rtsp://',
               'rtspu://',
               'sftp://',
               'shttp://',
               'sip://',
               'sips://',
               'snews://',
               'svn://',
               'svn+ssh://',
               'telnet://',
               'wais://',
               'ws://',
               'wss://')


def url_parser(url):
    """Parse url.
    If URL does not contain any of url schemas at the beginning
    then add https:// at the beginning.

    :param url: URL to parse
    :type url: str

    :return: Parsed URL
    :rtype: str
    """
    if url.startswith(URL_SCHEMES):
        return url
    else:
        return 'https://' + url


def close():
    """Close web browser
    """
    call(["pkill", "chrome"])


def web_open(url):
    """Open URL in web browser

    :param url: URL to open
    :type url: str
    """
    webbrowser.open(url_parser(url), new=0)


def poweroff():
    """Power off the machine
    """
    call(['systemctl', 'poweroff', '-i'])


def reboot():
    """Reboot the machine
    """
    call(['systemctl', 'reboot', '-i'])


def screenshot():
    """Make a screenshot
    """
    call(['gnome-screenshot'])


def mute():
    """Mute the machine
    """
    vol = alsaaudio.Mixer()
    vol.setvolume(0)


def volume(volume):
    """Set volume level on the machine

    :param volume: Volume level
    :type volume: int
    """
    vol = alsaaudio.Mixer()
    vol.setvolume(volume)


def xdotool_key(keys):
    """Call xdotool with specific keys

    :param keys: Keys to call
    :type keys: str
    """
    call(['xdotool', 'key', keys])


def get_volume():
    """Get current level of volume

    :return: Volume level
    :rtype: int
    """
    vol = alsaaudio.Mixer()
    value = vol.getvolume()
    return value[0]


def get_screen():
    """Get current snapshot of machine's screen

    :return: Screen's snapshot
    :rtype: base64.bytes
    """
    screen = ImageGrab.grab()
    buffered_screen = BytesIO()
    screen.save(buffered_screen, format='JPEG')
    return base64.b64encode(buffered_screen.getvalue()).decode('utf-8')
