import dash
import unittest
from unittest.mock import patch

from layouts.system_options_layout import create_system_options


class TestKeyboardLayout(unittest.TestCase):

    @patch('alsaaudio.Mixer')
    def test_create_system_options(self, mixer):
        self.assertIsInstance(type(create_system_options()),
                              dash.development.base_component.ComponentMeta)
