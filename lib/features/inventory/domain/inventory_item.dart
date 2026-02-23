class InventoryItem {
  final String id;
  final String name;
  final double minLevel;
  final double balance;
  final String? expiresAt;

  InventoryItem({required this.id, required this.name, required this.minLevel, required this.balance, this.expiresAt});

  bool get low => balance < minLevel;

  factory InventoryItem.fromJson(Map<String, dynamic> json) => InventoryItem(
        id: (json['item_id'] ?? json['id']) as String,
        name: json['name'] as String,
        minLevel: (json['min_level'] as num).toDouble(),
        balance: (json['balance'] as num).toDouble(),
        expiresAt: json['expires_at'] as String?,
      );
}
