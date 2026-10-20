# My First MCP Server

This directory contains a local Python MCP server for a small leave-management example. It uses the official MCP Python SDK's `FastMCP` interface and stdio transport. The server is intended for learning and experimentation, not for managing real employee records.

For the repository overview, see the [top-level README](../README.md).

## Requirements and setup

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/) for dependency management
- Claude Desktop or another MCP-compatible stdio client (optional)

From this directory:

```bash
uv sync
```

`pyproject.toml` declares the MCP SDK dependency, and `uv.lock` records the resolved dependency versions.

## Run the server

```bash
uv run main.py
```

The server communicates over standard input/output and waits for an MCP client. Do not print debugging messages to stdout when using stdio; stdout is reserved for MCP protocol messages. For temporary diagnostics, use stderr.

## Claude Desktop setup

Add the following entry to Claude Desktop's `claude_desktop_config.json`. Replace the example with the absolute path to this directory:

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

Configuration locations:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Merge this entry into the existing `mcpServers` object rather than replacing other server entries. Restart Claude Desktop after saving the configuration.

## MCP API reference

### Tools

| Tool | Arguments | Behavior |
| --- | --- | --- |
| `get_leave_balance` | `employee_id: str` | Returns the remaining balance for a demo employee ID. IDs are trimmed and compared case-insensitively. |
| `apply_leave` | `employee_id: str`, `leave_dates: list[str]` | Validates and records one or more dates. Dates must be unique ISO calendar dates (`YYYY-MM-DD`), must not already appear in history, and the request must fit within the balance. |
| `get_leave_history` | `employee_id: str` | Returns the dates recorded for the employee, or `No leaves taken.` when the history is empty. |

The sample IDs are `EMP001` and `EMP002`. Unknown IDs return `Employee ID not found.` The sample balances and history are defined near the top of `main.py`.

### Resource

`greeting://{name}` returns a simple personalized greeting. For example, an MCP client can read `greeting://Alex`.

## Leave request behavior

`apply_leave` validates the full request before changing the in-memory record:

1. The employee ID must match a sample record.
2. At least one date must be supplied.
3. Every date must be a valid `YYYY-MM-DD` calendar date.
4. Duplicate dates in the same request and dates already in the employee's history are rejected.
5. The requested number of days must not exceed the current balance.
6. Only after all checks pass are the balance and history updated.

Invalid requests do not partially change the balance or history. The example counts each requested date as one leave day; weekends and holidays are not treated specially.

## Run tests

The test suite uses Python's standard `unittest` library:

```bash
uv run python -m unittest discover -s tests -v
```

It covers ID normalization, balance/history reads, valid requests, invalid and duplicate dates, existing dates, empty requests, and insufficient balances.

## Data and security limitations

- Data lives in a module-level Python dictionary; it is reset on every server restart and is not shared across processes.
- The sample records are placeholders only. Do not add real personal or employment data to source code.
- There is no database, authentication, authorization, audit logging, approval process, concurrency protection, or holiday calendar.
- The server is configured for local stdio communication; it does not expose an HTTP service.
- Do not treat the demo checks as a security boundary. A production implementation needs an authenticated identity source, access controls, durable storage, privacy review, and operational monitoring.

## Troubleshooting

- **`ModuleNotFoundError: mcp`:** run `uv sync` from this directory and confirm that `uv` is on your PATH.
- **Server does not appear in Claude Desktop:** check that `command` is `uv`, the `--directory` value is an absolute path to this directory, and `main.py` is present; then fully restart Claude Desktop.
- **JSON/configuration error:** ensure the new entry is inside the `mcpServers` object, commas are valid JSON, and existing entries were preserved.
- **A tool returns `Employee ID not found.`:** use `EMP001` or `EMP002` (case-insensitive, whitespace is ignored).

## Extending the example

For a learning exercise, add tests before changing tool behavior. For a real application, replace the in-memory dictionary with a persistent data layer and design the identity, authorization, privacy, auditing, and approval model before exposing employee data or leave-changing operations.
