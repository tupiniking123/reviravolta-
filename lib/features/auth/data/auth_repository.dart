import 'package:dio/dio.dart';

import '../../../core/errors/failures.dart';
import '../../../core/storage/secure_storage_service.dart';
import '../domain/auth_models.dart';

class AuthRepository {
  final Dio dio;
  final SecureStorageService secureStorage;

  AuthRepository({required this.dio, required this.secureStorage});

  Future<AuthTokens> login(String email, String password) async {
    try {
      final response = await dio.post('/auth/login', data: {'email': email, 'password': password});
      final tokens = AuthTokens(
        accessToken: response.data['access_token'] as String,
        refreshToken: response.data['refresh_token'] as String,
      );
      await secureStorage.write('access_token', tokens.accessToken);
      await secureStorage.write('refresh_token', tokens.refreshToken);
      return tokens;
    } on DioException catch (e) {
      throw AuthFailure(e.response?.data.toString() ?? 'Falha no login');
    }
  }

  Future<AuthTokens?> readTokens() async {
    final access = await secureStorage.read('access_token');
    final refresh = await secureStorage.read('refresh_token');
    if (access == null || refresh == null) return null;
    return AuthTokens(accessToken: access, refreshToken: refresh);
  }

  Future<void> persistTokens(AuthTokens tokens) async {
    await secureStorage.write('access_token', tokens.accessToken);
    await secureStorage.write('refresh_token', tokens.refreshToken);
  }

  Future<void> logout() async {
    await secureStorage.delete('access_token');
    await secureStorage.delete('refresh_token');
  }

  Future<AuthTokens> refreshToken(String refreshToken) async {
    final response = await dio.post('/auth/refresh', data: {'refresh_token': refreshToken});
    final tokens = AuthTokens(
      accessToken: response.data['access_token'] as String,
      refreshToken: response.data['refresh_token'] as String,
    );
    await persistTokens(tokens);
    return tokens;
  }

  Future<SessionUser> me() async {
    try {
      final response = await dio.get('/auth/me');
      return SessionUser(
        id: response.data['id'] as String,
        name: response.data['name'] as String,
        email: response.data['email'] as String,
        role: (response.data['role'] ?? 'VIEWER') as String,
        permissions: Map<String, Map<String, bool>>.from(
          (response.data['permissions'] ?? <String, dynamic>{}).map(
            (key, value) => MapEntry(
              key,
              {
                'read': (value['read'] ?? false) as bool,
                'write': (value['write'] ?? false) as bool,
              },
            ),
          ),
        ),
      );
    } on DioException catch (e) {
      throw NetworkFailure(e.message ?? 'Erro ao buscar perfil');
    }
  }
}
