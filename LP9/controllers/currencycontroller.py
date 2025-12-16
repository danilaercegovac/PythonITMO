from controllers.databasecontroller import CurrencyRatesCRUD
from utils.currencies_api import get_currencies


class CurrencyController:
    """
    Business-logic controller for currency operations.
    - validates input data
    - fetches actual exchange rates
    - delegates database operations to CRUD layer
    """

    def __init__(self, crud: CurrencyRatesCRUD):
        """
        Initialize currency controller.
        Args:
            crud: CurrencyRatesCRUD instance
        """
        self.crud = crud


    def list_currencies(self) -> list[dict]:
        """
        Retrieve all currencies.
        Returns:
            List of currency dictionaries
        """
        return self.crud.read_all()


    def create_currency(
        self,
        char_code: str,
        name: str,
        num_code: str,
        nominal: int = 1
    ) -> None:
        """
        Create new currency using actual rate from external API.
        Args:
            char_code: alphabetic currency code
            name: currency name
            num_code: numeric currency code
            nominal: currency nominal value
        """
        rates = get_currencies([char_code.upper()])
        value_raw = rates.get(char_code.upper())

        if not value_raw or not value_raw.replace(',', '.').replace('.', '', 1).isdigit():
            raise ValueError("Invalid currency code or value")

        value = float(value_raw.replace(',', '.'))

        self.crud.create_one({
            "num_code": num_code,
            "char_code": char_code.upper(),
            "name": name,
            "value": value,
            "nominal": nominal
        })


    def update_currency(self, char_code: str, value: float) -> None:
        """
        Update currency exchange rate.
        Args:
            char_code: currency CharCode
            value: new exchange rate
        """
        if value <= 0:
            raise ValueError("Invalid currency value")

        self.crud.update(char_code.upper(), value)


    def delete_currency(self, currency_id: int) -> None:
        """
        Delete currency by ID.

        Args:
            currency_id: currency primary key
        """
        if currency_id <= 0:
            raise ValueError("Invalid currency id")

        self.crud.delete(currency_id)
