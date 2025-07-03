// lib/theme/octo_theme.dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class OctoColors {
  static const Color background = Color(0xFF2C2C34);
  static const Color surface = Color(0xFF3A3A45);
  static const Color borderNeon = Color(0xFF00FFFF);
  static const Color pinkNeon = Color(0xFFFF00FF);
  static const Color greenNeon = Color(0xFF00FF90);
  static const Color yellowNeon = Color(0xFFFFCC00);
  static const Color orangeNeon = Color(0xFFFF6600);
  static const Color purpleNeon = Color(0xFFB388FF);
  static const Color text = Color(0xFFEFEFEF);
  static const Color disabled = Colors.grey;
}

class OctoTheme {
  static ThemeData get theme {
    return ThemeData.dark().copyWith(
      scaffoldBackgroundColor: OctoColors.background,
      canvasColor: OctoColors.background,
      cardColor: OctoColors.surface,
      primaryColor: OctoColors.borderNeon,
      textTheme: GoogleFonts.orbitronTextTheme().apply(
        bodyColor: OctoColors.text,
        displayColor: OctoColors.text,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: OctoColors.borderNeon,
          foregroundColor: Colors.black,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
      ),
      cardTheme: CardThemeData(
        color: OctoColors.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(color: OctoColors.borderNeon, width: 1.5),
        ),
        elevation: 4,
        shadowColor: OctoColors.borderNeon.withOpacity(0.4),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: OctoColors.surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide(color: OctoColors.borderNeon),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide(color: OctoColors.borderNeon),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide(color: OctoColors.pinkNeon),
        ),
        labelStyle: TextStyle(color: OctoColors.text),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: OctoColors.surface,
        disabledColor: OctoColors.disabled,
        selectedColor: OctoColors.greenNeon.withOpacity(0.2),
        secondarySelectedColor: OctoColors.greenNeon.withOpacity(0.4),
        padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        labelStyle: TextStyle(color: OctoColors.text),
        secondaryLabelStyle: TextStyle(color: OctoColors.text),
        brightness: Brightness.dark,
      ),
    );
  }
}
