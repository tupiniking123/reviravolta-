import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/alerts/presentation/alerts_screen.dart';
import '../../features/auth/presentation/auth_notifier.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/farms/presentation/farm_selector_screen.dart';
import '../../features/finance/expense/presentation/expense_screen.dart';
import '../../features/finance/income/presentation/income_screen.dart';
import '../../features/inventory/presentation/inventory_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';
import '../../features/vaccinations/presentation/vaccinations_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authNotifierProvider);
  return GoRouter(
    initialLocation: '/login',
    redirect: (context, state) {
      final isLogged = auth.user != null;
      final inLogin = state.uri.path == '/login';
      final inFarms = state.uri.path == '/farms';
      if (!isLogged && !inLogin) return '/login';
      if (isLogged && inLogin) return '/farms';
      if (isLogged && auth.activeFarmId == null && !inFarms) return '/farms';
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/farms', builder: (_, __) => const FarmSelectorScreen()),
      GoRoute(path: '/', builder: (_, __) => const DashboardScreen()),
      GoRoute(path: '/income', builder: (_, __) => const IncomeScreen()),
      GoRoute(path: '/expense', builder: (_, __) => const ExpenseScreen()),
      GoRoute(path: '/inventory', builder: (_, __) => const InventoryScreen()),
      GoRoute(path: '/vaccinations', builder: (_, __) => const VaccinationsScreen()),
      GoRoute(path: '/alerts', builder: (_, __) => const AlertsScreen()),
      GoRoute(path: '/reports', builder: (_, __) => const ReportsScreen()),
      GoRoute(path: '/settings', builder: (_, __) => const SettingsScreen()),
    ],
  );
});
