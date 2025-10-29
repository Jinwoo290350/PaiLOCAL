import 'package:flutter/material.dart';
import '../core/responsive.dart';

class ShopPage extends StatelessWidget {
  const ShopPage({super.key});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    final crossAxisCount = context.isTablet || context.isDesktop ? 3 : 2;

    return ListView(
      padding: context.pagePadding,
      children: [
        Text(
          'Marketplace (OTOP)',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 12),

        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _items.length,
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: crossAxisCount,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            childAspectRatio: context.isPhone ? 0.72 : 0.82,
          ),
          itemBuilder: (_, i) {
            final it = _items[i];
            return Card(
              clipBehavior: Clip.antiAlias,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18),
              ),
              child: InkWell(
                onTap: () {},
                child: Padding(
                  padding: const EdgeInsets.all(10),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(14),
                        child: AspectRatio(
                          aspectRatio: 4 / 3,
                          child: Image.asset(it.image, fit: BoxFit.cover),
                        ),
                      ),
                      const SizedBox(height: 8),

                      Text(
                        it.title,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: Theme.of(context).textTheme.titleMedium,
                      ),

                      const SizedBox(height: 4),

                      Text(
                        it.subtitle,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          color: cs.onSurfaceVariant,
                          height: 1.15,
                        ),
                      ),

                      const Spacer(),

                      Row(
                        children: [
                          Icon(
                            Icons.shopping_bag_outlined,
                            size: 18,
                            color: cs.primary,
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              it.tag,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                color: cs.primary,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            );
          },
        ),

        const SizedBox(height: 12),

        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: const [
            _SmallFilterChip(icon: Icons.eco, label: 'Eco'),
            _SmallFilterChip(
              icon: Icons.local_shipping_outlined,
              label: 'Local',
            ),
            _SmallFilterChip(icon: Icons.handshake_outlined, label: 'Fair'),
          ],
        ),
      ],
    );
  }
}

class _SmallFilterChip extends StatelessWidget {
  final IconData icon;
  final String label;
  const _SmallFilterChip({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: cs.primary.withOpacity(.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: cs.outlineVariant),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: cs.primary),
          const SizedBox(width: 6),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}

// -------------------- DATA --------------------

class _ShopItem {
  final String image;
  final String title;
  final String subtitle;
  final String tag;
  const _ShopItem(this.image, this.title, this.subtitle, this.tag);
}

const _items = <_ShopItem>[
  _ShopItem(
    'assets/images/local_food.jpg',
    'Local',
    'Eco • Fair • Handmade',
    'Local Artisan',
  ),
  _ShopItem(
    'assets/images/cafe.jpg',
    'Cafe Drip',
    'Community Café',
    'Specialty',
  ),
  _ShopItem(
    'assets/images/old_town.jpg',
    'Old Town',
    'Local Artisan',
    'Crafts',
  ),
  _ShopItem(
    'assets/images/banner_bangkok.jpg',
    'Bangkok',
    'City Print',
    'Souvenir',
  ),
  _ShopItem('assets/images/beach.jpg', 'Beach', 'Low-plastic', 'Ocean-safe'),
  _ShopItem(
    'assets/images/wat_phra_kaew.jpg',
    'Temple',
    'Wat Phra Kaew',
    'Cultural',
  ),
];
