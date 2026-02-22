from finance_core import FinanceDB


def test_monthly_report_and_commitments(tmp_path):
    db = FinanceDB(str(tmp_path / "test.db"))

    db.add_expense("Aluguel", 1000, "fixo", "2026-02-05")
    db.add_expense("Mercado", 250, "diario", "2026-02-10")
    db.add_expense("Cinema", 80, "extra", "2026-02-12")
    db.add_expense("Cartão", 500, "fatura", "2026-02-15")
    db.add_commitment("Dentista", "2026-02-20", "14h")

    report = db.monthly_report(2026, 2, monthly_income=3000)

    assert report["total_gasto"] == 1830
    assert report["saldo"] == 1170
    assert report["gastos_fixos"] == 1000
    assert report["gastos_diarios"] == 250
    assert report["gastos_extras"] == 80
    assert report["fatura_cartao"] == 500

    commitments = db.list_commitments_for_day("2026-02-20")
    assert len(commitments) == 1
    assert commitments[0].title == "Dentista"
