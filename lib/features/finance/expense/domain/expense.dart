class Expense {
  final String id;
  final String date;
  final String description;
  final double amount;
  final String? vendor;

  Expense({required this.id, required this.date, required this.description, required this.amount, this.vendor});

  factory Expense.fromJson(Map<String, dynamic> json) => Expense(
        id: json['id'] as String,
        date: json['date'] as String,
        description: json['description'] as String,
        amount: (json['amount'] as num).toDouble(),
        vendor: json['vendor'] as String?,
      );
}
