import 'package:hive/hive.dart';

class SessionStore {
  final Box<dynamic> _box = Hive.box('session_box');

  String? get farmId => _box.get('active_farm_id') as String?;
  Future<void> setFarmId(String id) => _box.put('active_farm_id', id);
  Future<void> clearFarmId() => _box.delete('active_farm_id');
}
