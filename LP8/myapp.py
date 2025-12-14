from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import Author, App, User, Currency, User_Currency
from utils.currencies_api import get_currencies

# Jinja2 environment used for loading and rendering HTML templates.
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# HTML templates used by the application.
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")
template_user = env.get_template("user.html")
template_author = env.get_template("author.html")

# Application author information.
main_author = Author("Данила Эрцеговац", "P4150")

# Application metadata.
app = App("CurrenciesListApp", "1.0", main_author)

# List of application users.
users = [
    User("1", "Иван"),
    User("2", "Мария")
]

# List of supported currencies.
currencies = [
    Currency("R01010", "840", "USD", "Доллар США", 0, 1),
    Currency("R01239", "978", "EUR", "Евро", 0, 1)
]

# User-to-currency subscriptions.
subscriptions = [
    User_Currency("1", users[0], currencies[0]),
    User_Currency("2", users[0], currencies[1])
]

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

        if path == "/":
            self.render_index()

        elif path == "/users":
            self.render_users()

        elif path == "/user":
            self.render_user(params)

        elif path == "/currencies":
            self.render_currencies()

        elif path == "/author":
            self.render_author()

        else:
            self.send_error(404, "Страница не найдена")

    def render_index(self)-> None:
        """Render and send the application index page.
        Returns:
            None
        """        
        html = template_index.render(
            myapp=app.name,
            version=app.version,
            author_name=main_author.name,
            group=main_author.group
        )
        self.respond(html)

    def render_users(self) -> None:
        """Render and send the users list page.
        Returns:
            None
        """
        html = template_users.render(users=users)
        self.respond(html)

    def render_user(self, params: dict) -> None:
        """Render and send a specific user's page.
        Args:
            params - dictionary of GET query parameters.
                Expected key - "id": user identifier (str)
        Returns:
            None
        """
        user_id = params.get("id", [None])[0]
        user = next((u for u in users if u.id == user_id), None)

        user_currencies = [
            uc.currency_id for uc in subscriptions if uc.user_id == user
        ]

        html = template_user.render(
            user=user,
            currencies=user_currencies
        )
        self.respond(html)

    def render_currencies(self) -> None:
        """Render and send the currencies page with updated exchange rates.
        Retrieves current exchange rates from an external API and updates
        currency values before rendering the page.
        Returns:
            None
        """
        codes = [c.char_code for c in currencies]
        rates = get_currencies(codes)

        for c in currencies:
            value = rates.get(c.char_code)
            if value and value.replace(',', '.').replace('.', '', 1).isdigit():
                c.value = float(value.replace(',', '.'))

        html = template_currencies.render(currencies=currencies)
        self.respond(html)

    def render_author(self) -> None:
        """Render and send the author information page.
        Returns:
            None
        """
        html = template_author.render(author=main_author)
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