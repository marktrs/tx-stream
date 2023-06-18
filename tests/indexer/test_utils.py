from unittest import TestCase
from flows.indexer.utils import hex_to_address, hex_to_int


class TestHexToAddress(TestCase):
    def test_default(self):
        test_input = "0x0000000000000000010ad07e"
        expected_output = "0x10ad07e"
        self.assertEqual(hex_to_address(test_input), expected_output)

    def test_no_prefix(self):
        test_input = "0000000000000000010ad07e"
        expected_output = "0x10ad07e"
        self.assertEqual(hex_to_address(test_input), expected_output)


class TestHexToInt(TestCase):
    def test_default(self):
        test_input = "0x10ad07e"
        expected_output = 17485950
        self.assertEqual(hex_to_int(test_input), expected_output)

    def test_min_length(self):
        test_input = "0x"
        expected_output = 0
        self.assertEqual(hex_to_int(test_input), expected_output)

    def test_zero_length(self):
        test_input = ""
        expected_output = 0
        self.assertEqual(hex_to_int(test_input), expected_output)

    def test_no_prefix(self):
        test_input = "abc"
        expected_output = 2748
        self.assertEqual(hex_to_int(test_input), expected_output)
