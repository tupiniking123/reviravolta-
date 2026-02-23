import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
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
        data: (list) => ListView(
          children: list
              .map((a) => ListTile(
                    title: Text(a.title),
                    subtitle: Text(a.message),
                    trailing: Text(a.status),
                  ))
              .toList(),
        ),
      ),
    );
  }
}
