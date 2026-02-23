from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Income, Expense, ExpenseCategory, Cattle


def calculate_metrics(total_income: float, total_expense: float, direct_expense: float, cattle_count: int):
    gross_profit = total_income - direct_expense
    net_profit = total_income - total_expense
    gross_margin = (gross_profit / total_income * 100) if total_income else 0
    net_margin = (net_profit / total_income * 100) if total_income else 0
    cost_per_head = (direct_expense / cattle_count) if cattle_count else 0
    return gross_profit, net_profit, gross_margin, net_margin, cost_per_head


def get_summary(db: Session, farm_id, start: date, end: date):
    total_income = db.query(func.coalesce(func.sum(Income.amount), 0)).filter(
        Income.farm_id == farm_id, Income.date >= start, Income.date <= end, Income.deleted_at.is_(None)
    ).scalar()
    total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
        Expense.farm_id == farm_id, Expense.date >= start, Expense.date <= end, Expense.deleted_at.is_(None)
    ).scalar()
    direct_expense = db.query(func.coalesce(func.sum(Expense.amount), 0)).join(
        ExpenseCategory, Expense.category_id == ExpenseCategory.id
    ).filter(
        Expense.farm_id == farm_id,
        Expense.date >= start,
        Expense.date <= end,
        Expense.deleted_at.is_(None),
        ExpenseCategory.is_direct_cost.is_(True),
    ).scalar()
    cattle_count = db.query(func.count(Cattle.id)).filter(Cattle.farm_id == farm_id, Cattle.deleted_at.is_(None)).scalar()
    gross_profit, net_profit, gross_margin, net_margin, cost_per_head = calculate_metrics(float(total_income), float(total_expense), float(direct_expense), int(cattle_count))
    return {
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'direct_expense': float(direct_expense),
        'gross_profit': float(gross_profit),
        'net_profit': float(net_profit),
        'gross_margin_pct': float(gross_margin),
        'net_margin_pct': float(net_margin),
        'cost_per_head': float(cost_per_head),
    }
