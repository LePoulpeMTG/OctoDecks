// lib/screens/set_explore.dart
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

import '../models/mtg_set.dart';
import '../services/set_service.dart';

class SetExploreScreen extends StatelessWidget {
  const SetExploreScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MTG – Toutes les éditions'),
      ),
      body: FutureBuilder<List<MtgSet>>(
        future: SetService.fetchSets(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Text(
                'Erreur : ${snapshot.error}',
                style: const TextStyle(color: Colors.red),
              ),
            );
          }

          final sets = snapshot.data!;
          return GridView.builder(
            padding: const EdgeInsets.all(8),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 3,            // 3 colonnes
              mainAxisSpacing: 8,
              crossAxisSpacing: 8,
              childAspectRatio: .8,
            ),
            itemCount: sets.length,
            itemBuilder: (context, index) {
              final set = sets[index];
              return _SetTile(set: set);
            },
          );
        },
      ),
    );
  }
}

class _SetTile extends StatelessWidget {
  final MtgSet set;
  const _SetTile({required this.set});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        // TODO: Naviguer vers SetDetail lorsque l’écran sera prêt
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('⤵ ${set.name}')));
      },
      child: Card(
        elevation: 3,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // ─── Icône SVG ou placeholder ──────────────────────────────
            if (set.iconSvgUri.isNotEmpty)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: SvgPicture.network(
                  set.iconSvgUri,
                  height: 64,
                  placeholderBuilder: (ctx) =>
                      const SizedBox(height: 64, child: Center(child: CircularProgressIndicator(strokeWidth: 1.5))),
                ),
              ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4),
              child: Text(
                set.name,
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Text(
              '${set.releaseDate.year}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
