from app.services.finance_service import calculate_metrics


def test_profit_calculation():
    gross, net, gm, nm, cph = calculate_metrics(1000, 600, 300, 10)
    assert gross == 700
    assert net == 400
    assert gm == 70
    assert nm == 40
    assert cph == 30
