import sqlite3


class DatabaseController:
    """
    Controller responsible for initializing and managing
    the SQLite in-memory database schema
    - creates database connection
    - initializes tables
    - does NOT contain business logic
    """

    def __init__(self):
        """
        Initialize SQLite in-memory database and create tables.
        """
        self.con = sqlite3.connect(':memory:')
        self.con.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Create all required database tables:
        - user
        - currency
        - user_currency
        """
        cur = self.con.cursor()

        cur.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
        """)

        cur.execute("""
            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            )
        """)

        self.con.commit()


class CurrencyRatesCRUD:
    """
    Data access controller (CRUD) for currency entity.
    - works directly with SQLite
    - uses parameterized queries
    - does NOT contain business logic
    """

    def __init__(self, con: sqlite3.Connection):
        """
        Initialize CRUD controller with database connection.
        Args:
            con: SQLite connection object
        """
        self.con = con

    # CREATE
    def create_many(self, data: list[dict]) -> None:
        """
        Insert multiple currencies into database.
        Args:
            data: list of dictionaries with currency fields
        """
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        self.con.executemany(sql, data)
        self.con.commit()

    def create_one(self, data: dict) -> None:
        """
        Insert a single currency into database.
        Args:
            data: dictionary with currency fields
        """
        self.create_many([data])

    # READ
    def read_all(self) -> list[dict]:
        """
        Retrieve all currencies from database.
        Returns:
            List of currency dictionaries
        """
        cur = self.con.execute("SELECT * FROM currency")
        return [dict(row) for row in cur.fetchall()]

    def read_by_code(self, char_code: str) -> dict | None:
        """
        Retrieve currency by alphabetic code.
        Args:
            char_code: currency CharCode (e.g. USD)
        Returns:
            Currency dictionary or None if not found
        """
        cur = self.con.execute(
            "SELECT * FROM currency WHERE char_code = ?",
            (char_code,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    # UPDATE
    def update(self, char_code: str, value: float) -> None:
        """
        Update currency value by CharCode.
        Args:
            char_code: currency CharCode
            value: new exchange rate
        """
        self.con.execute(
            "UPDATE currency SET value = ? WHERE char_code = ?",
            (value, char_code)
        )
        self.con.commit()

    # DELETE
    def delete(self, currency_id: int) -> None:
        """
        Delete currency by its ID.
        Args:
            currency_id: currency primary key
        """
        self.con.execute(
            "DELETE FROM currency WHERE id = ?",
            (currency_id,)
        )
        self.con.commit()

