import dash
import unittest

from layouts.keyboard_layout import create_keyboard_layout, create_keyboard


class TestKeyboardLayout(unittest.TestCase):

    def test_sample_key_shortcuts(self):
        self.assertIsInstance(type(create_keyboard_layout()),
                              dash.development.base_component.ComponentMeta)

    def test_key_control_layout(self):
        self.assertIsInstance(type(create_keyboard()),
                              dash.development.base_component.ComponentMeta)
