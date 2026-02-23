CREATE OR REPLACE VIEW vw_financial_monthly AS
SELECT i.farm_id,
       date_trunc('month', i.date)::date AS month,
       COALESCE(SUM(i.amount),0) AS total_income,
       COALESCE((SELECT SUM(e.amount) FROM expense e WHERE e.farm_id=i.farm_id AND date_trunc('month',e.date)=date_trunc('month',i.date) AND e.deleted_at IS NULL),0) AS total_expense,
       COALESCE((SELECT SUM(e.amount) FROM expense e JOIN expense_categories c ON c.id=e.category_id WHERE e.farm_id=i.farm_id AND date_trunc('month',e.date)=date_trunc('month',i.date) AND c.is_direct_cost=true AND e.deleted_at IS NULL),0) AS direct_expense,
       COALESCE(SUM(i.amount),0) - COALESCE((SELECT SUM(e.amount) FROM expense e JOIN expense_categories c ON c.id=e.category_id WHERE e.farm_id=i.farm_id AND date_trunc('month',e.date)=date_trunc('month',i.date) AND c.is_direct_cost=true AND e.deleted_at IS NULL),0) AS gross_profit,
       COALESCE(SUM(i.amount),0) - COALESCE((SELECT SUM(e.amount) FROM expense e WHERE e.farm_id=i.farm_id AND date_trunc('month',e.date)=date_trunc('month',i.date) AND e.deleted_at IS NULL),0) AS net_profit
FROM income i
WHERE i.deleted_at IS NULL
GROUP BY i.farm_id, date_trunc('month', i.date);

CREATE OR REPLACE VIEW vw_expenses_by_category AS
SELECT e.farm_id, date_trunc('month', e.date)::date AS month, c.name AS category, SUM(e.amount) AS total
FROM expense e JOIN expense_categories c ON c.id = e.category_id
WHERE e.deleted_at IS NULL
GROUP BY e.farm_id, date_trunc('month', e.date), c.name;

CREATE OR REPLACE VIEW vw_cashflow_daily AS
SELECT d.farm_id, d.day,
       COALESCE(i.total_income,0) AS income,
       COALESCE(e.total_expense,0) AS expense
FROM (
    SELECT farm_id, date::date AS day FROM income
    UNION
    SELECT farm_id, date::date AS day FROM expense
) d
LEFT JOIN (SELECT farm_id, date::date AS day, SUM(amount) AS total_income FROM income WHERE deleted_at IS NULL GROUP BY farm_id, date::date) i ON i.farm_id=d.farm_id AND i.day=d.day
LEFT JOIN (SELECT farm_id, date::date AS day, SUM(amount) AS total_expense FROM expense WHERE deleted_at IS NULL GROUP BY farm_id, date::date) e ON e.farm_id=d.farm_id AND e.day=d.day;

CREATE OR REPLACE VIEW vw_inventory_status AS
SELECT it.farm_id, it.id AS item_id, it.name, it.min_level, it.expires_at,
       COALESCE(SUM(CASE WHEN m.movement_type='IN' THEN m.qty ELSE -m.qty END),0) AS balance,
       CASE WHEN COALESCE(SUM(CASE WHEN m.movement_type='IN' THEN m.qty ELSE -m.qty END),0) < it.min_level THEN 'LOW' ELSE 'OK' END AS stock_status
FROM inventory_items it
LEFT JOIN inventory_movements m ON m.item_id = it.id
WHERE it.deleted_at IS NULL
GROUP BY it.farm_id, it.id;

CREATE OR REPLACE VIEW vw_vaccinations_due AS
SELECT farm_id, id AS vaccination_id, cattle_id, vaccine_item_id, next_due_date,
       CASE WHEN next_due_date < CURRENT_DATE THEN 'OVERDUE' ELSE 'UPCOMING' END AS due_status
FROM vaccinations
WHERE next_due_date IS NOT NULL;
