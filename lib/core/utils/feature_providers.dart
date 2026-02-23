import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/alerts/data/alerts_repository.dart';
import '../../features/dashboard/presentation/dashboard_repository.dart';
import '../../features/finance/categories/data/categories_repository.dart';
import '../../features/finance/expense/data/expense_repository.dart';
import '../../features/finance/income/data/income_repository.dart';
import '../../features/inventory/data/inventory_repository.dart';
import '../../features/reports/data/export_repository.dart';
import '../../features/vaccinations/data/vaccination_repository.dart';
import 'providers.dart';

final incomeRepositoryProvider = Provider((ref) => IncomeRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final expenseRepositoryProvider = Provider((ref) => ExpenseRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final categoriesRepositoryProvider = Provider((ref) => CategoriesRepository(ref.watch(apiClientProvider)));
final inventoryRepositoryProvider = Provider((ref) => InventoryRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final vaccinationsRepositoryProvider = Provider((ref) => VaccinationRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final alertsRepositoryProvider = Provider((ref) => AlertsRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final dashboardRepositoryProvider = Provider((ref) => DashboardRepository(ref.watch(apiClientProvider), ref.watch(cacheServiceProvider)));
final exportRepositoryProvider = Provider((ref) => ExportRepository(ref.watch(apiClientProvider)));
