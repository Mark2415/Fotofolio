class Movie {
  final int id;
  final String title;
  final String overview;
  final String posterPath;

  // Field ini dapat diubah oleh pengguna
  bool isWatched;
  int rating;

  Movie({
    required this.id,
    required this.title,
    required this.overview,
    required this.posterPath,
    this.isWatched = false,
    this.rating = 0,
  });

  // Konversi dari JSON (API) ke objek Movie
  factory Movie.fromJson(Map<String, dynamic> json) {
    return Movie(
      id: json['id'],
      title: json['title'],
      overview: json['overview'],
      posterPath: json['poster_path'] ?? '',
    );
  }

  // Konversi dari objek Movie ke Map untuk disimpan di SQLite
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'overview': overview,
      'posterPath': posterPath,
      'isWatched': isWatched ? 1 : 0, // SQLite menggunakan 1 (true) atau 0 (false)
      'rating': rating,
    };
  }

  // Konversi dari Map (dari SQLite) ke objek Movie
  factory Movie.fromMap(Map<String, dynamic> map) {
    return Movie(
      id: map['id'],
      title: map['title'],
      overview: map['overview'],
      posterPath: map['posterPath'],
      isWatched: map['isWatched'] == 1, // Konversi 1/0 kembali ke true/false
      rating: map['rating'],
    );
  }
}