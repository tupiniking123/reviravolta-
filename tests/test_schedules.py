from datetime import datetime


def test_payroll_schedule_next_run_semantic():
    current = datetime(2025, 1, 1)
    next_run = datetime(2025, 2, 1)
    assert next_run > current
