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
            Padding(
              padding: const EdgeInsets.all(12),
              child: FilledButton(
                onPressed: () async {
                  await ref.read(incomeRepositoryProvider).create({
                    'date': DateTime.now().toIso8601String().split('T').first,
                    'description': 'Receita rápida',
                    'amount': 0,
                    'source': 'App',
                  });
                  ref.invalidate(incomeProvider);
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Receita criada (modo simples)')));
                  }
                },
                child: const Text('Nova Receita Rápida'),
              ),
            ),
          Expanded(
            child: incomes.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('Erro: $e')),
              data: (list) => ListView(
                children: list
                    .map((i) => ListTile(
                          title: Text(i.description),
                          subtitle: Text(i.date),
                          trailing: Text('R\$ ${i.amount.toStringAsFixed(2)}'),
                        ))
                    .toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
