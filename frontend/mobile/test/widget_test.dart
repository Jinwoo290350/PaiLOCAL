import 'package:flutter_test/flutter_test.dart';
import 'package:pailocal_traveler_app_fixed/main.dart';

void main() {
  testWidgets('App boot smoke test', (tester) async {
    await tester.pumpWidget(const PailocalApp());
    expect(find.text('P(AI)LOCAL+'), findsWidgets);
  });
}
