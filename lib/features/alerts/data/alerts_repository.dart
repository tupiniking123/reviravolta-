import 'package:dio/dio.dart';

import '../../../../core/storage/cache_service.dart';
import '../domain/alert_item.dart';

class AlertsRepository {
  final Dio dio;
  final CacheService cache;
  AlertsRepository(this.dio, this.cache);

  Future<List<AlertItem>> list() async {
    try {
      final response = await dio.get('/alerts');
      await cache.setJson('alerts', response.data);
      return (response.data as List).map((e) => AlertItem.fromJson(Map<String, dynamic>.from(e))).toList();
    } on DioException {
      final cached = cache.getJson('alerts');
      if (cached is List) {
        return cached.map((e) => AlertItem.fromJson(Map<String, dynamic>.from(e))).toList();
      }
      rethrow;
    }
  }

  Future<void> resolve(String id) async => dio.post('/alerts/$id/resolve');
}
