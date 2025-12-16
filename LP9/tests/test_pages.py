"""
Unit tests for PagesController.
Ensures templates render correctly with provided data.
Uses mocked CurrencyController to isolate business logic.
"""

import unittest
from unittest.mock import MagicMock

from jinja2 import Environment, DictLoader

from controllers.pages import PagesController
from controllers.currencycontroller import CurrencyController
from models import App, Author


class TestPagesController(unittest.TestCase):
    """
    Test suite for PagesController template rendering.
    """

    def setUp(self):
        """
        Setup a minimal Jinja2 environment with inline templates
        and a mocked CurrencyController.
        """
        templates = {
            "index.html": "<h1>{{ myapp }}</h1>",
            "author.html": "<p>{{ author.name }}</p>",
            "currencies.html": "{% for c in currencies %}{{ c.char_code }}{% endfor %}",
            "error.html": "{{ message }}"
        }

        env = Environment(loader=DictLoader(templates))

        author = Author("Author", "GROUP1")
        app = App("TestApp", "1.0", author)

        mock_currency = MagicMock(spec=CurrencyController)
        mock_currency.list_currencies.return_value = [{"char_code": "USD"}]

        self.pages = PagesController(env, app, author, mock_currency)

    def test_index_page(self):
        """
        Test that index page renders application name.
        """
        html = self.pages.index()
        self.assertIn("TestApp", html)

    def test_author_page(self):
        """
        Test that author page renders author's name.
        """
        html = self.pages.author_page()
        self.assertIn("Author", html)

    def test_currencies_page(self):
        """
        Test that currencies page renders
        currency data provided by the controller.
        """
        html = self.pages.currencies()
        self.assertIn("USD", html)

    def test_render_error_page(self):
        """
        Test that error page renders provided error message.
        """
        html = self.pages.render_error("Error!")
        self.assertIn("Error!", html)


if __name__ == "__main__":
    unittest.main()