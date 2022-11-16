import unittest
from unittest.mock import patch, Mock
import requests.exceptions
from requests.exceptions import Timeout, HTTPError
from main import len_joke, get_joke

class TestJoke(unittest.TestCase):

    @patch('main.get_joke')
    def test_len_joke(self, mock_get_joke):
        mock_get_joke.return_value = "twenty-five"
        self.assertEqual(len_joke(), 11)
    @patch('main.requests')
    def test_get_joke(self, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'value': {
            'joke': 'test with mock'
        }}
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_joke(), 'test with mock')

    @patch('main.requests')
    def test_fail_get_joke(self, mock_requests):
        mock_response = Mock(status_code = 403)
        mock_response.json.return_value = {'value': {
            'joke': 'test with mock'
        }}
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_joke(), 'No jokes')

    @patch('main.requests')
    def test_get_joke_raises_timeout_exception(self, mock_requests):
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.side_effect = Timeout('Seems that the server is down')
        self.assertEqual(get_joke(), 'No jokes')

    @patch('main.requests')
    def test_get_joke_raise_for_status(self, mock_requests):
        mock_response = Mock(status_code=403)
        mock_response.raise_for_status.side_effect = HTTPError('Something went wrong')
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_joke(), 'HTTPError was raised')
        # self.assertRaises(HTTPError, get_joke())

if __name__ == "__main__":
    unittest.main()