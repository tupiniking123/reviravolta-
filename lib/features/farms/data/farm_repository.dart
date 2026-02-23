import 'package:dio/dio.dart';

import '../../../core/storage/cache_service.dart';
import '../domain/farm.dart';

class FarmRepository {
  final Dio dio;
  final CacheService cache;

  FarmRepository(this.dio, this.cache);

  Future<List<Farm>> listFarms() async {
    try {
      final response = await dio.get('/farms');
      final farms = (response.data as List<dynamic>).map((e) => Farm.fromJson(e as Map<String, dynamic>)).toList();
      await cache.setJson('farms_list', response.data);
      return farms;
    } on DioException {
      final cached = cache.getJson('farms_list');
      if (cached is List) {
        return cached.map((e) => Farm.fromJson(Map<String, dynamic>.from(e as Map))).toList();
      }
      rethrow;
    }
  }
}
