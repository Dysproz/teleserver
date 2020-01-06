import unittest
from parameterized import parameterized

import tools.notifications as notify


class TestCheckIfConditionsTrue(unittest.TestCase):

    @parameterized.expand([
        ('==', '3', True),
        ('==', '4', False),
        ('<', '4', True),
        ('>', '2', True),
        ('<', '2', False),
        ('>', '4', False)
    ])
    def test_condition_with_digits(self, operator, test_val, expected):
        self.assertEqual(notify.check_if_condition_true('3', operator, test_val), expected)

    @parameterized.expand([
        ('==', '3.3', True),
        ('==', '4.3', False),
        ('<', '4.3', True),
        ('>', '2.3', True),
        ('<', '2.3', False),
        ('>', '4.3', False)
    ])
    def test_condition_with_floats(self, operator, test_val, expected):
        self.assertEqual(notify.check_if_condition_true('3.3', operator, test_val), expected)


class TestCheckNotificationConditions(unittest.TestCase):

    def setUp(self):
        self.mock_data = {
            'var1': 15,
            'var2': 20,
            'var3': 1,
            'var4': 0
        }

        self.mock_condition1 = {
            'var1': {
                'value': 16,
                'operator': '<'
            },
            'var2': {
                'value': 17,
                'operator': '>'
            }

        }

        self.mock_condition2 = {
            'var3': {
                'value': 1,
                'operator': '=='
            },
            'var4': {
                'value': 0,
                'operator': '!='
            }
        }

    def test_positive_check(self):
        self.assertTrue(notify.check_notification_conditions(self.mock_data,
                                                             self.mock_condition1))

    def test_negative_check(self):
        self.assertFalse(notify.check_notification_conditions(self.mock_data,
                                                              self.mock_condition2))
