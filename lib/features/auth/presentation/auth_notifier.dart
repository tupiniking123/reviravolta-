import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/storage/session_store.dart';
import '../../../core/utils/providers.dart';
import '../domain/auth_models.dart';

class AuthState {
  final SessionUser? user;
  final bool loading;
  final String? error;
  final String? activeFarmId;

  const AuthState({this.user, this.loading = false, this.error, this.activeFarmId});

  AuthState copyWith({SessionUser? user, bool? loading, String? error, String? activeFarmId}) {
    return AuthState(
      user: user ?? this.user,
      loading: loading ?? this.loading,
      error: error,
      activeFarmId: activeFarmId ?? this.activeFarmId,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final Ref ref;
  final SessionStore sessionStore;

  AuthNotifier(this.ref, this.sessionStore) : super(AuthState(activeFarmId: sessionStore.farmId));

  Future<void> login(String email, String password) async {
    state = state.copyWith(loading: true, error: null);
    try {
      await ref.read(authRepositoryProvider).login(email, password);
      final user = await ref.read(authRepositoryProvider).me();
      state = state.copyWith(user: user, loading: false);
    } catch (e) {
      state = state.copyWith(loading: false, error: e.toString());
    }
  }

  Future<void> restoreSession() async {
    final tokens = await ref.read(authRepositoryProvider).readTokens();
    if (tokens == null) return;
    try {
      final user = await ref.read(authRepositoryProvider).me();
      state = state.copyWith(user: user);
    } catch (_) {
      await logout();
    }
  }

  Future<void> setActiveFarm(String farmId) async {
    await sessionStore.setFarmId(farmId);
    state = state.copyWith(activeFarmId: farmId);
  }

  Future<void> logout() async {
    await ref.read(authRepositoryProvider).logout();
    await sessionStore.clearFarmId();
    state = const AuthState();
  }
}

final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref, ref.watch(sessionStoreProvider));
});
