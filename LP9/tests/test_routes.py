"""
Integration-like tests for HTTP routes in MyHandler.
Uses mock PagesController and CurrencyController to isolate HTTP server behavior.
"""

import unittest
from unittest.mock import MagicMock, patch

from myapp import MyHandler


class TestMyHandler(unittest.TestCase):
    """
    Test suite for MyHandler GET routing.
    """

    def setUp(self):
        """
        Create a MyHandler instance without invoking
        BaseHTTPRequestHandler initialization.

        The respond method is mocked to capture output.
        """
        self.handler = MyHandler.__new__(MyHandler)
        self.handler.respond = MagicMock()

    @patch("myapp.pages")
    def test_root_route_calls_index(self, mock_pages):
        """
        Test that GET '/' route calls PagesController.index
        and returns rendered HTML.
        """
        mock_pages.index.return_value = "INDEX PAGE"

        self.handler.path = "/"
        self.handler.do_GET()

        self.handler.respond.assert_called_once_with("INDEX PAGE")

    @patch("myapp.pages")
    def test_not_found_route_returns_error(self, mock_pages):
        """
        Test that unknown routes return an error page.
        """
        mock_pages.render_error.return_value = "ERROR PAGE"

        self.handler.path = "/unknown"
        self.handler.do_GET()

        self.handler.respond.assert_called_once_with("ERROR PAGE")


if __name__ == "__main__":
    unittest.main()
