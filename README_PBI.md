# Power BI - FarmOps

## Conexão PostgreSQL
No Power BI Desktop:
1. Obter Dados -> PostgreSQL
2. Servidor: `localhost:5432`
3. Banco: `farmops`
4. Usuário/senha do `.env`

## Views para importar
- `vw_financial_monthly`
- `vw_expenses_by_category`
- `vw_cashflow_daily`
- `vw_inventory_status`
- `vw_vaccinations_due`

## DimDate
Criar tabela calendário (Power Query ou DAX):
```DAX
DimDate = CALENDAR(DATE(2020,1,1), DATE(2035,12,31))
```
Adicionar colunas: Ano, Mês, AnoMês.

## Medidas DAX sugeridas
- Receitas = `SUM(vw_financial_monthly[total_income])`
- Despesas = `SUM(vw_financial_monthly[total_expense])`
- Lucro Bruto = `SUM(vw_financial_monthly[gross_profit])`
- Lucro Líquido = `SUM(vw_financial_monthly[net_profit])`
- Margem Bruta % = `DIVIDE([Lucro Bruto],[Receitas])`
- Margem Líquida % = `DIVIDE([Lucro Líquido],[Receitas])`
- MoM Receita = comparação mês anterior com `DATEADD`
- Itens a vencer = contar `expires_at <= TODAY()+30`
- Estoque baixo = contar `stock_status = "LOW"`
- Vacinas próximas/vencidas = contar `due_status`

## Páginas sugeridas
1. Visão Geral
2. Despesas por Categoria
3. Estoque
4. Vacinação
5. Alertas / Anomalias
