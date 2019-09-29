import dash
import unittest

from layouts.screen_layout import create_screen_content


class TestKeyboardLayout(unittest.TestCase):

    def test_create_screen_content(self):
        self.assertIsInstance(type(create_screen_content()),
                              dash.development.base_component.ComponentMeta)
