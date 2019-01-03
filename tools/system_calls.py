from subprocess import call
import webbrowser

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
    call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%', 'unmute'])


def volume(volume):
    call(['amixer',
          '-D',
          'pulse',
          'set',
          'Master',
          str(volume)+'%',
          'unmute'])


def update():
    call(['/usr/local/teleserver/update.sh'])