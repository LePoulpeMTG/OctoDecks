import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:core/models/mtg_set.dart';

class OctoApiService {
  static const String _baseUrl = 'https://firebasestorage.googleapis.com/v0/b/octodecks.appspot.com/o';
  static const String _altParam = '?alt=media';

  /// 🔁 Lit le fichier sets.json et retourne une liste de MtgSet
  static Future<List<MtgSet>> fetchSets() async {
    final uri = Uri.parse('$_baseUrl/sets.json$_altParam');

    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);

      if (data is List) {
        return data.map((json) => MtgSet.fromJson(json)).toList();
      } else {
        throw Exception('sets.json ne contient pas une liste valide');
      }
    } else {
      throw Exception('Erreur de chargement sets.json (${response.statusCode})');
    }
  }

  /// 🔁 Fonction générique pour charger n’importe quel fichier JSON depuis Firebase
  static Future<dynamic> fetchJsonFile(String fileName) async {
    final uri = Uri.parse('$_baseUrl/$fileName$_altParam');

    final response = await http.get(uri);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Erreur de chargement $fileName (${response.statusCode})');
    }
  }
}
