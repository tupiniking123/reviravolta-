import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/presentation/auth_notifier.dart';

bool canWrite(WidgetRef ref, String module) => ref.read(authNotifierProvider).user?.canWrite(module) ?? false;
bool canRead(WidgetRef ref, String module) => ref.read(authNotifierProvider).user?.canRead(module) ?? false;
