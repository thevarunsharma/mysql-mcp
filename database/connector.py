import urllib.parse
from conf import (
    load_config,
    DatabaseConfig
)
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import DBAPIError


class DbConnector:

    def __init__(self, is_test: bool = False):
        configs = load_config()
        if not hasattr(configs, "DATABASE"):
            raise KeyError("Configuration does not contain 'DATABASE' section.")
        self._db_conf = configs.DATABASE
        if is_test:
            self._db_url = "sqlite:///:memory:"  # Use in-memory SQLite for tests
            self.engine = create_engine(self._db_url)
        else:  
            self._db_url = self.url_from_conf(self._db_conf)
            self.engine = create_engine(
                self._db_url,
                connect_args={
                    "ssl": self._db_conf.ssl
                }
            )

    def url_from_conf(self, db_conf: DatabaseConfig) -> str:
        """
        Create a database URL from the configuration dictionary.

        Args:
            db_conf (dict): The database configuration dictionary.

        Returns:
            str: The database URL.
        """
        driver = db_conf.driver
        user = urllib.parse.quote(db_conf.user)
        password = urllib.parse.quote(db_conf.password)
        host = urllib.parse.quote(db_conf.host)
        port = urllib.parse.quote(str(db_conf.port))
        database = urllib.parse.quote(db_conf.database)
        return f"{driver}://{user}:{password}@{host}:{port}/{database}"

    @staticmethod
    def serialize_column(col: dict) -> dict:
        return {
            k: str(v) if isinstance(v, (type, object)) and not isinstance(v, (int, float, bool, type(None))) else v
            for k, v in col.items()
        }

    def show_tables(self) -> list[str]:
        """
        Show the tables in the database.
        Returns:
            list: A list of table names.
        """
        return inspect(self.engine).get_table_names()

    def describe_table(self, table: str) -> list[dict]:
        """
        Describe a table in the database.
        
        Args:
            table (str): The name of the table to describe.
        
        Returns:
            list: A list of dictionaries containing column information.
        """
        inspector = inspect(self.engine)
        if table not in inspector.get_table_names():
            return [{"Error": f"Table '{table}' does not exist."}]
        columns = inspector.get_columns(table)
        return [DbConnector.serialize_column(col) for col in columns]

    def execute_query(self, query: str) -> list[dict]:
        """
        Execute a SQL query and return the results.
        
        Args:
            query (str): The SQL query to execute.
        
        Returns:
            list: A list of dictionaries containing the query results.
            In case of an error, returns a list with a single dict containing error information.
        """
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(query))
            except DBAPIError as e:
                return [{"Error": str(e), "Query": query}]
            columns = result.keys()
            records = []
            for row in result.fetchall():
                records.append(DbConnector.serialize_column(dict(zip(columns, row))))
            return records
                