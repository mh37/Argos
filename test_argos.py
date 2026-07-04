import unittest
from unittest.mock import patch, mock_open
import json

from argos import getConfig

class TestArgosGetConfig(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"serverIp": "192.168.1.1", "serverPort": "9090", "whitelist": ["Test"], "blacklist": ["Bad"]}')
    def test_getConfig_success(self, mock_file):
        expected_config = {
            "serverIp": "192.168.1.1",
            "serverPort": "9090",
            "whitelist": ["Test"],
            "blacklist": ["Bad"]
        }

        result = getConfig()

        self.assertEqual(result, expected_config)
        mock_file.assert_called_once_with("config.json", 'r')

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("argos.logger.error")
    def test_getConfig_file_not_found(self, mock_logger_error, mock_file):
        expected_fallback = {
            "serverIp": "127.0.0.1",
            "serverPort": "8888",
            "whitelist": [],
            "blacklist": []
        }

        result = getConfig()

        self.assertEqual(result, expected_fallback)
        mock_file.assert_called_once_with("config.json", 'r')
        mock_logger_error.assert_called_once_with("config.json not found.")

if __name__ == '__main__':
    unittest.main()
