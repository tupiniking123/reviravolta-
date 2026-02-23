import 'package:dio/dio.dart';

import '../../../../core/storage/cache_service.dart';
import '../domain/income.dart';

class IncomeRepository {
  final Dio dio;
  final CacheService cache;
  IncomeRepository(this.dio, this.cache);

  Future<List<Income>> list() async {
    try {
      final response = await dio.get('/income');
      await cache.setJson('income_list', response.data);
      return (response.data as List).map((e) => Income.fromJson(Map<String, dynamic>.from(e))).toList();
    } on DioException {
      final cached = cache.getJson('income_list');
      if (cached is List) {
        return cached.map((e) => Income.fromJson(Map<String, dynamic>.from(e))).toList();
      }
      rethrow;
    }
  }

  Future<void> create(Map<String, dynamic> payload) async => dio.post('/income', data: payload);
}
