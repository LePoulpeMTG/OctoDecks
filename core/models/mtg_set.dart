class MtgSet {
  final String code;
  final String name;
  final DateTime releaseDate;
  final String iconSvgUri;      // 👈 nouveau champ
  final int cardsTotal;

  MtgSet({
    required this.code,
    required this.name,
    required this.releaseDate,
    required this.iconSvgUri,
    required this.cardsTotal,
  });

  factory MtgSet.fromJson(Map<String, dynamic> json) {
    return MtgSet(
      code:        json['set_code']      as String,
      name:        json['name']          as String,
      releaseDate: DateTime.parse(json['release_date'] as String),
      iconSvgUri:  json['icon_svg_uri']  as String? ?? '',
      cardsTotal:  json['total_cards']   as int?    ?? 0,
    );
  }
}
