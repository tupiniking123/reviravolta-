import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/utils/providers.dart';
import '../../auth/presentation/auth_notifier.dart';
import '../domain/farm.dart';

final farmListProvider = FutureProvider<List<Farm>>((ref) => ref.watch(farmRepositoryProvider).listFarms());

class FarmSelectorScreen extends ConsumerWidget {
  const FarmSelectorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final farms = ref.watch(farmListProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Selecione a Fazenda Ativa')),
      body: farms.when(
        data: (items) => ListView.builder(
          itemCount: items.length,
          itemBuilder: (_, i) {
            final farm = items[i];
            return ListTile(
              title: Text(farm.name),
              subtitle: Text('${farm.timezone} • ${farm.currency}'),
              onTap: () async {
                await ref.read(authNotifierProvider.notifier).setActiveFarm(farm.id);
                if (context.mounted) context.go('/');
              },
            );
          },
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro ao carregar fazendas: $e')),
      ),
    );
  }
}
