import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AdaptiveScaffold extends StatelessWidget {
  final Widget body;
  final String title;
  final int selectedIndex;

  const AdaptiveScaffold({super.key, required this.body, required this.title, required this.selectedIndex});

  static const destinations = [
    ('Dashboard', '/'),
    ('Receitas', '/income'),
    ('Despesas', '/expense'),
    ('Estoque', '/inventory'),
    ('Vacinação', '/vaccinations'),
    ('Alertas', '/alerts'),
    ('Relatórios', '/reports'),
    ('Config', '/settings'),
  ];

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.sizeOf(context).width >= 900;
    if (isDesktop) {
      return Scaffold(
        body: Row(
          children: [
            NavigationRail(
              selectedIndex: selectedIndex,
              onDestinationSelected: (index) => context.go(destinations[index].$2),
              labelType: NavigationRailLabelType.all,
              destinations: destinations
                  .map((d) => NavigationRailDestination(icon: const Icon(Icons.chevron_right), label: Text(d.$1)))
                  .toList(),
            ),
            const VerticalDivider(width: 1),
            Expanded(
              child: Scaffold(
                appBar: AppBar(title: Text(title)),
                body: body,
              ),
            ),
          ],
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: body,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex > 4 ? 0 : selectedIndex,
        onDestinationSelected: (index) => context.go(destinations[index].$2),
        destinations: destinations.take(5).map((d) => NavigationDestination(icon: const Icon(Icons.circle), label: d.$1)).toList(),
      ),
    );
  }
}
