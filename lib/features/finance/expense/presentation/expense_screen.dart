import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/utils/adaptive_scaffold.dart';
import '../../../../core/utils/feature_providers.dart';
import '../../../../core/utils/rbac.dart';
import '../domain/expense.dart';

final expenseProvider = FutureProvider<List<Expense>>((ref) => ref.watch(expenseRepositoryProvider).list());

class ExpenseScreen extends ConsumerWidget {
  const ExpenseScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final expenses = ref.watch(expenseProvider);

    return AdaptiveScaffold(
      title: 'Despesas',
      selectedIndex: 2,
      body: Column(
        children: [
          if (canWrite(ref, 'finance'))
            Padding(
              padding: const EdgeInsets.all(12),
              child: FilledButton(
                onPressed: () async {
                  await ref.read(expenseRepositoryProvider).create({
                    'date': DateTime.now().toIso8601String().split('T').first,
                    'description': 'Despesa rápida',
                    'amount': 0,
                    'category_id': '00000000-0000-0000-0000-000000000000',
                  });
                  ref.invalidate(expenseProvider);
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Despesa criada (modo simples)')));
                  }
                },
                child: const Text('Nova Despesa Rápida'),
              ),
            ),
          Expanded(
            child: expenses.when(
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
