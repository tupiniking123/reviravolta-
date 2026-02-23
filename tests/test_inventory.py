from types import SimpleNamespace


def test_inventory_low_alert_logic():
    row = SimpleNamespace(balance=5, min_level=10)
    assert row.balance < row.min_level
