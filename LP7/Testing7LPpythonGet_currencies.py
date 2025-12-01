import unittest
from unittest.mock import patch
from LP7pythonCurrency import get_currencies
import requests

class TestGetCurrencies(unittest.TestCase):

    @patch("LP7pythonCurrency.requests.get")
    def test_real_values(self, mock_get):
        """Checking correct return of real currency rate."""

        xml = """
        <ValCurs>
            <Valute>
                <CharCode>USD</CharCode>
                <Value>93,52</Value>
            </Valute>
            <Valute>
                <CharCode>EUR</CharCode>
                <Value>101,20</Value>
            </Valute>
        </ValCurs>
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.content = xml.encode("utf-8")

        result = get_currencies(["USD", "EUR"])

        self.assertEqual(result["USD"], "93,52")
        self.assertEqual(result["EUR"], "101,20")

    @patch("LP7pythonCurrency.requests.get")
    def test_unknown_currency(self, mock_get):
        """Checking behavior when requesting a non-existent currency."""

        xml = "<ValCurs></ValCurs>" 
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = xml.encode("utf-8")

        result = get_currencies(["ZZZ"])
        self.assertEqual(result["ZZZ"], "Код валюты 'ZZZ' не найден.")

    @patch("LP7pythonCurrency.requests.get")
    def test_connection_error(self, mock_get):
        """Check if ConnectionError is thrown when API is unavailable."""

        mock_get.side_effect = requests.exceptions.ConnectionError("Ошибка при запросе к API")

        with self.assertRaises(requests.exceptions.ConnectionError):
            get_currencies(["USD"])
if __name__ == "__main__":
    unittest.main()