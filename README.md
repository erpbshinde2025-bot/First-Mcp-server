# First MCP Server

A small educational **Model Context Protocol (MCP)** server built with Python and the MCP Python SDK. It exposes a demo leave manager to an MCP client such as Claude Desktop over local stdio.

> **Prototype, not an HR system:** employee records are hard-coded demo data held in memory. They are not connected to a database, are reset when the process restarts, and must not be replaced with real employee data without adding persistence, authentication, authorization, and appropriate privacy controls.

## What it demonstrates

- Registering MCP tools with `FastMCP`
- Returning tool results to an MCP client over stdio
- Validating dates and leave balances before changing state
- Exposing a parameterized MCP resource
- Connecting a local server to Claude Desktop

## Repository layout

```text
First-Mcp-server/
├── README.md
└── my-first-mcp-server/
    ├── README.md
    ├── main.py
    ├── pyproject.toml
    ├── uv.lock
    └── tests/
        └── test_main.py
```

The package-level README contains the complete setup guide, tool reference, behavior, testing instructions, and troubleshooting notes.

## Quick start

Requirements: Python 3.10 or newer and [`uv`](https://docs.astral.sh/uv/).

```bash
cd my-first-mcp-server
uv sync
uv run main.py
```

The server waits for an MCP client on standard input/output. To stop a manual run, press `Ctrl+C`.

Run the test suite with:

```bash
uv run python -m unittest discover -s tests -v
```

## Connect Claude Desktop

Open Claude Desktop's configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add an entry under `mcpServers`, replacing the example directory with the absolute path to this repository's `my-first-mcp-server` directory:

```json
{
  "mcpServers": {
    "leave-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/First-Mcp-server/my-first-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

Keep any existing entries in the configuration file. Save the file and fully restart Claude Desktop; the server's tools should then appear in a conversation.

## Important limitations

- The data store is a Python dictionary in `main.py`; all changes disappear when the server exits.
- The sample data uses placeholder employee IDs, not a real database or identity system.
- This prototype has no authentication, authorization, audit log, holiday calendar, or approval workflow.
- The server uses stdio and does not expose a remote HTTP endpoint.
- No license file is included in this repository; confirm licensing before redistributing it.

## Documentation

See [`my-first-mcp-server/README.md`](my-first-mcp-server/README.md) for the full implementation and usage reference.
