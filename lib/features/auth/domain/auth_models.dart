import 'package:equatable/equatable.dart';

class SessionUser extends Equatable {
  final String id;
  final String name;
  final String email;
  final String role;
  final Map<String, Map<String, bool>> permissions;

  const SessionUser({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    required this.permissions,
  });

  bool canRead(String module) => permissions[module]?['read'] ?? false;
  bool canWrite(String module) => permissions[module]?['write'] ?? false;

  @override
  List<Object?> get props => [id, name, email, role, permissions];
}

class AuthTokens extends Equatable {
  final String accessToken;
  final String refreshToken;

  const AuthTokens({required this.accessToken, required this.refreshToken});

  @override
  List<Object?> get props => [accessToken, refreshToken];
}
