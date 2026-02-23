import 'package:hive/hive.dart';

class CacheService {
  final Box<dynamic> _box = Hive.box('cache_box');

  Future<void> setJson(String key, dynamic value) async => _box.put(key, value);
  dynamic getJson(String key) => _box.get(key);
}
