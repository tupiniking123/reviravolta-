import 'package:dio/dio.dart';

class ExportRepository {
  final Dio dio;
  ExportRepository(this.dio);

  Future<String> downloadCsv(String endpoint) async {
    final response = await dio.get<String>('/export/powerbi/$endpoint.csv');
    return response.data ?? '';
  }
}
