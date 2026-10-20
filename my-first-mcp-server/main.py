"""A small, in-memory leave manager exposed as an MCP server."""

from dataclasses import dataclass, field
from datetime import date

from mcp.server.fastmcp import FastMCP


@dataclass
class LeaveRecord:
    """The demo leave balance and dates recorded for one employee."""

    balance: int
    history: list[str] = field(default_factory=list)


# Placeholder records only. Replace this in-memory store before any real use.
employee_leaves: dict[str, LeaveRecord] = {
    "EMP001": LeaveRecord(balance=18, history=["2025-01-01", "2025-01-02"]),
    "EMP002": LeaveRecord(balance=20),
}

mcp = FastMCP("LeaveManager")


def _find_employee(employee_id: str) -> LeaveRecord | None:
    """Look up a demo employee by case-insensitive ID."""
    if not isinstance(employee_id, str):
        return None
    return employee_leaves.get(employee_id.strip().upper())


def _validate_leave_dates(
    leave_dates: list[str], record: LeaveRecord
) -> tuple[list[str] | None, str | None]:
    """Validate a complete request before any balance or history is changed."""
    if not leave_dates:
        return None, "Please provide at least one leave date."

    normalized_dates: list[str] = []
    seen_dates: set[str] = set()
    existing_dates = set(record.history)

    for value in leave_dates:
        if not isinstance(value, str) or not value.strip():
            return None, "Each leave date must use YYYY-MM-DD format."

        normalized = value.strip()
        try:
            parsed = date.fromisoformat(normalized)
        except ValueError:
            return None, f"Invalid leave date '{value}'. Use YYYY-MM-DD format."

        if parsed.isoformat() != normalized:
            return None, f"Invalid leave date '{value}'. Use YYYY-MM-DD format."
        if normalized in seen_dates:
            return None, f"Duplicate leave date '{normalized}' is not allowed."
        if normalized in existing_dates:
            return None, f"Leave date '{normalized}' is already in the history."

        normalized_dates.append(normalized)
        seen_dates.add(normalized)

    return normalized_dates, None


@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Return the remaining leave-day balance for a demo employee ID."""
    record = _find_employee(employee_id)
    if record is None:
        return "Employee ID not found."
    return f"{employee_id.strip().upper()} has {record.balance} leave days remaining."


@mcp.tool()
def apply_leave(employee_id: str, leave_dates: list[str]) -> str:
    """Apply for one or more leave dates in YYYY-MM-DD format."""
    record = _find_employee(employee_id)
    if record is None:
        return "Employee ID not found."

    normalized_dates, error = _validate_leave_dates(leave_dates, record)
    if error is not None:
        return error

    # Validation is complete; reject the request without partial updates.
    assert normalized_dates is not None
    requested_days = len(normalized_dates)
    if requested_days > record.balance:
        return (
            f"Insufficient leave balance. You requested {requested_days} "
            f"day(s) but have only {record.balance}."
        )

    record.balance -= requested_days
    record.history.extend(normalized_dates)
    return (
        f"Leave applied for {requested_days} day(s). "
        f"Remaining balance: {record.balance}."
    )


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Return the recorded leave dates for a demo employee ID."""
    record = _find_employee(employee_id)
    if record is None:
        return "Employee ID not found."
    if not record.history:
        return f"Leave history for {employee_id.strip().upper()}: No leaves taken."
    return (
        f"Leave history for {employee_id.strip().upper()}: "
        f"{', '.join(record.history)}"
    )


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a simple greeting resource for the supplied name."""
    return f"Hello, {name}! How can I assist you with leave management today?"


if __name__ == "__main__":
    mcp.run()
