TELESERVER_DIR = '/var/lib/teleserver'
UPLOAD_DIRECTORY = f'{TELESERVER_DIR}/data'

OPENMEET_var = "https://meet.google.com/"

SPECIAL_CHAR = {
    'asciitilde': '~',
    'exclam': '!',
    'at': '@',
    'numbersign': '#',
    'dollar': '$',
    'percent': '%',
    'asciicircum': '^',
    'ampersand': '&',
    'asterisk': '*',
    'parenleft': '(',
    'parenright': ')',
    'underscore': '_',
    'plus': '+',
    'quoteleft': '`',
    'minus': '-',
    'equal': '=',
    'bracketleft': '[',
    'bracketright': ']',
    'backslash': (r"\"" [0]),
    'braceleft': ' {',
    'braceright': '}',
    'bar': '|',
    'semicolon': ';',
    'quoteright': "'",
    'colon': ':',
    'quotedbl': '"',
    'comma': ',',
    'period': '.',
    'slash': '/',
    'less': '<',
    'greater': '>',
    'question': '?'
}
REV_SPECIAL_CHAR = SPECIAL_CHAR.__class__(map(reversed, SPECIAL_CHAR.items()))
REV_SPECIAL_CHAR[' '] = 'space'
