import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../../../core/utils/skeleton.dart';
import '../../alerts/domain/alert_item.dart';
import '../../auth/presentation/auth_notifier.dart';

final dashboardRangeProvider = StateProvider<DateTimeRange>((ref) {
  final now = DateTime.now();
  return DateTimeRange(start: DateTime(now.year, now.month, 1), end: now);
});

final dashboardSummaryProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final range = ref.watch(dashboardRangeProvider);
  final fmt = DateFormat('yyyy-MM-dd');
  return ref.watch(dashboardRepositoryProvider).summary(fmt.format(range.start), fmt.format(range.end));
});

final alertsPreviewProvider = FutureProvider<List<AlertItem>>((ref) async {
  return ref.watch(alertsRepositoryProvider).list();
});

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summary = ref.watch(dashboardSummaryProvider);
    final alerts = ref.watch(alertsPreviewProvider);
    final user = ref.watch(authNotifierProvider).user;

    return AdaptiveScaffold(
      title: 'Dashboard',
      selectedIndex: 0,
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Wrap(spacing: 8, runSpacing: 8, children: [
            Chip(label: Text('Role: ${user?.role ?? 'N/A'}')),
            OutlinedButton.icon(
              onPressed: () async {
                final current = ref.read(dashboardRangeProvider);
                final picked = await showDateRangePicker(
                  context: context,
                  firstDate: DateTime(2020),
                  lastDate: DateTime.now(),
                  initialDateRange: current,
                );
                if (picked != null) ref.read(dashboardRangeProvider.notifier).state = picked;
              },
              icon: const Icon(Icons.filter_alt),
              label: const Text('Filtrar período'),
            ),
          ]),
          const SizedBox(height: 12),
          summary.when(
            loading: () => const SkeletonBox(height: 120),
            error: (e, _) => Text('Erro: $e'),
            data: (s) {
              final kpis = {
                'Receita Total': s['total_income'] ?? 0,
                'Despesa Total': s['total_expense'] ?? 0,
                'Lucro Bruto': s['gross_profit'] ?? 0,
                'Lucro Líquido': s['net_profit'] ?? 0,
              };
              return Wrap(
                spacing: 8,
                runSpacing: 8,
                children: kpis.entries
                    .map((e) => SizedBox(
                          width: 220,
                          child: Card(
                            child: ListTile(
                              title: Text(e.key),
                              subtitle: Text(NumberFormat.currency(locale: 'pt_BR', symbol: 'R\$').format(e.value)),
                            ),
                          ),
                        ))
                    .toList(),
              );
            },
          ),
          const SizedBox(height: 16),
          const Text('Margens e Tendência', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          SizedBox(
            height: 220,
            child: LineChart(
              LineChartData(lineBarsData: [
                LineChartBarData(spots: const [FlSpot(0, 10), FlSpot(1, 30), FlSpot(2, 25), FlSpot(3, 40)], isCurved: true),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Despesas por categoria', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          SizedBox(
            height: 220,
            child: PieChart(
              PieChartData(sections: [
                PieChartSectionData(value: 35, title: 'Ração'),
                PieChartSectionData(value: 25, title: 'Vacinas'),
                PieChartSectionData(value: 40, title: 'Outros'),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Alertas recentes', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          alerts.when(
            loading: () => const SkeletonBox(height: 100),
            error: (e, _) => Text('Erro: $e'),
            data: (list) => Column(
              children: list.take(5).map((a) => ListTile(title: Text(a.title), subtitle: Text(a.message))).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
