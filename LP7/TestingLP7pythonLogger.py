import unittest
import io
import logging
import requests
from LP7pythonCurrencyXML import logger, get_currencies

class TestLoggerAllInOne(unittest.TestCase):
    # Test of Success
    def test_logging_success(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def test_function(x, y):
            return x + y

        result = test_function(2, 3)
        self.assertEqual(result, 5)

        logs = stream.getvalue()

        self.assertIn("INFO: Calling test_function(2, 3)", logs)
        self.assertIn("INFO: test_function returned 5", logs)

    # Test of Fail
    def test_logging_error(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def faulty(x):
            raise RuntimeError("RuntimeError")

        with self.assertRaises(RuntimeError):
            faulty(10)

        logs = stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("RuntimeError: RuntimeError", logs)

    # Test from task (ConnectionError)
    def test_stream_write_connection_error(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        with self.assertRaises(requests.exceptions.ConnectionError):
            wrapped()

        logs = stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)

    # Testing usage of logging.Loggeras handle
    def test_logger_with_logging_object(self):
        log_obj = logging.getLogger("test_logger")
        stream = io.StringIO()

        handler = logging.StreamHandler(stream)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        log_obj.handlers = []
        log_obj.addHandler(handler)
        log_obj.setLevel(logging.INFO)

        @logger(handle=log_obj)
        def multiply(a):
            return a * 3

        multiply(4)

        logs = stream.getvalue()
        self.assertIn("INFO: Calling multiply(4)", logs)
        self.assertIn("INFO: multiply returned 12", logs)

    # Testing function without arguments
    def test_no_args(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def f():
            return "ok"

        res = f()
        self.assertEqual(res, "ok")

        logs = stream.getvalue()
        self.assertIn("Calling f()", logs)
        self.assertIn("returned 'ok'", logs)


if __name__ == "__main__":
    unittest.main()

