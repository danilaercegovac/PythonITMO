"""
Unit tests for DatabaseController and CurrencyRatesCRUD.
Tests CRUD operations on the in-memory SQLite database.
"""

import unittest
import sqlite3
from controllers.databasecontroller import DatabaseController, CurrencyRatesCRUD


class TestDatabaseController(unittest.TestCase):
    """Test cases for DatabaseController and CurrencyRatesCRUD."""

    def setUp(self):
        """Initialize in-memory database and CRUD controller."""
        self.db = DatabaseController()
        self.crud = CurrencyRatesCRUD(self.db.con)

    def test_create_and_read_one_currency(self):
        """Test inserting a single currency and reading it back."""
        data = {"num_code": "840", "char_code": "USD", "name": "Dollar", "value": 90.5, "nominal": 1}
        self.crud.create_one(data)
        currencies = self.crud.read_all()
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0]["char_code"], "USD")

    def test_create_many_and_read_all(self):
        """Test inserting multiple currencies."""
        data_list = [
            {"num_code": "840", "char_code": "USD", "name": "Dollar", "value": 90.5, "nominal": 1},
            {"num_code": "978", "char_code": "EUR", "name": "Euro", "value": 98.2, "nominal": 1}
        ]
        self.crud.create_many(data_list)
        currencies = self.crud.read_all()
        self.assertEqual(len(currencies), 2)

    def test_update_currency(self):
        """Test updating currency value."""
        self.crud.create_one({"num_code": "840", "char_code": "USD", "name": "Dollar", "value": 90, "nominal": 1})
        self.crud.update("USD", 91.5)
        currency = self.crud.read_by_code("USD")
        self.assertEqual(currency["value"], 91.5)

    def test_delete_currency(self):
        """Test deleting a currency by id."""
        self.crud.create_one({"num_code": "840", "char_code": "USD", "name": "Dollar", "value": 90, "nominal": 1})
        currency = self.crud.read_by_code("USD")
        self.crud.delete(currency["id"])
        self.assertIsNone(self.crud.read_by_code("USD"))


if __name__ == "__main__":
    unittest.main()
