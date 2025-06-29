import 'package:flutter/material.dart';
import 'package:core/models/mtg_set.dart';
import 'package:web_admin/services/set_service.dart';

class SetExplorePage extends StatelessWidget {
  const SetExplorePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sets MTG')),
      body: FutureBuilder<List<MtgSet>>(
        future: SetService.fetchSets(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Erreur : ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Aucun set trouvé.'));
          }

          final sets = snapshot.data!;
          return GridView.builder(
            padding: const EdgeInsets.all(8),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 5,
              childAspectRatio: 0.7,
              mainAxisSpacing: 8,
              crossAxisSpacing: 8,
            ),
            itemCount: sets.length,
            itemBuilder: (context, index) {
              final set = sets[index];
              return Card(
                child: Column(
                  children: [
                    Expanded(
                      child: Image.network(set.iconSvgUri, fit: BoxFit.contain),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(set.name, textAlign: TextAlign.center),
                    ),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}
