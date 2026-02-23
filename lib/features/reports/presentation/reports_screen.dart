import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';

class ReportsScreen extends ConsumerWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    Future<void> download(String name) async {
      final csv = await ref.read(exportRepositoryProvider).downloadCsv(name);
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('CSV $name baixado em memória (${csv.length} bytes)')));
      }
    }

    return AdaptiveScaffold(
      title: 'Export Power BI',
      selectedIndex: 6,
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Wrap(spacing: 8, runSpacing: 8, children: [
            FilledButton(onPressed: () => download('financial_monthly'), child: const Text('financial_monthly')),
            FilledButton(onPressed: () => download('expenses_by_category'), child: const Text('expenses_by_category')),
            FilledButton(onPressed: () => download('cashflow_daily'), child: const Text('cashflow_daily')),
            FilledButton(onPressed: () => download('inventory_status'), child: const Text('inventory_status')),
            FilledButton(onPressed: () => download('vaccinations_due'), child: const Text('vaccinations_due')),
          ]),
        ],
      ),
    );
  }
}
