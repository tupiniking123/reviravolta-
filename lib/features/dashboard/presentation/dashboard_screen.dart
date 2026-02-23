import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../core/utils/adaptive_scaffold.dart';
import '../../../core/utils/feature_providers.dart';
import '../../alerts/domain/alert_item.dart';

final dashboardSummaryProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final now = DateTime.now();
  final start = DateFormat('yyyy-MM-01').format(now);
  final end = DateFormat('yyyy-MM-dd').format(now);
  return ref.watch(dashboardRepositoryProvider).summary(start, end);
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

    return AdaptiveScaffold(
      title: 'Início',
      selectedIndex: 0,
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          summary.when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('Erro ao carregar resumo: $e'),
            data: (s) {
              final items = [
                ('Receita', s['total_income'] ?? 0),
                ('Despesa', s['total_expense'] ?? 0),
                ('Lucro Bruto', s['gross_profit'] ?? 0),
                ('Lucro Líquido', s['net_profit'] ?? 0),
              ];
              return Wrap(
                spacing: 8,
                runSpacing: 8,
                children: items
                    .map(
                      (i) => SizedBox(
                        width: 210,
                        child: Card(
                          child: ListTile(
                            title: Text(i.$1),
                            subtitle: Text(NumberFormat.currency(locale: 'pt_BR', symbol: 'R\$').format(i.$2)),
                          ),
                        ),
                      ),
                    )
                    .toList(),
              );
            },
          ),
          const SizedBox(height: 16),
          const Text('Tendência (simples)'),
          SizedBox(
            height: 180,
            child: LineChart(
              LineChartData(
                titlesData: const FlTitlesData(show: false),
                borderData: FlBorderData(show: false),
                lineBarsData: [
                  LineChartBarData(spots: const [FlSpot(0, 10), FlSpot(1, 20), FlSpot(2, 15), FlSpot(3, 30)], isCurved: true),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Alertas recentes'),
          alerts.when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('Erro ao carregar alertas: $e'),
            data: (list) => Column(
              children: list.take(5).map((a) => ListTile(title: Text(a.title), subtitle: Text(a.message))).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
