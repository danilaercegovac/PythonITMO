from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from models import Author, App

from controllers.databasecontroller import DatabaseController, CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController

# Jinja2 environment used for loading and rendering HTML templates.
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# Application author information.
main_author = Author("Данила Эрцеговац", "P4150")

# Application metadata.
app = App("CurrenciesListApp", "2.0", main_author)

# Database controller initialization
db = DatabaseController() 
currency_crud = CurrencyRatesCRUD(db.con)

# Pre-fill database with initial currencies
currency_crud.create_many([
    {
        "num_code": "840",
        "char_code": "USD",
        "name": "Доллар США",
        "value": 90.5,
        "nominal": 1
    },
    {
        "num_code": "978",
        "char_code": "EUR",
        "name": "Евро",
        "value": 98.2,
        "nominal": 1
    }
])

db.con.commit()

# Business logic controllers
currency_controller = CurrencyController(currency_crud)

# Pages rendering controller
pages = PagesController(env, app, main_author, currency_controller)

class MyHandler(BaseHTTPRequestHandler):
    """ HTTP request handler for the web application.
    This class routes incoming GET requests to the appropriate
    page-rendering methods and returns HTML responses.
    """
    def do_GET(self)-> None:
        """Handle an incoming HTTP GET request.
        Parses the request URL and dispatches execution to the
        corresponding rendering method based on the request path.

        Returns:
            None
        """
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        html = ""

        try:
            if path == "/":
                html = pages.index()

            elif path == "/currencies":
                html = pages.currencies()

            elif path == "/author":
                html = pages.author_page()

            elif path == "/currency/create":
                currency_controller.create_currency(
                    char_code=params["char_code"][0],
                    name=params["name"][0],
                    num_code=params["num_code"][0],
                    nominal=int(params.get("nominal", [1])[0])
                )
                html = pages.currencies()

            elif path == "/currency/delete":
                currency_controller.delete_currency(
                    int(params["id"][0])
                )
                html = pages.currencies()

            elif path == "/currency/update":
                code, value = next(iter(params.items()))
                currency_controller.update_currency(
                    code, float(value[0])
                )
                html = pages.currencies()

            elif path == "/currency/show":
                print(currency_controller.list_currencies())
                html = pages.currencies()

            else:
                html = pages.render_error("Page not found")

        except (KeyError, ValueError):
            html = pages.render_error("Invalid input format")

        self.respond(html)

    def respond(self, html: str) -> None:
        """Send an HTTP response with HTML content.
        Args:
            html - HTML content to be sent to the client.
        Returns:
            None
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
    
    
    
#Starts the HTTP server on localhost at port 8080.
if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), MyHandler)
    print("Server started at http://localhost:8080")
    server.serve_forever()   