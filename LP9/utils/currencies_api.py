import requests
from xml.etree import ElementTree as ET

def get_currencies(currency_codes: list, 
                   url: str = 'https://www.cbr.ru/scripts/XML_daily.asp') -> dict:
    """Fetch currency values from Central Bank of Russia (CBR) API by sending
    GET-request to CBR XML API
    Keyword arguments:
        currency_codes - list of currency alphabetic codes (e.g., ["USD", "EUR"])
        url - URL of CBR XML endpoint. Defaults to official daily rate API
    Returns:
        Dictionary with currency codes = values. For example:
        {"USD": "93,52", "ZZZ": "Код валюты 'ZZZ' не найден."}
    """
    dict = {}
    # trying to send GET-request to cbr
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    # processing exception
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.ConnectionError(f"Ошибка при запросе к API: {e}")
    else:
        # from XML bytes to XML-node for processing XML
        root = ET.fromstring(response.content)
        # parsing codes and forming code=value element into dict
        for code in currency_codes:
            if root.find(f".//Valute[CharCode='{code}']/Value") is None:
                dict[code] = f"Код валюты '{code}' не найден."
            else:
                dict[code] = root.find(f".//Valute[CharCode='{code}']/Value").text
        return dict