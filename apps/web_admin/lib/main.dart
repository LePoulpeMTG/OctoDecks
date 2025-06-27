import 'package:flutter/material.dart';
import 'screens/set_explore.dart';


void main() {
  print('🔷 App started');
  runApp(const OctoAdminApp());
}
class OctoAdminApp extends StatelessWidget {
  const OctoAdminApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OctoDecks Admin',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
      debugShowCheckedModeBanner: false,

      // ─── Routage ───────────────────────────────────────────────────
      initialRoute: '/',
      routes: {
        '/':      (_) => const SetExploreScreen(),
        // '/set/:code' → sera ajouté quand l’écran de détail existera
      },
    );
  }
}
