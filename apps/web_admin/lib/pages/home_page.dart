import 'package:flutter/material.dart';
import 'set_explore_page.dart'; // à adapter selon le nom exact

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Column(
          children: [
            // BANNIÈRE
            Flexible(
              flex: 2,
              child: Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage("assets/icons/banner/banner_octodecks_1.png"),
                    fit: BoxFit.cover,
                  ),
                ),
                alignment: Alignment.center,
                child: Text(
                  "OctoDeck - Tableau de bord Capitaine",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    shadows: [
                      Shadow(blurRadius: 10, color: Colors.black, offset: Offset(2, 2))
                    ],
                  ),
                ),
              ),
            ),

            // ONGLET NAVIGATION
            const TabBar(
              labelColor: Colors.amber,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Colors.amber,
              tabs: [
                Tab(text: "KPI"),
                Tab(text: "Sets"),
                Tab(text: "Détail Set"),
                Tab(text: "Carte"),
              ],
            ),

            // CONTENU PAR ONGLET
            const Expanded(
              flex: 8,
              child: TabBarView(
                children: [
                  Center(child: Text("📊 Page KPI à venir", style: TextStyle(color: Colors.white))),
                  SetExplorePage(),
                  Center(child: Text("🧾 Détail Set à faire", style: TextStyle(color: Colors.white))),
                  Center(child: Text("🃏 Détail Carte à faire", style: TextStyle(color: Colors.white))),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
