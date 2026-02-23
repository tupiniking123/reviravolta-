import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../../../core/utils/rbac.dart';
import '../domain/alert_item.dart';

final alertsProvider = FutureProvider<List<AlertItem>>((ref) => ref.watch(alertsRepositoryProvider).list());

class AlertsScreen extends ConsumerWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final alerts = ref.watch(alertsProvider);
    return AdaptiveScaffold(
      title: 'Alertas',
      selectedIndex: 5,
      body: alerts.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro: $e')),
        data: (list) => ListView.builder(
          itemCount: list.length,
          itemBuilder: (_, i) {
            final a = list[i];
            return ListTile(
              title: Text(a.title),
              subtitle: Text(a.message),
              trailing: canWrite(ref, 'alerts') && a.status == 'OPEN'
                  ? TextButton(
                      onPressed: () async {
                        await ref.read(alertsRepositoryProvider).resolve(a.id);
                        ref.invalidate(alertsProvider);
                      },
                      child: const Text('Resolver'),
                    )
                  : Text(a.status),
            );
          },
        ),
      ),
    );
  }
}
