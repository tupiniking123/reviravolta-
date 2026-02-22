from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Expense:
    id: int
    description: str
    amount: float
    category: str
    expense_date: str


@dataclass
class Commitment:
    id: int
    title: str
    commitment_date: str
    note: str


class FinanceDB:
    """Simple SQLite database layer for personal finance + daily agenda."""

    def __init__(self, db_path: str = "financas.db") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    expense_date TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS commitments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    commitment_date TEXT NOT NULL,
                    note TEXT DEFAULT ''
                )
                """
            )

    def add_expense(
        self,
        description: str,
        amount: float,
        category: str,
        expense_date: Optional[str] = None,
    ) -> None:
        if amount <= 0:
            raise ValueError("Valor deve ser maior que zero.")
        expense_date = expense_date or date.today().isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO expenses (description, amount, category, expense_date)
                VALUES (?, ?, ?, ?)
                """,
                (description.strip(), float(amount), category.strip(), expense_date),
            )

    def add_commitment(
        self,
        title: str,
        commitment_date: str,
        note: str = "",
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO commitments (title, commitment_date, note)
                VALUES (?, ?, ?)
                """,
                (title.strip(), commitment_date, note.strip()),
            )

    def list_expenses_for_month(self, year: int, month: int) -> List[Expense]:
        prefix = f"{year:04d}-{month:02d}"
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, description, amount, category, expense_date
                FROM expenses
                WHERE expense_date LIKE ?
                ORDER BY expense_date ASC
                """,
                (f"{prefix}%",),
            ).fetchall()
        return [Expense(**dict(row)) for row in rows]

    def list_commitments_for_day(self, day_iso: str) -> List[Commitment]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, title, commitment_date, note
                FROM commitments
                WHERE commitment_date = ?
                ORDER BY id ASC
                """,
                (day_iso,),
            ).fetchall()
        return [Commitment(**dict(row)) for row in rows]

    def monthly_report(self, year: int, month: int, monthly_income: float) -> Dict[str, float]:
        expenses = self.list_expenses_for_month(year, month)
        total_spent = sum(item.amount for item in expenses)

        by_category: Dict[str, float] = {}
        for item in expenses:
            by_category[item.category] = by_category.get(item.category, 0.0) + item.amount

        fixed = by_category.get("fixo", 0.0)
        extra = by_category.get("extra", 0.0)
        daily = by_category.get("diario", 0.0)
        card_bill_close = by_category.get("fatura", 0.0)

        savings = monthly_income - total_spent
        savings_rate = (savings / monthly_income * 100.0) if monthly_income > 0 else 0.0

        return {
            "renda_mensal": monthly_income,
            "total_gasto": total_spent,
            "saldo": savings,
            "taxa_rendimento": savings_rate,
            "gastos_fixos": fixed,
            "gastos_extras": extra,
            "gastos_diarios": daily,
            "fatura_cartao": card_bill_close,
            "quantidade_lancamentos": float(len(expenses)),
        }
