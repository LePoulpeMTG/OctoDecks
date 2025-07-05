
import 'package:flutter/material.dart';

class OctoColors {
  static const Color background = Color(0xFF1D1F23); // Anthracite sombre
  static const Color surface = Color(0xFF2A2D32);     // Un peu plus clair pour les containers

  static const Color octoPink = Color(0xFFFF2EC4);     // Néon rose (logo)
  static const Color octoCyan = Color(0xFF00F0FF);     // Néon cyan (accents, bordures)
  static const Color octoYellow = Color(0xFFFFF740);   // Néon jaune (texte secondaire)
  static const Color octoGreen = Color(0xFF00FF9F);    // Vert fluo (confirm)
  static const Color octoPurple = Color(0xFFB367FF);   // Violet néon (labels, sets...)

  static const Color white = Colors.white;
  static const Color disabled = Colors.grey;
}

class OctoTheme {
  static const BorderRadius baseRadius = BorderRadius.all(Radius.circular(16));

  static const double elevation = 4;

  static const TextStyle heading = TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.bold,
    color: OctoColors.white,
    letterSpacing: 1.2,
  );

  static const TextStyle button = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.bold,
    color: OctoColors.white,
    letterSpacing: 1,
  );

  static const TextStyle tag = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w600,
    color: OctoColors.octoYellow,
  );

  static BoxDecoration glowingBorder(Color color) {
    return BoxDecoration(
      borderRadius: baseRadius,
      border: Border.all(color: color, width: 2),
      boxShadow: [
        BoxShadow(
          color: color.withOpacity(0.6),
          blurRadius: 10,
          spreadRadius: 1,
        ),
      ],
    );
  }
}
