import 'package:flutter/widgets.dart';

extension ContextSizeX on BuildContext {
  Size get mq => MediaQuery.sizeOf(this);
  double get w => mq.width;
  double get h => mq.height;

  bool get isPhone => w < 600;
  bool get isTablet => w >= 600 && w < 1024;
  bool get isDesktop => w >= 1024;

  EdgeInsets get pagePadding =>
      EdgeInsets.symmetric(horizontal: isPhone ? 16 : 28, vertical: 12);
}
