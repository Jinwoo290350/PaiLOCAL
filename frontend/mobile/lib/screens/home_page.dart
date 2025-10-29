import 'package:flutter/material.dart';
import '../core/responsive.dart';
import '../widgets/common_widgets.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    final trips = [
      ('Ecotourism', 'assets/images/old_town.jpg'),
      ('Beach Vibes', 'assets/images/beach.jpg'),
      ('Cafe Hopping', 'assets/images/cafe.jpg'),
      ('Old Town Walk', 'assets/images/old_town.jpg'),
      ('Local Food', 'assets/images/local_food.jpg'),
      ('Bangkok City', 'assets/images/banner_bangkok.jpg'),
    ];

    return CustomScrollView(
      slivers: [
        SliverAppBar(
          pinned: true,
          title: const Text('P(AI)LOCAL+'),
          actions: [
            IconButton(onPressed: () {}, icon: const Icon(Icons.notifications)),
          ],
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: context.pagePadding,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  decoration: InputDecoration(
                    hintText: 'Search for locations',
                    prefixIcon: const Icon(Icons.search),
                    filled: true,
                    fillColor: cs.surface,
                    border: OutlineInputBorder(
                      borderSide: BorderSide(color: cs.outlineVariant),
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                FeatureCard(
                  header: ClipRRect(
                    borderRadius: BorderRadius.circular(16),
                    child: AspectRatio(
                      aspectRatio: 16 / 9,
                      child: Stack(
                        fit: StackFit.expand,
                        children: [
                          Image.asset(
                            'assets/images/banner_bangkok.jpg',
                            fit: BoxFit.cover,
                          ),
                          DecoratedBox(
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomCenter,
                                colors: [
                                  Colors.black.withValues(alpha: .10),
                                  Colors.black.withValues(alpha: .25),
                                ],
                              ),
                            ),
                          ),
                          Align(
                            alignment: Alignment.center,
                            child: Text(
                              'Bangkok • 30°C',
                              style: Theme.of(context).textTheme.headlineSmall
                                  ?.copyWith(
                                    color: Colors.white,
                                    fontWeight: FontWeight.w700,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  title: 'Plan my trip',
                  subtitle:
                      'Quickly start planning with AI suggestions and local insight.',
                  footer: const [
                    IconChip(icon: Icons.eco, label: 'Eco-score 9.2'),
                    IconChip(icon: Icons.cloud, label: 'Chance of rain 23%'),
                  ],
                ),

                const SectionHeader('Suggested Trips', actionText: 'See all'),

                SizedBox(
                  height: 170,
                  child: ListView.separated(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    scrollDirection: Axis.horizontal,
                    itemCount: trips.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 12),
                    itemBuilder: (_, i) {
                      final (title, img) = trips[i];
                      return AspectRatio(
                        aspectRatio: 1.35,
                        child: Card(
                          clipBehavior: Clip.antiAlias,
                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              Image.asset(img, fit: BoxFit.cover),
                              Align(
                                alignment: Alignment.bottomLeft,
                                child: Container(
                                  margin: const EdgeInsets.all(8),
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 8,
                                    vertical: 4,
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.black.withValues(alpha: .35),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text(
                                    title,
                                    style: const TextStyle(color: Colors.white),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),

                const SectionHeader('Top Pick Trip'),
                FeatureCard(
                  header: ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: AspectRatio(
                      aspectRatio: 16 / 9,
                      child: Image.asset(
                        'assets/images/local_food.jpg',
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  title: 'Local Food Tour',
                  subtitle:
                      'Explore culinary heritage with friendly local hosts.',
                  footer: const [
                    IconChip(icon: Icons.timer, label: '2.5h'),
                    IconChip(icon: Icons.route, label: '15 km'),
                    IconChip(icon: Icons.co2, label: '-0.8 kg CO₂e'),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
