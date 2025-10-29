import 'package:flutter/material.dart';

class OverlayImage extends StatelessWidget {
  final String asset;
  final String? caption;
  final double aspect;
  final BorderRadiusGeometry radius;

  const OverlayImage({
    super.key,
    required this.asset,
    this.caption,
    this.aspect = 16 / 9,
    this.radius = const BorderRadius.all(Radius.circular(12)),
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: radius,
      child: AspectRatio(
        aspectRatio: aspect,
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.asset(asset, fit: BoxFit.cover),
            DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.black.withValues(alpha: .05),
                    Colors.black.withValues(alpha: .25),
                  ],
                ),
              ),
            ),
            if (caption != null)
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
                    caption!,
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
