import logging
import math
from functools import wraps
from typing import Callable, Any

# file Logger configuration
logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def logger_quadratic(func:Callable)->Callable:
    """Decorator that adds logging for quadratic equation solver:
        - Logs ``TypeError`` as ERROR
        - Logs ``ValueError`` as CRITICAL
        - Logs WARNING if discriminant < 0 (result is None)
        - Logs INFO for:
            * a single real root
            * two real roots
    Keyword arguments:
        func - function that should be decorated
    Returns:
        Wrapper function that logs execution details of quadratic solver
    """
    # save signature/information about function
    @wraps(func)
    def wrapper(*args, **kwargs)->Any:
        """Wrapper of quadratic solver
        Keyword arguments:
            *args, **kwargs - Positional and keyword arguments forwarded 
            directly to the original decorated function.
        Returns:
            Whatever decorated function returns
        """
        func_name = func.__name__
        # trying to execute function
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            # forming exception message
            exc_type_name = type(exc).__name__
            exc_text = f"{exc_type_name}: {exc}"
            error_msg = f"Exception in {func_name}: {exc_text}"
            # logging exception
            if exc_type_name == 'TypeError':
                logging.error(error_msg)
            if exc_type_name == 'ValueError':
                logging.critical(error_msg)
        else:
            # logging result
            if result is None:
                logging.warning("Discriminant < 0: no real roots")
            elif isinstance(result, (int, float)):
                logging.info(f"Single root = {result}")
            else:
                logging.info(f"1st root = {result[0]}, 2nd root = {result[1]}")
    return wrapper

@logger_quadratic
def solve_quadratic(a: float|int, b: float|int, c: float|int)-> None|float|tuple[float, float]:
    """Solve a quadratic equation ax^2 + bx + c = 0
    Keyword arguments:
        a - Quadratic coefficient (must not be zero)
        b - Linear coefficient
        c - Constant term
    Returns:
        Roots of quadratic equation depending on discriminant
    """
    # verifying correctness of arguments' types -> exception if types are wrong
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Parameter '{name}' must be a number, got: {value}")

    # verfying if a equals to zero -> exception if does
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero")
    # solving quadratic equation
    d = b*b - 4*a*c
    logging.debug(f"Discriminant: {d}")

    if d < 0:
        return None

    if d == 0:
        x = -b / (2*a)
        return x

    root1 = (-b + math.sqrt(d)) / (2*a)
    root2 = (-b - math.sqrt(d)) / (2*a)
    return root1, root2

solve_quadratic(0, 0, 3)