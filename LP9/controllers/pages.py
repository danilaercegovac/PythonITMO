from jinja2 import Environment
from models import App, Author
from controllers.currencycontroller import CurrencyController

class PagesController:
    """
    Controller responsible for rendering HTML pages
    - renders templates via Jinja2
    - does NOT contain business logic
    - does NOT access database directly
    """

    def __init__(
        self,
        env: Environment,
        app: App,
        author: Author,
        currency_controller: CurrencyController
    ):
        """
        Initialize pages controller.
        Args:
            env: Jinja2 Environment
            app: application metadata
            author: application author
            currency_controller: currency business controller
        """
        self.env = env
        self.app = app
        self.author = author
        self.currency_controller = currency_controller

    def index(self) -> str:
        """
        Render index page.
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template("index.html")
        return template.render(
            myapp=self.app.name,
            version=self.app.version,
            author_name=self.author.name,
            group=self.author.group
        )

    def author_page(self) -> str:
        """
        Render author information page.
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template("author.html")
        return template.render(author=self.author)

    def currencies(self) -> str:
        """
        Render currencies list page.
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template("currencies.html")
        currencies = self.currency_controller.list_currencies()
        return template.render(currencies=currencies)

    def render_error(self, message: str) -> str:
        """
        Render error page.
        Args:
            message: error description
        Returns:
            Rendered HTML string
        """
        template = self.env.get_template("error.html")
        return template.render(message=message)