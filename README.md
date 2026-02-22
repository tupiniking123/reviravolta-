# App de Finanças Simples (Versão Windows)

Aplicativo desktop em Python, com interface gráfica **simples e fácil de entender**, focado em **Windows**.

## Funcionalidades

- Botões para adicionar:
  - gastos mensais fixos
  - gastos extras
  - gastos diários
  - fechamento de fatura
- Relatório mensal com estatísticas:
  - renda mensal
  - total gasto
  - saldo
  - taxa de rendimento
  - totais por categoria
- Agenda diária para compromissos.
- Visualização de lançamentos do mês atual e compromissos do dia.

## Tecnologias

- `Tkinter` (interface desktop nativa do Python no Windows)
- `SQLite` (banco local)

## Como executar no Windows

```bash
python app.py
```

> Dica: use Python 3.10+.

## Gerar executável (.exe) para Windows (opcional)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed app.py
```

O executável será gerado na pasta `dist/`.

## Estrutura

- `app.py`: interface Windows (Tkinter).
- `finance_core.py`: regras de negócio e persistência em SQLite.
- `test_finance_core.py`: testes unitários da lógica de negócio.
