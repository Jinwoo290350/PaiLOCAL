import 'package:flutter/material.dart';
import 'core/theme.dart';
import 'screens/home_page.dart';
import 'screens/plan_my_trip_page.dart';
import 'screens/location_detail_page.dart';
import 'screens/smart_buddy_page.dart';
import 'screens/shop_page.dart';

void main() {
  runApp(const PailocalApp());
}

class PailocalApp extends StatelessWidget {
  const PailocalApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'P(AI)LOCAL+',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.leafGreenLight,
      home: const _HomeShell(),
    );
  }
}

class _HomeShell extends StatefulWidget {
  const _HomeShell();
  @override
  State<_HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<_HomeShell> {
  int _index = 0;
  final _pages = const [
    HomePage(),
    PlanMyTripPage(),
    LocationDetailPage(),
    SmartBuddyPage(),
    ShopPage(),
  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(child: IndexedStack(index: _index, children: _pages)),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.map_outlined), label: 'Plan'),
          NavigationDestination(icon: Icon(Icons.place_outlined), label: 'Location'),
          NavigationDestination(icon: Icon(Icons.smart_toy_outlined), label: 'Buddy'),
          NavigationDestination(icon: Icon(Icons.storefront_outlined), label: 'Shop'),
        ],
      ),
    );
  }
}
