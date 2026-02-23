import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/utils/adaptive_scaffold.dart';
import '../../../../core/utils/feature_providers.dart';
import '../../../../core/utils/rbac.dart';
import '../../categories/domain/category.dart';
import '../domain/expense.dart';

final expenseProvider = FutureProvider<List<Expense>>((ref) => ref.watch(expenseRepositoryProvider).list());
final categoriesProvider = FutureProvider<List<ExpenseCategory>>((ref) => ref.watch(categoriesRepositoryProvider).list());

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
            Align(
              alignment: Alignment.centerRight,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: FilledButton.icon(onPressed: () => _showCreate(context, ref), icon: const Icon(Icons.add), label: const Text('Nova Despesa')),
              ),
            ),
          Expanded(
            child: expenses.when(
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
    String? selectedCategory;
    final cats = await ref.read(categoriesProvider.future);
    selectedCategory = cats.isNotEmpty ? cats.first.id : null;

    await showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Nova despesa'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButton<String>(
                value: selectedCategory,
                items: cats.map((c) => DropdownMenuItem(value: c.id, child: Text(c.name))).toList(),
                onChanged: (v) => setState(() => selectedCategory = v),
              ),
              TextField(controller: desc, decoration: const InputDecoration(labelText: 'Descrição')),
              TextField(controller: amt, decoration: const InputDecoration(labelText: 'Valor')),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancelar')),
            FilledButton(
              onPressed: () async {
                await ref.read(expenseRepositoryProvider).create({'date': DateTime.now().toIso8601String().split('T').first, 'category_id': selectedCategory, 'description': desc.text, 'amount': double.tryParse(amt.text) ?? 0});
                ref.invalidate(expenseProvider);
                if (context.mounted) Navigator.pop(context);
              },
              child: const Text('Salvar'),
            ),
          ],
        ),
      ),
    );
  }
}
