import 'package:equatable/equatable.dart';

class Farm extends Equatable {
  final String id;
  final String name;
  final String timezone;
  final String currency;

  const Farm({required this.id, required this.name, required this.timezone, required this.currency});

  factory Farm.fromJson(Map<String, dynamic> json) => Farm(
        id: json['id'] as String,
        name: json['name'] as String,
        timezone: (json['timezone'] ?? 'America/Sao_Paulo') as String,
        currency: (json['currency'] ?? 'BRL') as String,
      );

  @override
  List<Object?> get props => [id, name, timezone, currency];
}
