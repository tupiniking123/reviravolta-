import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../domain/vaccination.dart';

final vaccinationsProvider = FutureProvider<List<Vaccination>>((ref) => ref.watch(vaccinationsRepositoryProvider).list());

class VaccinationsScreen extends ConsumerWidget {
  const VaccinationsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final vaccs = ref.watch(vaccinationsProvider);

    return AdaptiveScaffold(
      title: 'Vacinação',
      selectedIndex: 4,
      body: vaccs.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro: $e')),
        data: (list) => ListView(
          children: list
              .map((v) => ListTile(
                    title: Text('Aplicada em ${v.date}'),
                    subtitle: Text('Próxima: ${v.nextDueDate ?? '-'}'),
                  ))
              .toList(),
        ),
      ),
    );
  }
}
