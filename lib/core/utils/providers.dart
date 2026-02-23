import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import '../../features/auth/data/auth_repository.dart';
import '../../features/auth/presentation/auth_notifier.dart';
import '../../features/farms/data/farm_repository.dart';
import '../network/api_client.dart';
import '../storage/cache_service.dart';
import '../storage/secure_storage_service.dart';
import '../storage/session_store.dart';

final secureStorageProvider = Provider<SecureStorageService>((ref) => SecureStorageService());
final cacheServiceProvider = Provider<CacheService>((ref) => CacheService());
final sessionStoreProvider = Provider<SessionStore>((ref) => SessionStore());

final bootstrapDioProvider = Provider<Dio>((ref) => Dio(BaseOptions(baseUrl: AppConfig.baseUrl)));

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(dio: ref.watch(bootstrapDioProvider), secureStorage: ref.watch(secureStorageProvider));
});

final apiClientProvider = Provider<Dio>((ref) {
  final sessionStore = ref.watch(sessionStoreProvider);
  return ApiClientFactory.build(
    getTokens: () async => ref.read(authRepositoryProvider).readTokens(),
    refresh: (refreshToken) => ref.read(authRepositoryProvider).refreshToken(refreshToken),
    sessionStore: sessionStore,
    onUnauthorized: () async => ref.read(authNotifierProvider.notifier).logout(),
  );
});

final farmRepositoryProvider = Provider<FarmRepository>((ref) => FarmRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
