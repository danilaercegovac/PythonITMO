import unittest
from unittest.mock import patch, MagicMock
from LP7pythonCurrencyJSON import get_currencies
import requests
import io


class TestGetCurrenciesJSON(unittest.TestCase):

    @patch("LP7pythonCurrencyJSON.requests.get")
    def test_real_values(self, mock_get):
        """Checking correct return of real currency."""

        json_data = {
            "Valute": {
                "USD": {"Value": 93.52},
                "EUR": {"Value": 101.20}
            }
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_data
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])

        self.assertEqual(result["USD"], 93.52)
        self.assertEqual(result["EUR"], 101.20)

    @patch("LP7pythonCurrencyJSON.requests.get")
    def test_unknown_currency(self, mock_get):
        """Checking behavior when requesting a non-existent currency."""

        json_data = {"Valute": {}}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_data
        mock_get.return_value = mock_response

        result = get_currencies(["ZZZ"])

        self.assertEqual(result["ZZZ"], "Код валюты 'ZZZ' не найден.")

    @patch("LP7pythonCurrencyJSON.requests.get")
    def test_missing_valute_key(self, mock_get):
        """Checking behavior when JSON has no 'Valute' key."""

        json_data = {"WrongKey": "Something"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_data
        mock_get.return_value = mock_response

        output = io.StringIO()
        result = get_currencies(["USD"], handle=output)

        self.assertIn("KeyError: Ключа Valute не существует", output.getvalue())
        self.assertIn(KeyError, result)
        self.assertEqual(result[KeyError], "Ключа Valute не существует")

    @patch("LP7pythonCurrencyJSON.requests.get")
    def test_incorrect_json_format(self, mock_get):
        """Checking handling of ValueError (invalid JSON)."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("API вернул некорректный JSON")
        mock_get.return_value = mock_response

        output = io.StringIO()
        result = get_currencies(["USD"], handle=output)

        self.assertIn("ValueError: API вернул некорректный JSON", output.getvalue())
        self.assertIn(ValueError, result)
        self.assertEqual(result[ValueError], "API вернул некорректный JSON")

    @patch("LP7pythonCurrencyJSON.requests.get")
    def test_connection_error(self, mock_get):
        """Check if ConnectionError is thrown when API is unavailable."""

        mock_get.side_effect = requests.exceptions.ConnectionError("Ошибка при запросе к API")

        with self.assertRaises(requests.exceptions.ConnectionError):
            get_currencies(["USD"])


if __name__ == "__main__":
    unittest.main()
