from __future__ import annotations

from datetime import date, datetime
import tkinter as tk
from tkinter import messagebox, ttk

from finance_core import FinanceDB


class FinanceWindowsApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Finanças Simples - Windows")
        self.root.geometry("900x680")
        self.db = FinanceDB()
        self.today = date.today().isoformat()

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="Pronto para registrar seus dados.")

        title = ttk.Label(
            container,
            text="Finanças Simples (Desktop Windows)",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w", pady=(0, 10))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        self.expenses_tab = ttk.Frame(notebook, padding=10)
        self.report_tab = ttk.Frame(notebook, padding=10)
        self.agenda_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.expenses_tab, text="Gastos")
        notebook.add(self.report_tab, text="Relatório mensal")
        notebook.add(self.agenda_tab, text="Agenda diária")

        self._build_expenses_tab()
        self._build_report_tab()
        self._build_agenda_tab()

        status = ttk.Label(container, textvariable=self.status_var, foreground="#1f4e79")
        status.pack(anchor="w", pady=(8, 0))

    def _build_expenses_tab(self) -> None:
        form = ttk.LabelFrame(self.expenses_tab, text="Adicionar gasto", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Descrição").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.desc_entry = ttk.Entry(form, width=40)
        self.desc_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Valor (R$)").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.value_entry = ttk.Entry(form, width=20)
        self.value_entry.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Data (AAAA-MM-DD)").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.date_entry = ttk.Entry(form, width=20)
        self.date_entry.insert(0, self.today)
        self.date_entry.grid(row=2, column=1, sticky="w", padx=4, pady=4)

        buttons = ttk.Frame(form)
        buttons.grid(row=3, column=0, columnspan=2, sticky="ew", padx=4, pady=(8, 2))

        ttk.Button(buttons, text="Adicionar gasto fixo", command=lambda: self.add_expense("fixo")).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Adicionar gasto extra", command=lambda: self.add_expense("extra")).pack(
            side="left", padx=3
        )
        ttk.Button(buttons, text="Adicionar gasto diário", command=lambda: self.add_expense("diario")).pack(
            side="left", padx=3
        )
        ttk.Button(
            buttons,
            text="Fechamento de fatura",
            command=lambda: self.add_expense("fatura"),
        ).pack(side="left", padx=3)

        list_frame = ttk.LabelFrame(self.expenses_tab, text="Lançamentos do mês atual", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("data", "descricao", "categoria", "valor")
        self.expenses_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=16)
        self.expenses_tree.heading("data", text="Data")
        self.expenses_tree.heading("descricao", text="Descrição")
        self.expenses_tree.heading("categoria", text="Categoria")
        self.expenses_tree.heading("valor", text="Valor")
        self.expenses_tree.column("data", width=120)
        self.expenses_tree.column("descricao", width=350)
        self.expenses_tree.column("categoria", width=120)
        self.expenses_tree.column("valor", width=120, anchor="e")
        self.expenses_tree.pack(fill="both", expand=True)

        self.refresh_expenses_list()

    def _build_report_tab(self) -> None:
        panel = ttk.LabelFrame(self.report_tab, text="Gerar relatório", padding=10)
        panel.pack(fill="x")

        ttk.Label(panel, text="Renda mensal (R$)").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.income_entry = ttk.Entry(panel, width=20)
        self.income_entry.insert(0, "3000")
        self.income_entry.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(panel, text="Mês (1-12)").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.month_entry = ttk.Entry(panel, width=10)
        self.month_entry.insert(0, str(date.today().month))
        self.month_entry.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(panel, text="Ano").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.year_entry = ttk.Entry(panel, width=10)
        self.year_entry.insert(0, str(date.today().year))
        self.year_entry.grid(row=2, column=1, sticky="w", padx=4, pady=4)

        ttk.Button(panel, text="Gerar relatório mensal", command=self.generate_report).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=4, pady=(8, 0)
        )

        output_frame = ttk.LabelFrame(self.report_tab, text="Estatísticas", padding=10)
        output_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.report_text = tk.Text(output_frame, height=20, wrap="word")
        self.report_text.pack(fill="both", expand=True)
        self.report_text.insert("1.0", "Clique em 'Gerar relatório mensal'.")
        self.report_text.configure(state="disabled")

    def _build_agenda_tab(self) -> None:
        form = ttk.LabelFrame(self.agenda_tab, text="Adicionar compromisso", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Compromisso").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.commit_title_entry = ttk.Entry(form, width=40)
        self.commit_title_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Data (AAAA-MM-DD)").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.commit_date_entry = ttk.Entry(form, width=20)
        self.commit_date_entry.insert(0, self.today)
        self.commit_date_entry.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Nota").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.commit_note_entry = ttk.Entry(form, width=40)
        self.commit_note_entry.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=3, column=0, columnspan=2, sticky="ew", padx=4, pady=(8, 0))
        ttk.Button(btns, text="Adicionar compromisso", command=self.add_commitment).pack(side="left", padx=4)
        ttk.Button(btns, text="Ver compromissos de hoje", command=self.show_today_commitments).pack(side="left", padx=4)

        list_frame = ttk.LabelFrame(self.agenda_tab, text="Compromissos", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(10, 0))

        cols = ("data", "titulo", "nota")
        self.commit_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=16)
        self.commit_tree.heading("data", text="Data")
        self.commit_tree.heading("titulo", text="Compromisso")
        self.commit_tree.heading("nota", text="Nota")
        self.commit_tree.column("data", width=130)
        self.commit_tree.column("titulo", width=330)
        self.commit_tree.column("nota", width=280)
        self.commit_tree.pack(fill="both", expand=True)

        self.show_today_commitments()

    def _valid_date(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_expense(self, category: str) -> None:
        description = self.desc_entry.get().strip()
        value_text = self.value_entry.get().strip()
        expense_date = self.date_entry.get().strip() or self.today

        if not description or not value_text:
            messagebox.showwarning("Campos obrigatórios", "Preencha descrição e valor.")
            return
        if not self._valid_date(expense_date):
            messagebox.showwarning("Data inválida", "Use o formato AAAA-MM-DD.")
            return

        try:
            value = float(value_text)
        except ValueError:
            messagebox.showwarning("Valor inválido", "Digite um valor numérico.")
            return

        try:
            self.db.add_expense(description, value, category, expense_date)
        except ValueError as exc:
            messagebox.showwarning("Erro", str(exc))
            return

        self.desc_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.status_var.set(f"Lançado: {description} - R$ {value:.2f} [{category}]")
        self.refresh_expenses_list()

    def refresh_expenses_list(self) -> None:
        year = date.today().year
        month = date.today().month
        expenses = self.db.list_expenses_for_month(year, month)

        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)

        for exp in expenses:
            self.expenses_tree.insert(
                "",
                tk.END,
                values=(exp.expense_date, exp.description, exp.category, f"R$ {exp.amount:.2f}"),
            )

    def generate_report(self) -> None:
        income_text = self.income_entry.get().strip() or "0"
        month_text = self.month_entry.get().strip()
        year_text = self.year_entry.get().strip()

        try:
            income = float(income_text)
            month = int(month_text)
            year = int(year_text)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Revise renda, mês e ano.")
            return

        report = self.db.monthly_report(year, month, income)

        lines = [
            f"Relatório de {month:02d}/{year}",
            "=" * 35,
            f"Renda mensal: R$ {report['renda_mensal']:.2f}",
            f"Total gasto: R$ {report['total_gasto']:.2f}",
            f"Saldo: R$ {report['saldo']:.2f}",
            f"Taxa de rendimento: {report['taxa_rendimento']:.2f}%",
            "",
            "Gastos por categoria:",
            f"- Fixos: R$ {report['gastos_fixos']:.2f}",
            f"- Extras: R$ {report['gastos_extras']:.2f}",
            f"- Diários: R$ {report['gastos_diarios']:.2f}",
            f"- Fatura: R$ {report['fatura_cartao']:.2f}",
            f"- Quantidade de lançamentos: {int(report['quantidade_lancamentos'])}",
        ]

        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert("1.0", "\n".join(lines))
        self.report_text.configure(state="disabled")
        self.status_var.set("Relatório mensal atualizado.")

    def add_commitment(self) -> None:
        title = self.commit_title_entry.get().strip()
        commitment_date = self.commit_date_entry.get().strip() or self.today
        note = self.commit_note_entry.get().strip()

        if not title:
            messagebox.showwarning("Campo obrigatório", "Informe o compromisso.")
            return
        if not self._valid_date(commitment_date):
            messagebox.showwarning("Data inválida", "Use o formato AAAA-MM-DD.")
            return

        self.db.add_commitment(title, commitment_date, note)
        self.commit_title_entry.delete(0, tk.END)
        self.commit_note_entry.delete(0, tk.END)
        self.status_var.set(f"Compromisso salvo para {commitment_date}.")
        self.load_commitments_for_day(commitment_date)

    def load_commitments_for_day(self, day: str) -> None:
        items = self.db.list_commitments_for_day(day)

        for row in self.commit_tree.get_children():
            self.commit_tree.delete(row)

        for item in items:
            self.commit_tree.insert("", tk.END, values=(item.commitment_date, item.title, item.note))

    def show_today_commitments(self) -> None:
        self.load_commitments_for_day(self.today)
        self.status_var.set(f"Compromissos de hoje ({self.today}) carregados.")


def main() -> None:
    root = tk.Tk()
    FinanceWindowsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
