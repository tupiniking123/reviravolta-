INSERT INTO expense_categories (id, farm_id, name, is_direct_cost, is_active)
VALUES
(gen_random_uuid(), NULL, 'Insumos', TRUE, TRUE),
(gen_random_uuid(), NULL, 'Ração', TRUE, TRUE),
(gen_random_uuid(), NULL, 'Vacinas', TRUE, TRUE),
(gen_random_uuid(), NULL, 'Salário do caseiro', FALSE, TRUE),
(gen_random_uuid(), NULL, 'Despesas extras', FALSE, TRUE),
(gen_random_uuid(), NULL, 'Imprevistos', FALSE, TRUE)
ON CONFLICT DO NOTHING;
