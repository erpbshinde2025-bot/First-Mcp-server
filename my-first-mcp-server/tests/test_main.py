"""Unit tests for the in-memory leave manager."""

import copy
import unittest

import main


class LeaveManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_records = copy.deepcopy(main.employee_leaves)

    def tearDown(self) -> None:
        main.employee_leaves.clear()
        main.employee_leaves.update(self.original_records)

    def test_balance_lookup_normalizes_employee_id(self) -> None:
        self.assertEqual(
            main.get_leave_balance(" emp001 "),
            "EMP001 has 18 leave days remaining.",
        )

    def test_unknown_employee_is_reported(self) -> None:
        self.assertEqual(main.get_leave_balance("EMP999"), "Employee ID not found.")

    def test_apply_leave_updates_balance_and_history(self) -> None:
        result = main.apply_leave("emp001", ["2030-02-15", "2030-02-16"])

        self.assertEqual(
            result,
            "Leave applied for 2 day(s). Remaining balance: 16.",
        )
        self.assertEqual(main.employee_leaves["EMP001"].balance, 16)
        self.assertEqual(
            main.employee_leaves["EMP001"].history[-2:],
            ["2030-02-15", "2030-02-16"],
        )

    def test_empty_request_is_rejected_without_mutation(self) -> None:
        before = copy.deepcopy(main.employee_leaves["EMP001"])

        result = main.apply_leave("EMP001", [])

        self.assertEqual(result, "Please provide at least one leave date.")
        self.assertEqual(main.employee_leaves["EMP001"], before)

    def test_invalid_date_is_rejected_without_partial_mutation(self) -> None:
        before = copy.deepcopy(main.employee_leaves["EMP001"])

        result = main.apply_leave("EMP001", ["2030-02-15", "2030-02-30"])

        self.assertEqual(
            result,
            "Invalid leave date '2030-02-30'. Use YYYY-MM-DD format.",
        )
        self.assertEqual(main.employee_leaves["EMP001"], before)

    def test_non_iso_date_format_is_rejected(self) -> None:
        result = main.apply_leave("EMP001", ["20300215"])

        self.assertEqual(
            result,
            "Invalid leave date '20300215'. Use YYYY-MM-DD format.",
        )

    def test_duplicate_dates_in_request_are_rejected(self) -> None:
        before = copy.deepcopy(main.employee_leaves["EMP001"])

        result = main.apply_leave("EMP001", ["2030-02-15", "2030-02-15"])

        self.assertEqual(
            result,
            "Duplicate leave date '2030-02-15' is not allowed.",
        )
        self.assertEqual(main.employee_leaves["EMP001"], before)

    def test_date_already_in_history_is_rejected(self) -> None:
        before = copy.deepcopy(main.employee_leaves["EMP001"])

        result = main.apply_leave("EMP001", ["2025-01-01"])

        self.assertEqual(
            result,
            "Leave date '2025-01-01' is already in the history.",
        )
        self.assertEqual(main.employee_leaves["EMP001"], before)

    def test_insufficient_balance_is_rejected_without_mutation(self) -> None:
        main.employee_leaves["EMP001"].balance = 1
        before = copy.deepcopy(main.employee_leaves["EMP001"])

        result = main.apply_leave("EMP001", ["2030-02-15", "2030-02-16"])

        self.assertEqual(
            result,
            "Insufficient leave balance. You requested 2 day(s) but have only 1.",
        )
        self.assertEqual(main.employee_leaves["EMP001"], before)

    def test_history_for_employee_with_no_leave(self) -> None:
        self.assertEqual(
            main.get_leave_history("EMP002"),
            "Leave history for EMP002: No leaves taken.",
        )

    def test_history_for_employee_with_leave(self) -> None:
        self.assertEqual(
            main.get_leave_history("emp001"),
            "Leave history for EMP001: 2025-01-01, 2025-01-02",
        )


if __name__ == "__main__":
    unittest.main()
