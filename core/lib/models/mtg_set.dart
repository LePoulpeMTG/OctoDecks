class MtgSet {
  final String code;
  final String name;
  final DateTime releaseDate;
  final String iconSvgUri;
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
      code: json['set_code'] as String,
      name: json['name'] as String,
      releaseDate: DateTime.tryParse(json['release_date'] ?? '') ?? DateTime(1900),
      iconSvgUri: json['icon_svg_uri'] ?? '',
      cardsTotal: json['total_cards'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'set_code': code,
      'name': name,
      'release_date': releaseDate.toIso8601String(),
      'icon_svg_uri': iconSvgUri,
      'total_cards': cardsTotal,
    };
  }

  @override
  String toString() {
    return 'MtgSet($code, $name, $cardsTotal cartes)';
  }
}
