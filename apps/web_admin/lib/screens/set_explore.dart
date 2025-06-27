// lib/screens/set_explore.dart
import 'package:flutter/material.dart';
import '../services/set_service.dart';
import '../models/mtg_set.dart';

class SetExplorePage extends StatefulWidget {
  const SetExplorePage({super.key});

  @override
  State<SetExplorePage> createState() => _SetExplorePageState();
}

class _SetExplorePageState extends State<SetExplorePage> {
  late Future<List<MtgSet>> _future;

  @override
  void initState() {
    super.initState();
    _future = SetService.fetchSets();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sets')),
      body: FutureBuilder(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Erreur : ${snap.error}'));
          }
          final sets = snap.data as List<MtgSet>;
          return GridView.builder(
            padding: const EdgeInsets.all(12),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 4,
              childAspectRatio: .8,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
            ),
            itemCount: sets.length,
            itemBuilder: (_, i) => _SetTile(sets[i]),
          );
        },
      ),
    );
  }
}

class _SetTile extends StatelessWidget {
  final MtgSet set;
  const _SetTile(this.set);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => Navigator.pushNamed(context, '/set/${set.code}'),
      child: Card(
        elevation: 3,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // ⚠️ Pour un svg: utilise flutter_svg
            if (set.iconSvg.isNotEmpty)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Image.network(set.iconSvg, height: 64),
              ),
            Text(set.name, textAlign: TextAlign.center),
            Text('${set.releaseDate.year}', style: const TextStyle(fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
