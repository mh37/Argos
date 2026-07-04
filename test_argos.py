import unittest
import argos

class TestCheckVendor(unittest.TestCase):
    def setUp(self):
        # Save the original VENDORS dictionary
        self.original_vendors = argos.VENDORS

        # Mock the VENDORS dictionary with test data
        argos.VENDORS = {
            "001122": "Vendor 6",
            "3344556": "Vendor 7",
            "778899001": "Vendor 9"
        }

    def tearDown(self):
        # Restore the original VENDORS dictionary
        argos.VENDORS = self.original_vendors

    def test_6_char_prefix(self):
        self.assertEqual(argos.checkVendor("00:11:22:AA:BB:CC"), "Vendor 6")

    def test_7_char_prefix(self):
        self.assertEqual(argos.checkVendor("33:44:55:6A:BB:CC"), "Vendor 7")

    def test_9_char_prefix(self):
        self.assertEqual(argos.checkVendor("77:88:99:00:1A:BB"), "Vendor 9")

    def test_formatting_normalization(self):
        # Check uppercase and formatting issues
        self.assertEqual(argos.checkVendor("00:11:22:aa:bb:cc".upper()), "Vendor 6")
        self.assertEqual(argos.checkVendor("33:44:55:6a:bb:cc".lower()), "Vendor 7")

    def test_unmatched_case(self):
        self.assertEqual(argos.checkVendor("FF:FF:FF:FF:FF:FF"), "N/A")

    def test_edge_cases(self):
        self.assertEqual(argos.checkVendor(""), "N/A")
        self.assertEqual(argos.checkVendor("12:34"), "N/A")
        self.assertEqual(argos.checkVendor("001122AABBCC"), "Vendor 6") # no colons

if __name__ == '__main__':
    unittest.main()
