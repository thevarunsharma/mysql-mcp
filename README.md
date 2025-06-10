# Basic MySQL MCP

## Setup
### Database configs
Create a `config.yaml` in the project root with the following format

```
DATABASE:
  driver: <driver>
  user: <username>
  password: <password>
  host: <mysql_hostname>
  database: <db_name>
  port: <db_port>
  # following section is optional
  # required if you are using ssl based db authentication
  ssl:
    cert: "/path/to/cert"       # client certificate
    key: "/path/to/key"         # client private key
    ca: "/path/to/ca-bundle"    # certificate authority
```

### Install dependencies
* Make sure your using `python 3.10+`
* Create and activate the virtual environment and install python dependencies:
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run MCP server
```
source env/bin/activate
python server.py
```
The server will start running at `http://127.0.0.1:8000`

## Add MCP server to VS Code
[Follow these steps to add the local MCP server to VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server-to-your-user-settings)

Set `http://127.0.0.1:8000/sse` as the `url` value
