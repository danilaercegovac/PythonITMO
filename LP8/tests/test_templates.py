import unittest
from jinja2 import Environment, FileSystemLoader
from models import User, Currency, Author


class TestTemplates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env = Environment(
            loader=FileSystemLoader("templates")
        )

    # checks correct rendering of variables in index.html
    def test_index_template(self):
        template = self.env.get_template("index.html")
        html = template.render(
            myapp="TestApp",
            version="1.0",
            author_name="Данила",
            group="P4150"
        )

        self.assertIn("TestApp", html)
        self.assertIn("1.0", html)
        self.assertIn("Данила", html)
        self.assertIn("P4150", html)

    # checks correct rendering of user list loop in users.html
    def test_users_template_loop(self):
        template = self.env.get_template("users.html")
        users = [User("1", "Иван"), User("2", "Мария")]
        html = template.render(users=users)

        self.assertIn("Иван", html)
        self.assertIn("Мария", html)

    # checks correct rendering of currency list loop in currencies.html
    def test_currencies_template_loop(self):
        template = self.env.get_template("currencies.html")
        currencies = [
            Currency("R01010", "840", "USD", "Dollar", 75.0, 1),
            Currency("R01239", "978", "EUR", "Euro", 80.0, 1)
        ]
        html = template.render(currencies=currencies)

        self.assertIn("USD", html)
        self.assertIn("EUR", html)
        self.assertIn("75.0", html)
        self.assertIn("80.0", html)

    # checks conditional rendering when user has no currency subscriptions
    def test_user_template_without_currencies(self):
        template = self.env.get_template("user.html")
        user = User("1", "Иван")
        html = template.render(user=user, currencies=[])

        self.assertIn("не подписан", html.lower())

    # checks conditional rendering when user has currency subscriptions
    def test_user_template_with_currencies(self):
        template = self.env.get_template("user.html")
        user = User("1", "Иван")
        currencies = [
            Currency("R01010", "840", "USD", "Dollar", 75.0, 1)
        ]
        html = template.render(user=user, currencies=currencies)

        self.assertIn("Dollar", html)
        self.assertIn("USD", html)
        self.assertIn("75.0", html)

    # checks correct rendering of variables in author.html
    def test_author_template(self):
        template = self.env.get_template("author.html")
        author = Author("Данила", "P4150")
        html = template.render(author=author)

        self.assertIn("Данила", html)
        self.assertIn("P4150", html)


if __name__ == "__main__":
    unittest.main()

