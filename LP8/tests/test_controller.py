import unittest
import threading
import time
import http.client

from http.server import HTTPServer
from myapp import MyHandler

HOST = "localhost"
PORT = 8082

class TestController(unittest.TestCase):

    @classmethod
    
    # Starts the HTTP server in a separate daemon thread so it can handle requests during controller tests
    def setUpClass(cls):
        
        def start_server():
            server = HTTPServer((HOST, PORT), MyHandler)
            server.serve_forever()

        cls.server_thread = threading.Thread(
            target=start_server, daemon=True
        )
        cls.server_thread.start()

        # Gives the server time to start before running tests
        time.sleep(0.5)

    # Sends an HTTP GET request to the test server and returns the response status code and body
    def make_request(self, path):
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        conn.close()
        return response.status, body

    # checks that / route returns HTTP 200 and renders the main page
    def test_index_route(self):
        status, body = self.make_request("/")
        self.assertEqual(status, 200)
        self.assertIn("CurrenciesListApp", body)

    # checks that /users route returns HTTP 200 and renders users list
    def test_users_route(self):
        status, body = self.make_request("/users")
        self.assertEqual(status, 200)
        self.assertIn("Иван", body)
        self.assertIn("Мария", body)

    # checks that /currencies route returns HTTP 200 and renders currencies page
    def test_currencies_route(self):
        status, body = self.make_request("/currencies")
        self.assertEqual(status, 200)
        self.assertIn("USD", body)
        self.assertIn("EUR", body)

    # checks correct handling of query parameter /user?id=...
    def test_user_query_param(self):
        status, body = self.make_request("/user?id=1")
        self.assertEqual(status, 200)
        self.assertIn("Иван", body)

if __name__ == "__main__":
    unittest.main()
