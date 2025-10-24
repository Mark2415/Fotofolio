// ignore_for_file: library_private_types_in_public_api, use_build_context_synchronously, deprecated_member_use

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'search_movie_screen.dart';
import 'movie.dart';
import 'database_helper.dart';
import 'movie_detail_screen.dart';

class FavoriteListScreen extends StatefulWidget {
  // ignore: use_super_parameters
  const FavoriteListScreen({Key? key}) : super(key: key);

  @override
  _FavoriteListScreenState createState() => _FavoriteListScreenState();
}

class _FavoriteListScreenState extends State<FavoriteListScreen> {
  final dbHelper = DatabaseHelper.instance;
  List<Movie> favoriteMovies = [];

  @override
  void initState() {
    super.initState();
    _refreshFavoriteList();
  }

  void _refreshFavoriteList() async {
    final allMovies = await dbHelper.getAllFavoriteMovies();
    setState(() {
      favoriteMovies = allMovies;
    });
  }

  void _updateMovie(Movie movie) async {
    await dbHelper.update(movie);
    _refreshFavoriteList();
  }

  void _deleteMovie(int id) async {
    await dbHelper.delete(id);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Film dihapus dari watchlist!')),
    );
    _refreshFavoriteList();
  }

  void _goToSearchScreen() async {
    await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SearchMovieScreen()),
    );
    _refreshFavoriteList();
  }

  void _goToDetailScreen(Movie movie) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => MovieDetailScreen(movie: movie)),
    );
  }

  Widget _buildRatingStars(Movie movie) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (index) {
        return IconButton(
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
          icon: Icon(
            index < movie.rating ? Icons.star : Icons.star_border,
            color: Colors.amber,
            size: 22,
          ),
          onPressed: () {
            setState(() {
              movie.rating = index + 1;
            });
            _updateMovie(movie);
          },
        );
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "My Movie Watch List",
          style: GoogleFonts.kaushanScript(fontSize: 32, color: Colors.white),
          textAlign: TextAlign.center,
        ),
        backgroundColor: const Color(0xFF0D1B2A),
      ),
      backgroundColor: const Color(0xFF4A4A4A),
      body: favoriteMovies.isEmpty
          ? Center(
              child: Text(
                'Watchlist Anda kosong.\nTekan tombol Cari untuk menambahkan film!',
                textAlign: TextAlign.center,
                style: GoogleFonts.poppins(fontSize: 18, color: Colors.white70),
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: favoriteMovies.length,
              itemBuilder: (context, index) {
                final movie = favoriteMovies[index];
                final posterUrl =
                    'https://image.tmdb.org/t/p/w200${movie.posterPath}';
                return Card(
                  color: const Color(0xFF1B263B),
                  elevation: 5,
                  margin: const EdgeInsets.symmetric(vertical: 8),
                  child: Column(
                    children: [
                      ListTile(
                        contentPadding:
                            const EdgeInsets.fromLTRB(15, 10, 5, 10),
                        onTap: () => _goToDetailScreen(movie),
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(4.0),
                          child: Image.network(
                            posterUrl,
                            fit: BoxFit.cover,
                            width: 60,
                            errorBuilder: (context, error, stackTrace) =>
                                Container(
                                    width: 60,
                                    height: 90,
                                    color: Colors.grey.shade800,
                                    child: const Icon(Icons.movie,
                                        color: Colors.white)),
                          ),
                        ),
                        title: Text(
                          movie.title,
                          style: GoogleFonts.poppins(
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                              fontSize: 16),
                        ),
                        subtitle: Padding(
                          padding: const EdgeInsets.only(top: 5.0),
                          child: Text(
                            movie.overview,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: GoogleFonts.poppins(
                                color: Colors.white60, fontSize: 12),
                          ),
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete_forever,
                              color: Colors.redAccent, size: 28),
                          onPressed: () => _deleteMovie(movie.id),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 15, vertical: 5),
                        color: const Color(0xFF0D1B2A).withOpacity(0.5),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Row(
                              children: [
                                Checkbox(
                                  value: movie.isWatched,
                                  onChanged: (bool? value) {
                                    setState(() {
                                      movie.isWatched = value ?? false;
                                      if (!movie.isWatched) movie.rating = 0;
                                    });
                                    _updateMovie(movie);
                                  },
                                  checkColor: Colors.white,
                                  activeColor: Colors.green,
                                ),
                                Text(
                                  "Sudah ditonton",
                                  style:
                                      GoogleFonts.poppins(color: Colors.white),
                                ),
                              ],
                            ),
                            if (movie.isWatched) _buildRatingStars(movie),
                          ],
                        ),
                      )
                    ],
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _goToSearchScreen,
        tooltip: 'Cari Film',
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0D1B2A),
        child: const Icon(Icons.search),
      ),
    );
  }
}
