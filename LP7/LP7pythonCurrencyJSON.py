import requests
from xml.etree import ElementTree as ET
import sys
import functools
import logging
import traceback
from typing import Callable, Any

def logger(func=None, *, handle=sys.stdout):
    """Parameterizable logging decorator - logging function's calls/results/exceptions
    Can be used with or without parameters:
        @logger
        @logger(handle=my_logger)
    Keyword arguments:
        func : Callable | None. Function that is decorated
        handle : io.TextIOBase | logging.Logger. Destination for logging output. Can be:
            - Not specified. As default log will be wrote into console
            - File-like object. Log will be wrote into space of handle
            - logging.Logger object. Log will be wrote into space of logger
    Returns:
        Wrapped function with added logging behavior
    """
    def _is_logging_logger(obj: Any) -> bool:
        """ Function for definition type of handle 
        Keyword arguments:
            obj - handle that was chosen
        Returns:
            True - if obj belongs to logging.Logger class 
            False - if obj doesn't belong to logging.Logger class 
        """
        return isinstance(obj, logging.Logger)

    def _make_decorator(func_to_decorate:Callable)->Callable:
        """Create wrapper for decorated function
        Keyword arguments:
            func_to_decorate - function that will be wrapped with logging logic
        Returns:
            wrapper function that logs:
            - function call start and arguments
            - return value on success,
            - exception type and message on error
        """
        # save signature/information about function
        @functools.wraps(func_to_decorate)
        def wrapper(*args, **kwargs)->Any:
            """Execute wrapped function with added logging.
            Keyword arguments:
                *args, **kwargs - Positional and keyword arguments forwarded 
                directly to the original decorated function.
            Returns:
                Whatever decorated function returns
            """
            # preparing arguments for representation
            try:
                args_repr = ", ".join(repr(a) for a in args) if args else ""
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items()) if kwargs else ""
                all_args = ", ".join(filter(None, (args_repr, kwargs_repr)))
            except Exception:
                # if repr of argument led to error
                all_args = "<error during representation of arguments>"
            # forming INFO message
            func_name = func_to_decorate.__name__
            start_msg = f"INFO: Calling {func_name}({all_args})"
            # choosing of logging space
            if _is_logging_logger(handle):
                handle.info(start_msg)
            else:
                handle.write(start_msg + "\n")
            # trying to execute function
            try:
                result = func_to_decorate(*args, **kwargs)
            except Exception as exc:
                # forming exception message 
                exc_type_name = type(exc).__name__
                exc_text = f"{exc_type_name}: {exc}"
                error_msg = f"ERROR: Exception in {func_name}: {exc_text}"
                tb = traceback.format_exc()
                # logging exception
                if _is_logging_logger(handle):
                    handle.error(error_msg + "\n" + tb)
                else:
                    handle.write(error_msg + "\n")
                    handle.write(tb + "\n")
                raise
            else:
                # logging result
                end_msg = f"INFO: {func_name} returned {result!r}"
                if _is_logging_logger(handle):
                    handle.info(end_msg)
                else:
                    handle.write(end_msg + "\n")
                return result

        return wrapper

    # if function is called with @logger
    if func is not None:
        return _make_decorator(func)

    # if function is called with @logger(...)
    def _decorator_with_params(f:Callable)->Callable:
        """Receives the function being decorated and applies `_make_decorator` 
           to actually wrap it
        Keyword arguments:
            f - function that will be decorated
        Returns:
            Wrapped version of `f` with logging behavior applied
        """
        return _make_decorator(f)

    return _decorator_with_params

#Creating logger that will write logs into file
file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)
#Creating handler that writes into file
handler = logging.FileHandler("currency.log", encoding="utf-8")
handler.setLevel(logging.INFO)
#Setting format of log for handler
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
#Connecting handler to logger
file_logger.addHandler(handler)

@logger(handle=file_logger)
def get_currencies(currency_codes: list,
                   url: str = 'https://www.cbr-xml-daily.ru/daily_json.js',
                   handle=sys.stdout) -> dict:
    """Fetch currency values from Central Bank of Russia (CBR) API by sending
    GET-request to CBR JSON API.
    Keyword arguments:
        currency_codes - list of currency alphabetic codes (e.g., ["USD", "EUR"])
        url - URL of CBR JSON endpoint. Defaults to official daily rate API
        handle - direction for print(...,file=handle) of ValueError/KeyError. Defaults = console
    Returns:
        Dictionary with currency codes = values. For example:
        {"USD": 93.52, "ZZZ": "Код валюты 'ZZZ' не найден."}
    """
    dict = {}

    # trying to send GET-request to CBR
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    # processing exception
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.ConnectionError(f"Ошибка при запросе к API: {e}")
    else:
        # checking if API returned correct json
        try:
            data = response.json()
        except ValueError:
            print("ValueError: API вернул некорректный JSON", file=handle)
            dict = {ValueError: "API вернул некорректный JSON"}
            return dict
        
        # decoding JSON
        data = response.json()          
        valutes = data.get("Valute")

        # parsing codes and forming code=value element into dict
        if valutes is None:
            print("KeyError: Ключа Valute не существует", file=handle)
            dict = {KeyError: "Ключа Valute не существует"}
            return dict
        for code in currency_codes:
            if code not in valutes:
                print(f"Код валюты '{code}' не найден.", file=handle)
                dict[code] = f"Код валюты '{code}' не найден."
            else:
                dict[code] = valutes[code]["Value"]

        return dict
