class Income {
  final String id;
  final String date;
  final String description;
  final double amount;
  final String source;

  Income({required this.id, required this.date, required this.description, required this.amount, required this.source});

  factory Income.fromJson(Map<String, dynamic> json) => Income(
        id: json['id'] as String,
        date: json['date'] as String,
        description: json['description'] as String,
        amount: (json['amount'] as num).toDouble(),
        source: (json['source'] ?? '') as String,
      );
}
