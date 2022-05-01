import unittest
from utils import *
from unittest.mock import patch, call

class TestUtils(unittest.TestCase):
    def test_print_log_game(self):
        with patch('builtins.print') as mock_print:
            Utils.print_log_game('test')
            self.assertEqual(mock_print.mock_calls, [call('This is a test')])

    def test_template_log(self):
        self.assertIsInstance(Utils.template_log('test'), str)

    def test_multi_key_dict_get(self):
        self.assertEqual(Utils.multi_key_dict_get({'a': 1, 'b': 2}, 'a'), 1)
        self.assertEqual(Utils.multi_key_dict_get({'a': 1, 'b': 2}, 'c'), None)
        self.assertEqual(Utils.multi_key_dict_get({(1,2,3): 2, (4,5,6): 1}, 1), 2)

if __name__ == '__main__':
    unittest.main()