import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../domain/inventory_item.dart';

final inventoryProvider = FutureProvider<List<InventoryItem>>((ref) => ref.watch(inventoryRepositoryProvider).status());

class InventoryScreen extends ConsumerWidget {
  const InventoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final items = ref.watch(inventoryProvider);

    return AdaptiveScaffold(
      title: 'Estoque',
      selectedIndex: 3,
      body: items.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro: $e')),
        data: (list) => ListView(
          children: list
              .map(
                (item) => ListTile(
                  title: Text(item.name),
                  subtitle: Text('Saldo ${item.balance} / mínimo ${item.minLevel}'),
                  trailing: item.low ? const Chip(label: Text('Baixo')) : const Chip(label: Text('OK')),
                ),
              )
              .toList(),
        ),
      ),
    );
  }
}
