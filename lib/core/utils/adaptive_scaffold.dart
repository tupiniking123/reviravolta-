import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AdaptiveScaffold extends StatelessWidget {
  final Widget body;
  final String title;
  final int selectedIndex;

  const AdaptiveScaffold({
    super.key,
    required this.body,
    required this.title,
    required this.selectedIndex,
  });

  static const routes = [
    ('Início', '/'),
    ('Receitas', '/income'),
    ('Despesas', '/expense'),
    ('Estoque', '/inventory'),
    ('Vacinação', '/vaccinations'),
    ('Alertas', '/alerts'),
    ('Relatórios', '/reports'),
    ('Configurações', '/settings'),
  ];

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.of(context).size.width >= 900;

    if (isDesktop) {
      return Scaffold(
        body: Row(
          children: [
            NavigationRail(
              selectedIndex: selectedIndex,
              onDestinationSelected: (index) => context.go(routes[index].$2),
              labelType: NavigationRailLabelType.all,
              destinations: routes
                  .map((r) => NavigationRailDestination(
                        icon: const Icon(Icons.circle_outlined),
                        selectedIcon: const Icon(Icons.circle),
                        label: Text(r.$1),
                      ))
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
      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(child: Text('FarmOps')),
            ...routes.asMap().entries.map(
                  (e) => ListTile(
                    selected: e.key == selectedIndex,
                    title: Text(e.value.$1),
                    onTap: () {
                      Navigator.pop(context);
                      context.go(e.value.$2);
                    },
                  ),
                ),
          ],
        ),
      ),
      body: body,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex.clamp(0, 4),
        onDestinationSelected: (index) => context.go(routes[index].$2),
        destinations: routes.take(5).map((r) => NavigationDestination(icon: const Icon(Icons.circle_outlined), label: r.$1)).toList(),
      ),
    );
  }
}
