import unittest
from models import Author, App, User, Currency


class TestModels(unittest.TestCase):

    # Author

    # checks valid setters and getters of the Author model
    def test_author_valid(self):
        author = Author("Данила", "P4150")
        self.assertEqual(author.name, "Данила")
        self.assertEqual(author.group, "P4150")

    # checks raising ValueError for invalid author name
    def test_author_invalid_name(self):
        with self.assertRaises(ValueError):
            Author("A", "P4150")

    # checks raising ValueError for invalid author group
    def test_author_invalid_group(self):
        with self.assertRaises(ValueError):
            Author("Данила", "123")

    # App

    # checks valid setters and getters of the App model
    def test_app_valid(self):
        author = Author("Данила", "P4150")
        app = App("MyApp", "1.0", author)

        self.assertEqual(app.name, "MyApp")
        self.assertEqual(app.version, "1.0")
        self.assertEqual(app.author, author)

    # checks raising ValueError for invalid application name
    def test_app_invalid_name(self):
        author = Author("Данила", "P4150")
        with self.assertRaises(ValueError):
            App("", "1.0", author)

    # checks raising ValueError for invalid application version
    def test_app_invalid_version(self):
        author = Author("Данила", "P4150")
        with self.assertRaises(ValueError):
            App("MyApp", "", author)

    # checks raising TypeError when author is not an Author instance
    def test_app_invalid_author_type(self):
        with self.assertRaises(TypeError):
            App("MyApp", "1.0", "not_author")

    # User

    # checks valid setters and getters of the User model
    def test_user_valid(self):
        user = User("1", "Иван")
        self.assertEqual(user.id, "1")
        self.assertEqual(user.name, "Иван")

    # checks raising ValueError for invalid user id
    def test_user_invalid_id(self):
        with self.assertRaises(ValueError):
            User("", "Иван")

    # checks raising ValueError for invalid user name
    def test_user_invalid_name(self):
        with self.assertRaises(ValueError):
            User("1", "A")

    # Currency

    # checks valid setters and getters of the Currency model
    def test_currency_valid(self):
        currency = Currency("R01010", "840", "usd", "US Dollar", 75.5, 1)

        self.assertEqual(currency.id, "R01010")
        self.assertEqual(currency.num_code, "840")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "US Dollar")
        self.assertEqual(currency.value, 75.5)
        self.assertEqual(currency.nominal, 1)

    # checks raising ValueError for invalid currency id
    def test_currency_invalid_id(self):
        with self.assertRaises(ValueError):
            Currency("123", "840", "USD", "Dollar", 1.0, 1)

    # checks raising ValueError for invalid numeric code
    def test_currency_invalid_num_code(self):
        with self.assertRaises(ValueError):
            Currency("R01010", "84", "USD", "Dollar", 1.0, 1)

    # checks raising ValueError for invalid character code
    def test_currency_invalid_char_code(self):
        with self.assertRaises(ValueError):
            Currency("R01010", "840", "US", "Dollar", 1.0, 1)

    # checks raising ValueError for invalid currency name
    def test_currency_invalid_name(self):
        with self.assertRaises(ValueError):
            Currency("R01010", "840", "USD", "D", 1.0, 1)

    # checks raising TypeError for invalid currency value type
    def test_currency_invalid_value_type(self):
        with self.assertRaises(TypeError):
            Currency("R01010", "840", "USD", "Dollar", "abc", 1)

    # checks raising TypeError for invalid nominal type
    def test_currency_invalid_nominal_type(self):
        with self.assertRaises(TypeError):
            Currency("R01010", "840", "USD", "Dollar", 1.0, "1")


if __name__ == "__main__":
    unittest.main()
