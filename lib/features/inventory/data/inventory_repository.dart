import 'package:dio/dio.dart';

import '../../../../core/storage/cache_service.dart';
import '../domain/inventory_item.dart';

class InventoryRepository {
  final Dio dio;
  final CacheService cache;

  InventoryRepository(this.dio, this.cache);

  Future<List<InventoryItem>> status() async {
    try {
      final response = await dio.get('/inventory/status');
      await cache.setJson('inventory_status', response.data);
      return (response.data as List).map((e) => InventoryItem.fromJson(Map<String, dynamic>.from(e))).toList();
    } on DioException {
      final cached = cache.getJson('inventory_status');
      if (cached is List) {
        return cached.map((e) => InventoryItem.fromJson(Map<String, dynamic>.from(e))).toList();
      }
      rethrow;
    }
  }

  Future<void> movement(Map<String, dynamic> payload) async => dio.post('/inventory/movements', data: payload);
}
