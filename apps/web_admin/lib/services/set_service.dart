import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:web_admin/models/mtg_set.dart';

const _url = 'https://firebasestorage.googleapis.com/v0/b/'
    'octodecks.firebasestorage.app/o/exports%2Fsets.json?alt=media';

class SetService {
  static Future<List<MtgSet>> fetchSets() async {
    final res = await http.get(Uri.parse(_url));
    if (res.statusCode != 200) throw Exception('HTTP ${res.statusCode}');
    final List data = jsonDecode(res.body);
    return data.map((e) => MtgSet.fromJson(e)).toList()
      ..sort((a, b) => b.releaseDate.compareTo(a.releaseDate));
  }
}
