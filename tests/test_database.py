import pytest
from conf import DatabaseConfig
from database.connector import DbConnector
from sqlalchemy import text


@pytest.fixture(scope='class')
def db_connector():
    """Fixture to create a DbConnector instance for testing."""
    db_connector = DbConnector(is_test=True)
    engine = db_connector.engine
    # Mock data for testing
    mock_tables = ['users', 'orders', 'products']
    with engine.connect() as connection:
        for table in mock_tables:
            connection.execute(text(f"CREATE TABLE {table} (id INT, name VARCHAR(100))"))
        connection.execute(text("INSERT INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob')"))
        connection.commit()
    return db_connector


class TestDbConnection:

    def test_url_from_conf(self, db_connector):
        """Test the URL generation from configuration."""
        db_conf = DatabaseConfig(
            driver='mysql+pymysql',
            user='test_user',
            password='test_p@ss',
            host='localhost',
            port=3306,
            database='test_db'
        )
        expected_url = "mysql+pymysql://test_user:test_p%40ss@localhost:3306/test_db"
        assert db_connector.url_from_conf(db_conf) == expected_url
    
    def test_show_tables(self, db_connector):
        """Test showing tables in the database."""
        result = db_connector.show_tables()
        assert isinstance(result, list)
        assert set(result) == {'users', 'orders', 'products'}
    
    def test_describe_table(self, db_connector):
        """Test describing a table in the database."""
        result = db_connector.describe_table('users')
        assert isinstance(result, list)
        assert len(result) > 0
        for column in result:
            assert column.get('name') in ['id', 'name']

    def test_execute_query(self, db_connector):
        """Test executing a SQL query."""
        query = "SELECT * FROM users ORDER by id"
        result = db_connector.execute_query(query)
        assert isinstance(result, list)
        # Assuming the table 'users' has at least one row
        assert len(result) >= 0
        assert result == [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]
    
    def test_execute_invalid_query(self, db_connector):
        """Test executing an invalid SQL query."""
        query = "SELECT * FROM non_existing_table"
        result = db_connector.execute_query(query)
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'Error' in result[0]
        assert 'Query' in result[0]
        assert result[0]['Query'] == query

    def test_serialize_column(self, db_connector):
        """Test serializing a column."""
        col = {'name': 'id', 'type': int, 'nullable': False}
        serialized_col = db_connector.serialize_column(col)
        assert isinstance(serialized_col, dict)
        assert serialized_col['name'] == 'id'
        assert serialized_col['type'] == "<class 'int'>"
        assert serialized_col['nullable'] is False
