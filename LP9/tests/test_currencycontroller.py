"""
Unit tests for CurrencyController.
Tests all CRUD operations with mocked dependencies.
"""

import unittest
from unittest.mock import MagicMock, patch

from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import CurrencyRatesCRUD


class TestCurrencyController(unittest.TestCase):
    """
    Test suite for CurrencyController CRUD operations.

    Uses mocks to isolate controller logic from
    database and external API dependencies.
    """

    def setUp(self):
        """
        Prepare a mocked CRUD layer before each test.

        The 'spec' argument ensures that only existing methods
        of CurrencyRatesCRUD can be accessed.
        """
        self.mock_crud = MagicMock(spec=CurrencyRatesCRUD)
        self.controller = CurrencyController(self.mock_crud)

    @patch("controllers.currencycontroller.get_currencies")
    def test_create_currency_success(self, mock_get):
        """
        Test successful creation of a currency.

        Scenario:
        - External API returns a valid numeric value
        - CurrencyController parses and converts the value correctly
        - CRUD layer is called with valid normalized data
        """
        mock_get.return_value = {"USD": "90,5"}

        self.controller.create_currency("USD", "Dollar", "840")

        self.mock_crud.create_one.assert_called_once()
        data = self.mock_crud.create_one.call_args[0][0]

        self.assertEqual(data["char_code"], "USD")
        self.assertEqual(data["name"], "Dollar")
        self.assertEqual(data["num_code"], "840")
        self.assertEqual(data["nominal"], 1)
        self.assertEqual(data["value"], 90.5)

    @patch("controllers.currencycontroller.get_currencies")
    def test_create_currency_invalid_code(self, mock_get):
        """
        Test that ValueError is raised when currency code
        is not found by the external API.
        """
        mock_get.return_value = {"ZZZ": "Currency not found"}

        with self.assertRaises(ValueError):
            self.controller.create_currency("ZZZ", "Unknown", "999")

        self.mock_crud.create_one.assert_not_called()

    def test_list_currencies(self):
        """
        Test that list_currencies returns data provided
        by the CRUD layer without modification.
        """
        self.mock_crud.read_all.return_value = [{"char_code": "USD"}]

        result = self.controller.list_currencies()

        self.assertEqual(result[0]["char_code"], "USD")
        self.mock_crud.read_all.assert_called_once()

    def test_update_currency(self):
        """
        Test that updating a currency delegates
        the operation to the CRUD layer.
        """
        self.controller.update_currency("USD", 91.5)
        self.mock_crud.update.assert_called_once_with("USD", 91.5)

    def test_delete_currency(self):
        """
        Test that deleting a currency delegates
        the operation to the CRUD layer.
        """
        self.controller.delete_currency(1)
        self.mock_crud.delete.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()