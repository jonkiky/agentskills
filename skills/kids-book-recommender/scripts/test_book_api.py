import os
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit, parse_qs
from book_api import build_request, NoRedirect


class BookApiTests(unittest.TestCase):
    def test_openlibrary(self):
        url = urlsplit(build_request("openlibrary", "The Wild Robot & friends").full_url)
        self.assertEqual(url.netloc, "openlibrary.org")
        self.assertEqual(parse_qs(url.query)["q"], ["The Wild Robot & friends"])

    @patch.dict(os.environ, {"GOOGLE_BOOKS_API_KEY": "test-key"})
    def test_google(self):
        url = urlsplit(build_request("google", "isbn:9780316381994").full_url)
        self.assertEqual(url.path, "/books/v1/volumes")
        self.assertEqual(parse_qs(url.query)["key"], ["test-key"])

    @patch.dict(os.environ, {"NYT_BOOKS_API_KEY": "test-key"})
    def test_nyt(self):
        self.assertTrue(urlsplit(build_request("nyt", "names").full_url).path.endswith("/lists/names.json"))
        self.assertTrue(urlsplit(build_request("nyt", "childrens-middle-grade-hardcover").full_url).path.endswith("/current/childrens-middle-grade-hardcover.json"))
        with self.assertRaises(ValueError):
            build_request("nyt", "../bad")

    @patch.dict(os.environ, {"LIBRARYTHING_API_KEY": "test-key"})
    def test_librarything(self):
        url = urlsplit(build_request("librarything", "9780316381994,0316381993").full_url)
        self.assertEqual(parse_qs(url.query)["isbns"], ["9780316381994,0316381993"])
        with self.assertRaises(ValueError):
            build_request("librarything", "not-isbn")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_key(self):
        with self.assertRaises(ValueError):
            build_request("nyt", "names")

    def test_empty_query(self):
        with self.assertRaises(ValueError):
            build_request("openlibrary", " ")

    def test_no_redirect(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, None, {}, "https://example.com"))


if __name__ == "__main__":
    unittest.main()
