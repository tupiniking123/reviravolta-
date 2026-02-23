import 'package:dio/dio.dart';

import '../../../../core/storage/cache_service.dart';
import '../domain/expense.dart';

class ExpenseRepository {
  final Dio dio;
  final CacheService cache;
  ExpenseRepository(this.dio, this.cache);

  Future<List<Expense>> list() async {
    try {
      final response = await dio.get('/expense');
      await cache.setJson('expense_list', response.data);
      return (response.data as List).map((e) => Expense.fromJson(Map<String, dynamic>.from(e))).toList();
    } on DioException {
      final cached = cache.getJson('expense_list');
      if (cached is List) {
        return cached.map((e) => Expense.fromJson(Map<String, dynamic>.from(e))).toList();
      }
      rethrow;
    }
  }

  Future<void> create(Map<String, dynamic> payload) async => dio.post('/expense', data: payload);
}
