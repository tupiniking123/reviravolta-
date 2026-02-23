import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../../../core/utils/rbac.dart';
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
      body: Column(
        children: [
          if (canWrite(ref, 'inventory'))
            Align(
              alignment: Alignment.centerRight,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: FilledButton(
                  onPressed: () => _movement(context, ref),
                  child: const Text('Registrar Movimento'),
                ),
              ),
            ),
          Expanded(
            child: items.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('Erro: $e')),
              data: (list) => ListView.builder(
                itemCount: list.length,
                itemBuilder: (_, i) {
                  final item = list[i];
                  final expiring = item.expiresAt != null;
                  return ListTile(
                    title: Text(item.name),
                    subtitle: Text('Saldo: ${item.balance} | Mínimo: ${item.minLevel}'),
                    trailing: Wrap(spacing: 8, children: [
                      if (item.low) const Chip(label: Text('Baixo'), backgroundColor: Colors.redAccent),
                      if (expiring) const Chip(label: Text('Venc. próximo'), backgroundColor: Colors.orangeAccent),
                    ]),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _movement(BuildContext context, WidgetRef ref) async {
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Use endpoint /inventory/movements para entrada/saída detalhada')));
  }
}
