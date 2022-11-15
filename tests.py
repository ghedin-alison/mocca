import unittest
from unittest.mock import patch, Mock
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


if __name__ == "__main__":
    unittest.main()