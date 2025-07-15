import json
from mcp.server.fastmcp import FastMCP
from database.connector import DbConnector

mcp = FastMCP("mysql_client")


@mcp.tool()
async def show_tables() -> str:
    """
    Show the tables in the database.
    
    Returns:
        str: A JSON string containing the list of table names.
    """
    db_connector = DbConnector()
    tables = db_connector.show_tables()
    return json.dumps(tables)


@mcp.tool()
async def describe_table(table: str) -> str:
    """
    Describe a table in the database.
    
    Args:
        table (str): The name of the table to describe.
    
    Returns:
        str: A JSON string containing the column information of the table.
    """
    db_connector = DbConnector()
    description = db_connector.describe_table(table)
    return json.dumps(description)


@mcp.tool()
async def execute_query(query: str) -> str:
    """
    Execute a SQL query and return the results.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        str: A JSON string containing the query results.
    """
    db_connector = DbConnector()
    result = db_connector.execute_query(query)
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run(transport="sse")
