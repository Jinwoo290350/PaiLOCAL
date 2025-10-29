import 'package:flutter/material.dart';
import '../widgets/common_widgets.dart';
import '../core/responsive.dart';

class PlanMyTripPage extends StatelessWidget {
  const PlanMyTripPage({super.key});
  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return ListView(
      padding: context.pagePadding,
      children: [
        Text('Plan My Trip', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 12),
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: const [
            IconChip(icon: Icons.park_outlined, label: 'Conservative'),
            IconChip(icon: Icons.nature_outlined, label: 'Naturalist'),
            IconChip(icon: Icons.camera_alt_outlined, label: 'Photogenic'),
            IconChip(icon: Icons.local_cafe_outlined, label: 'Café•ist'),
            IconChip(icon: Icons.home_outlined, label: 'Based on hood'),
            IconChip(icon: Icons.cloud_outlined, label: 'Based on weather'),
          ],
        ),
        const SizedBox(height: 16),
        FeatureCard(
          title: 'Real-time map (AI)',
          subtitle:
              'Estimated arrival 2h30 • Distance 15.5 km • Reduced carbon 0.8 kg CO₂e',
          header: Container(
            height: 160,
            decoration: BoxDecoration(
              color: cs.primaryContainer.withOpacity(.5),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Center(child: Icon(Icons.map, size: 64)),
          ),
          footer: const [
            IconChip(icon: Icons.place, label: 'Wat Phrakaew'),
            IconChip(icon: Icons.directions_walk, label: 'My Trip'),
            IconChip(icon: Icons.settings, label: 'Options'),
          ],
        ),
      ],
    );
  }
}
