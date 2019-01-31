from subprocess import call
import webbrowser
import alsaaudio
import pyscreenshot as ImageGrab
from io import BytesIO
import base64


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
    webbrowser.open('https://'+url, new=0)


def poweroff():
    call(['systemctl', 'poweroff', '-i'])


def reboot():
    call(['systemctl', 'reboot', '-i'])


def screenshot():
    call(['gnome-screenshot'])


def mute():
    vol = alsaaudio.Mixer()
    vol.setvolume(0)


def volume(volume):
    vol = alsaaudio.Mixer()
    vol.setvolume(volume)


def get_volume():
    vol = alsaaudio.Mixer()
    value = vol.getvolume()
    return value[0]


def get_screen():
    screen = ImageGrab.grab()
    buffered_screen = BytesIO()
    screen.save(buffered_screen, format='JPEG')
    return base64.b64encode(buffered_screen.getvalue()).decode('utf-8')
