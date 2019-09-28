import dash_core_components as dcc
import dash_html_components as html

import layouts.style.style as style

KEYBOARD_KEYS = [
    [
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'Home', 'End'
    ],
    [
        'asciitilde', 'exclam', 'at', 'numbersign', 'dollar', 'percent',
        'asciicircum', 'ampersand', 'asterisk', 'parenleft', 'parenright',
        'underscore', 'plus'
    ],
    [
        'quoteleft', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus',
        'equal', 'BackSpace'
    ],
    [
        'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'bracketleft',
        'bracketright', 'backslash', 'braceleft', 'braceright', 'bar'
    ],
    [
        'Caps_Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'semicolon',
        'quoteright', 'colon', 'quotedbl', 'Return'
    ],
    [
        'shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'period', 'slash',
        'less', 'greater', 'question'
    ], ['ctrl', 'Alt', 'space', 'Super', 'Up', 'Down', 'Left', 'Right']
]

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

FLAT_KEYBOARD_KEYS = [item for sublist in KEYBOARD_KEYS for item in sublist]
KEYBOARD_NAMES = ['{}-button'.format(name) for name in FLAT_KEYBOARD_KEYS]


def create_keyboard_layout():
    """Create keyboard layout for dash

    :return: Keyboard layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        html.Div([
            dcc.Input(id='key-control', type='text', value=''),
        ],
                 style={'margin': style.PADDING}),
        html.Button(
            id='key-control-button',
            n_clicks=0,
            children='Execute',
            style={
                'margin': style.PADDING,
                'backgroundColor': style.BUTTON_COLOR
            }),
        create_keyboard()
    ])


def create_keyboard():
    """Create keyboard
    Create Div with keyboard keys

    :return: keyboard keys
    :rtype: dash.development.base_component.ComponentMeta
    """
    keyboard_layout = []
    for line in KEYBOARD_KEYS:
        line_layout = []
        for key in line:
            if key in SPECIAL_CHAR:
                display_key = SPECIAL_CHAR[key]
            else:
                display_key = key
            line_layout.append(
                html.Button(
                    id='{}-button'.format(key),
                    n_clicks_timestamp=0,
                    children=display_key,
                    style={
                        'margin': style.PADDING,
                        'backgroundColor': style.BUTTON_COLOR
                    }))
        keyboard_layout.append(html.Div(line_layout))
    return html.Div(keyboard_layout)
