// lib/pages/styleguide_page.dart
import 'package:flutter/material.dart';
import '../theme/octo_theme.dart';
import '../widgets/octo_button.dart';

class StyleguidePage extends StatelessWidget {
  const StyleguidePage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('🎨 Styleguide OctoDecks')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
        const SizedBox(height: 32),
        Text('OctoButton Demo', style: OctoTheme.heading),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action principale',
          onPressed: () {},
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action cyan',
          onPressed: () {},
          variant: OctoButtonVariant.cyan,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action désactivée',
          onPressed: null,
          variant: OctoButtonVariant.disabled,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action large',
          onPressed: () {},
          expand: true,
        ),

            Text('Typographie', style: theme.textTheme.headlineLarge),
            const SizedBox(height: 8),
            Text('Headline Medium', style: theme.textTheme.headlineMedium),
            Text('Body Medium', style: theme.textTheme.bodyMedium),
            Text('Caption', style: theme.textTheme.labelSmall),

            const Divider(height: 32),
            Text('Boutons', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
        const SizedBox(height: 32),
        Text('OctoButton Demo', style: OctoTheme.heading),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action principale',
          onPressed: () {},
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action cyan',
          onPressed: () {},
          variant: OctoButtonVariant.cyan,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action désactivée',
          onPressed: null,
          variant: OctoButtonVariant.disabled,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action large',
          onPressed: () {},
          expand: true,
        ),

                ElevatedButton(onPressed: () {}, child: const Text('Primary')),
                OutlinedButton(onPressed: () {}, child: const Text('Secondary')),
                TextButton(onPressed: () {}, child: const Text('TextButton')),
              ],
            ),

            const Divider(height: 32),
            Text('Chip + Card', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
        const SizedBox(height: 32),
        Text('OctoButton Demo', style: OctoTheme.heading),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action principale',
          onPressed: () {},
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action cyan',
          onPressed: () {},
          variant: OctoButtonVariant.cyan,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action désactivée',
          onPressed: null,
          variant: OctoButtonVariant.disabled,
        ),
        SizedBox(height: 12),
        OctoButton(
          label: 'Action large',
          onPressed: () {},
          expand: true,
        ),

                Chip(label: const Text('Chip normal')),
                FilterChip(
  label: const Text('Chip sélectionné'),
  selected: true,
  onSelected: (_) {},
),
              ],
            ),
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Carte exemple'),
                    SizedBox(height: 4),
                    Text('Contenu dans une Card personnalisée.'),
                  ],
                ),
              ),
            ),

            const Divider(height: 32),
            Text('InputField', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            TextField(
              decoration: const InputDecoration(
                labelText: 'Champ de saisie themed',
                hintText: 'Tape ici',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
