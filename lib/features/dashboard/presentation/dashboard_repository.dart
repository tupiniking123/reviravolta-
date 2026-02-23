import 'package:dio/dio.dart';

import '../../../core/storage/cache_service.dart';

class DashboardRepository {
  final Dio dio;
  final CacheService cache;
  DashboardRepository(this.dio, this.cache);

  Future<Map<String, dynamic>> summary(String start, String end) async {
    try {
      final response = await dio.get('/reports/summary', queryParameters: {'start': start, 'end': end});
      await cache.setJson('summary_$start$end', response.data);
      return Map<String, dynamic>.from(response.data as Map);
    } on DioException {
      final cached = cache.getJson('summary_$start$end');
      if (cached is Map) return Map<String, dynamic>.from(cached);
      rethrow;
    }
  }
}
