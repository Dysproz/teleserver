import alsaaudio
import base64
from io import BytesIO
import pyscreenshot as ImageGrab
from subprocess import call
import webbrowser

from common import TELESERVER_DIR


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
    if url.startswith(URL_SCHEMES):
        return url
    else:
        return 'https://' + url


def close():
    call(["pkill", "chrome"])


def web_open(url):
    webbrowser.open(url_parser(url), new=0)


def poweroff():
    call(['systemctl', 'poweroff', '-i'])


def reboot():
    call(['systemctl', 'reboot', '-i'])


def screenshot():
    call(['gnome-screenshot',
          '-f',
          '{dir}/data/$(date +"%m_%d_%Y_%H_%M_%S""_screenshot.png")'
          .format(dir=TELESERVER_DIR)])


def mute():
    vol = alsaaudio.Mixer()
    vol.setvolume(0)


def volume(volume):
    vol = alsaaudio.Mixer()
    vol.setvolume(volume)


def xdotool_key(keys):
    call(['xdotool', 'key', keys])


def get_volume():
    vol = alsaaudio.Mixer()
    value = vol.getvolume()
    return value[0]


def get_screen():
    screen = ImageGrab.grab()
    buffered_screen = BytesIO()
    screen.save(buffered_screen, format='JPEG')
    return base64.b64encode(buffered_screen.getvalue()).decode('utf-8')
