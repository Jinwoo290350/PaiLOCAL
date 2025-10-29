import 'package:flutter/material.dart';
import '../core/responsive.dart';
import '../widgets/common_widgets.dart';

class SmartBuddyPage extends StatelessWidget {
  const SmartBuddyPage({super.key});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: context.pagePadding,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Smart Travel Buddy',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 12),
          Expanded(
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: ListView(
                  children: const [
                    _Bubble(text: 'Welcome to Smart Travel Buddy!'),
                    _Bubble(
                      text: 'Is there any local events going on at Nong Chok?',
                      isMe: true,
                    ),
                    _Bubble(
                      text:
                          'Yes, a local OTOP food fair is going on at Koo Sai Mall.',
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: TextField(
                  decoration: InputDecoration(
                    hintText: 'Type your request...',
                    filled: true,
                    fillColor: Theme.of(context).colorScheme.surface,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(14),
                      borderSide: BorderSide(
                        color: Theme.of(context).colorScheme.outlineVariant,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              FilledButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.send),
                label: const Text('Send'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text(
                    'Emergency Alert',
                    style: TextStyle(fontWeight: FontWeight.w700),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Earth slide has been detected nearby your area, please proceed with care',
                  ),
                  SizedBox(height: 10),
                  Wrap(
                    spacing: 10,
                    children: [
                      IconChip(
                        icon: Icons.medical_services,
                        label: 'Request Aid',
                      ),
                      IconChip(
                        icon: Icons.warning_amber_rounded,
                        label: 'Situation Update',
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _Bubble extends StatelessWidget {
  final String text;
  final bool isMe;
  const _Bubble({required this.text, this.isMe = false});
  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: isMe ? cs.primaryContainer : cs.surfaceVariant,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(text),
      ),
    );
  }
}
