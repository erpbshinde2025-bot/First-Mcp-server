# First MCP Server — Claude + Database Integration

A hands-on implementation of a **Model Context Protocol (MCP) server** built in Python, connected to a database and integrated with **Claude Desktop**. This project demonstrates how to expose database context to an LLM through the MCP standard, enabling Claude to answer natural language questions directly against live data.

---

## What is MCP?

The **Model Context Protocol (MCP)** is an open standard that allows AI models like Claude to securely connect to external tools and data sources. Instead of copy-pasting data into the chat, the model calls your server directly and gets structured responses back — no manual context injection needed.

```
Claude Desktop
     │
     │  MCP (stdio transport)
     ▼
MCP Server (Python)
     │
     │  SQL / DB queries
     ▼
Database  [PostgreSQL / SQLite / MySQL]
```

---

## Features

- Custom MCP server built with the **MCP Python SDK** (`FastMCP`)
- Exposes database as a **tool/resource** Claude can query at runtime
- Claude Desktop integration via `claude_desktop_config.json`
- Natural language → database answer, end to end

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| MCP Framework | MCP Python SDK (FastMCP) |
| AI Client | Claude Desktop |
| Database | [PostgreSQL / SQLite — update this] |
| Transport | stdio |

---

## Project Structure

```
First-Mcp-server/
└── my-first-mcp-server/
    ├── server.py          # MCP server — tool definitions + DB connection
    ├── pyproject.toml     # Project config and dependencies
    └── [other files]
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) package manager (recommended)
- Claude Desktop installed
- A running database instance

### Install dependencies

```bash
cd my-first-mcp-server
uv sync
```

Or with pip:

```bash
pip install mcp
```

### Run the server (for testing)

```bash
uv run server.py
```

Or inspect it with the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv run server.py
```

---

## Claude Desktop Integration

To connect this MCP server to Claude Desktop, add the following to your `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-first-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/First-Mcp-server/my-first-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after saving. You should see the MCP tools available in the chat interface.

---

## How It Works

1. Claude Desktop launches the MCP server as a subprocess over **stdio transport**.
2. The server registers one or more **tools** (e.g. `query_database`, `get_table_info`).
3. When you ask Claude a question about your data, it calls the relevant tool.
4. The server executes the query against the database and returns structured results.
5. Claude interprets the results and responds in natural language.

**Example interaction:**

> You: "How many orders were placed last month?"  
> Claude: *(calls `query_database` tool)* → "There were 342 orders placed in April 2026."

---

## What I Learned

- How the MCP protocol works under the hood (JSON-RPC over stdio)
- How to define and register tools using `@mcp.tool()` decorators
- How Claude Desktop discovers and calls external MCP servers
- Connecting a live database as an LLM-accessible context source

---

## Roadmap

- [ ] Add more tools (insert, update, aggregate queries)
- [ ] Switch from stdio to SSE/HTTP transport for remote access
- [ ] Add input validation and error handling on DB queries
- [ ] Support multiple database schemas

---

## License

MIT License
