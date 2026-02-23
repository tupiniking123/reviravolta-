import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../../../core/utils/rbac.dart';
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
      body: Column(
        children: [
          if (canWrite(ref, 'vaccinations'))
            Align(
              alignment: Alignment.centerRight,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: FilledButton(onPressed: () => _create(context, ref), child: const Text('Novo Registro')),
              ),
            ),
          Expanded(
            child: vaccs.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('Erro: $e')),
              data: (list) => ListView(
                children: list.map((v) {
                  final overdue = v.nextDueDate != null && DateTime.tryParse(v.nextDueDate!)?.isBefore(DateTime.now()) == true;
                  return ListTile(
                    title: Text('Aplicada em ${v.date}'),
                    subtitle: Text('Próxima: ${v.nextDueDate ?? '-'}'),
                    trailing: overdue ? const Chip(label: Text('Vencida'), backgroundColor: Colors.redAccent) : const Chip(label: Text('Próxima')),
                  );
                }).toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _create(BuildContext context, WidgetRef ref) async {
    await ref.read(vaccinationsRepositoryProvider).create({
      'date': DateTime.now().toIso8601String().split('T').first,
      'dose': '1',
      'cost': 0,
      'vaccine_item_id': '00000000-0000-0000-0000-000000000000',
    });
    ref.invalidate(vaccinationsProvider);
  }
}
