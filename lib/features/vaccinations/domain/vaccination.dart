class Vaccination {
  final String id;
  final String date;
  final String? nextDueDate;

  Vaccination({required this.id, required this.date, required this.nextDueDate});

  factory Vaccination.fromJson(Map<String, dynamic> json) => Vaccination(
        id: json['id'] as String,
        date: json['date'] as String,
        nextDueDate: json['next_due_date'] as String?,
      );
}
