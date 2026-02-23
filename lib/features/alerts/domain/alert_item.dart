class AlertItem {
  final String id;
  final String title;
  final String message;
  final String severity;
  final String status;

  AlertItem({required this.id, required this.title, required this.message, required this.severity, required this.status});

  factory AlertItem.fromJson(Map<String, dynamic> json) => AlertItem(
        id: json['id'] as String,
        title: json['title'] as String,
        message: json['message'] as String,
        severity: (json['severity'] ?? 'LOW') as String,
        status: (json['status'] ?? 'OPEN') as String,
      );
}
