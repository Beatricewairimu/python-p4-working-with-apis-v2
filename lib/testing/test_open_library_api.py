import unittest
from unittest.mock import patch, MagicMock
from ..open_library_api import OpenLibraryAPI

class TestOpenLibraryAPI(unittest.TestCase):
    def setUp(self):
        self.api = OpenLibraryAPI()
        self.mock_response = {
            "docs": [{
                "title": "Test Book",
                "author_name": ["Author One", "Author Two"]
            }]
        }

    @patch('requests.get')
    def test_search_books_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.api.search_books("Test Book")
        self.assertEqual(result, self.mock_response)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_search_books_failure(self, mock_get):
        mock_get.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            self.api.search_books("Test Book")

    def test_format_book_result(self):
        formatted = self.api.format_book_result(self.mock_response["docs"][0])
        self.assertEqual(
            formatted,
            "Title: Test Book\nAuthor(s): Author One, Author Two"
        )

    def test_format_book_result_missing_fields(self):
        test_data = {"title": "No Author Book"}
        formatted = self.api.format_book_result(test_data)
        self.assertEqual(
            formatted,
            "Title: No Author Book\nAuthor(s): Unknown Author"
        )

if __name__ == "__main__":
    unittest.main()
