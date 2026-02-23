import 'dart:convert';

import 'package:dio/dio.dart';

import '../../features/auth/data/auth_repository.dart';
import '../../features/auth/domain/auth_models.dart';
import '../config/app_config.dart';
import '../storage/session_store.dart';

class ApiClientFactory {
  static Dio build({
    required Future<AuthTokens?> Function() getTokens,
    required Future<AuthTokens> Function(String refreshToken) refresh,
    required SessionStore sessionStore,
    required Future<void> onUnauthorized,
  }) {
    final dio = Dio(BaseOptions(baseUrl: AppConfig.baseUrl));

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final tokens = await getTokens();
          final farmId = sessionStore.farmId;
          if (tokens != null) {
            options.headers['Authorization'] = 'Bearer ${tokens.accessToken}';
          }
          if (farmId != null && !options.path.startsWith('/auth') && !options.path.startsWith('/farms')) {
            options.headers['X-Farm-Id'] = farmId;
          }
          handler.next(options);
        },
        onError: (error, handler) async {
          if (error.response?.statusCode == 401 && !error.requestOptions.path.contains('/auth/refresh')) {
            final tokens = await getTokens();
            if (tokens != null) {
              try {
                final newTokens = await refresh(tokens.refreshToken);
                final retry = error.requestOptions;
                retry.headers['Authorization'] = 'Bearer ${newTokens.accessToken}';
                final response = await dio.fetch(retry);
                return handler.resolve(response);
              } catch (_) {
                await onUnauthorized();
              }
            }
          }
          handler.next(error);
        },
      ),
    );

    dio.interceptors.add(LogInterceptor(responseBody: false, requestBody: false, logPrint: (obj) => jsonEncode({'dio': obj.toString()})));
    return dio;
  }
}
