import 'package:flutter/material.dart';
import '../core/responsive.dart';
import '../widgets/common_widgets.dart';

class LocationDetailPage extends StatelessWidget {
  const LocationDetailPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: context.pagePadding,
      children: [
        Text('Wat Phra Kaew', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 10),
        Card(
          clipBehavior: Clip.antiAlias,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(18),
            child: AspectRatio(
              aspectRatio: 16 / 9,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Image.asset(
                    'assets/images/wat_phra_kaew.jpg',
                    fit: BoxFit.cover,
                  ),
                  Align(
                    alignment: Alignment.center,
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.black.withValues(alpha: .35),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.play_circle,
                            size: 24,
                            color: Colors.white,
                          ),
                          SizedBox(width: 8),
                          Text(
                            'Watch video',
                            style: TextStyle(color: Colors.white),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SectionHeader('History and Culture'),
        const FeatureCard(
          title: 'Background',
          subtitle:
              'The Temple of the Emerald Buddha is Thailand’s most sacred Buddhist temple.',
        ),
        const SectionHeader('Review From Tourists', actionText: 'See all'),
        const FeatureCard(
          title: 'Jay Wang',
          subtitle:
              '“Absolutely breathtaking! The details left me completely awestruck.”',
          footer: [IconChip(icon: Icons.star, label: '4.9')],
        ),
        const SizedBox(height: 8),
        const Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            IconChip(icon: Icons.view_in_ar, label: 'AR Guide'),
            IconChip(icon: Icons.volume_up, label: 'Audio Story'),
          ],
        ),
      ],
    );
  }
}
