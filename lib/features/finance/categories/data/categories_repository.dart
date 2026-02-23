import 'package:dio/dio.dart';

import '../domain/category.dart';

class CategoriesRepository {
  final Dio dio;
  CategoriesRepository(this.dio);

  Future<List<ExpenseCategory>> list() async {
    final response = await dio.get('/categories');
    return (response.data as List).map((e) => ExpenseCategory.fromJson(Map<String, dynamic>.from(e))).toList();
  }
}
