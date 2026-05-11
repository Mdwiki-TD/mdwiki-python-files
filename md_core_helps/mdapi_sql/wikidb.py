import os
import pymysql


class Database:
    """A class for interacting with a database.
    Attributes:
        _connection (pymysql.connections.Connection): A connection to the database.
        _query (str): The current SQL query.
        result (list): The result of the last executed query.
    """

    def __init__(self):
        """Initializes the Database with the connection and query attributes set to None, and result set to an empty list."""
        super().__init__()
        self._connection = None
        self._query = ""
        self.result = []

    @property
    def connection(self):
        """Returns the current connection to the database. If none exists, a new connection is established and returned.
        Returns:
            pymysql.connections.Connection: A connection to the database.
        """
        # db_name = "arwiki"  # _config.db_name_format.format("arwiki")
        db_name = "arwiki_p"

        db_hostname_format = '{0}.analytics.db.svc.wikimedia.cloud'  # _config.db_hostname_format
        db_connect_file = os.path.join(os.path.expanduser('~'), '.my.cnf')  # _config.db_connect_file

        if self._connection is not None:
            return self._connection
        else:
            return pymysql.connect(
                host=db_hostname_format.format("arwiki"),
                read_default_file=db_connect_file,
                db=db_name,
                charset="utf8mb4",
                port=3306,
                cursorclass=pymysql.cursors.DictCursor,
            )

    @property
    def query(self):
        """Returns the current SQL query.
        Returns:
            str: The current SQL query.
        """
        return self._query

    @query.setter
    def query(self, value):
        """Sets the current SQL query and replaces placeholders with the appropriate values.
        Args:
            value (str): The new SQL query.
        """
        self._query = value

    def get_content_from_database(self):
        """Executes the current SQL query and stores the result in the `result` attribute.
        Raises:
            pymysql.err.OperationalError: If a connection to the database cannot be established.
        """
        try:
            # Create a cursor page
            with self.connection.cursor() as cursor:
                # Execute the SELECT statement
                cursor.execute(self._query)
                # Fetch all the rows of the result
                self.result = cursor.fetchall()
        finally:
            # Close the connection
            self.connection.close()

    @connection.setter
    def connection(self, value):
        """Sets the current connection to the database.
        Args:
            value (pymysql.connections.Connection): The new connection to the database.
        """
        self._connection = value
