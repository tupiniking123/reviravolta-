import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/utils/adaptive_scaffold.dart';
import '../../../../core/utils/feature_providers.dart';
import '../../../../core/utils/rbac.dart';
import '../domain/income.dart';

final incomeProvider = FutureProvider<List<Income>>((ref) => ref.watch(incomeRepositoryProvider).list());

class IncomeScreen extends ConsumerWidget {
  const IncomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final incomes = ref.watch(incomeProvider);
    return AdaptiveScaffold(
      title: 'Receitas',
      selectedIndex: 1,
      body: Column(
        children: [
          if (canWrite(ref, 'finance'))
            Align(
              alignment: Alignment.centerRight,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: FilledButton.icon(
                  onPressed: () => _showCreate(context, ref),
                  icon: const Icon(Icons.add),
                  label: const Text('Nova Receita'),
                ),
              ),
            ),
          Expanded(
            child: incomes.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('Erro: $e')),
              data: (list) => ListView.builder(
                itemCount: list.length,
                itemBuilder: (_, i) => ListTile(
                  title: Text(list[i].description),
                  subtitle: Text(list[i].date),
                  trailing: Text('R\$ ${list[i].amount.toStringAsFixed(2)}'),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _showCreate(BuildContext context, WidgetRef ref) async {
    final desc = TextEditingController();
    final amt = TextEditingController();
    await showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Nova receita'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [TextField(controller: desc, decoration: const InputDecoration(labelText: 'Descrição')), TextField(controller: amt, decoration: const InputDecoration(labelText: 'Valor'))],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancelar')),
          FilledButton(
            onPressed: () async {
              await ref.read(incomeRepositoryProvider).create({'date': DateTime.now().toIso8601String().split('T').first, 'description': desc.text, 'amount': double.tryParse(amt.text) ?? 0, 'source': 'App'});
              ref.invalidate(incomeProvider);
              if (context.mounted) Navigator.pop(context);
            },
            child: const Text('Salvar'),
          ),
        ],
      ),
    );
  }
}
