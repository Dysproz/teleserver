from subprocess import call
import webbrowser
import alsaaudio


def urlChecker(url):
    if not url.startswith('http'):
        if url.startswith('www'):
            url = "http://" + url
        else:
            url = "http://www." + url
    return url


def close():
    call(["pkill", "chrome"])


def web_open(url):
    webbrowser.open(urlChecker(url), new=0)


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


def update():
    call(['/usr/local/teleserver/update.sh'])


def get_volume():
    vol = alsaaudio.Mixer()
    value = vol.getvolume()
    return value[0]
