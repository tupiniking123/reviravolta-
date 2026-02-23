import 'package:dio/dio.dart';

import '../../../../core/storage/cache_service.dart';
import '../domain/vaccination.dart';

class VaccinationRepository {
  final Dio dio;
  final CacheService cache;
  VaccinationRepository(this.dio, this.cache);

  Future<List<Vaccination>> list() async {
    try {
      final response = await dio.get('/vaccinations');
      await cache.setJson('vaccinations', response.data);
      return (response.data as List).map((e) => Vaccination.fromJson(Map<String, dynamic>.from(e))).toList();
    } on DioException {
      final cached = cache.getJson('vaccinations');
      if (cached is List) {
        return cached.map((e) => Vaccination.fromJson(Map<String, dynamic>.from(e))).toList();
      }
      rethrow;
    }
  }

  Future<void> create(Map<String, dynamic> payload) async => dio.post('/vaccinations', data: payload);
}
