import dash
import unittest

from layouts.key_control_layout import create_key_control_layout, create_sample_key_shortcuts


class TestKeyControlLayout(unittest.TestCase):

    def test_sample_key_shortcuts(self):
        self.assertIsInstance(type(create_sample_key_shortcuts()),
                              dash.development.base_component.ComponentMeta)

    def test_key_control_layout(self):
        self.assertIsInstance(type(create_key_control_layout()),
                              dash.development.base_component.ComponentMeta)
