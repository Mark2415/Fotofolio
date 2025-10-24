
// ignore_for_file: use_super_parameters, library_private_types_in_public_api, use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'movie.dart';
import 'database_helper.dart';
import 'movie_detail_screen.dart';

class SearchMovieScreen extends StatefulWidget {
  const SearchMovieScreen({Key? key}) : super(key: key);

  @override
  _SearchMovieScreenState createState() => _SearchMovieScreenState();
}

class _SearchMovieScreenState extends State<SearchMovieScreen> {

  final String _apiKey = "be1289f0bc807682e648792b983aab0c";

  final TextEditingController _searchController = TextEditingController();
  final dbHelper = DatabaseHelper.instance;

  List<Movie> _searchResults = [];
  bool _isLoading = false;
  String _message = 'Gunakan kolom di atas untuk mencari film...';

  Future<void> _searchMovies(String query) async {
    if (query.isEmpty) return;
    setState(() {
      _isLoading = true;
      _message = 'Mencari...';
    });
    final url =
        'https://api.themoviedb.org/3/search/movie?api_key=$_apiKey&query=$query&language=id-ID';
    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List results = data['results'];
        setState(() {
          _searchResults = results.map((e) => Movie.fromJson(e)).toList();
          _isLoading = false;
          _message = _searchResults.isEmpty ? 'Film tidak ditemukan.' : '';
        });
      } else {
        setState(() {
          _isLoading = false;
          _message = 'Gagal memuat data. Periksa koneksi.';
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _message = 'Terjadi error: $e';
      });
    }
  }

  void _addFavorite(Movie movie) async {
    await dbHelper.insert(movie);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${movie.title} ditambahkan ke watchlist!'),
        backgroundColor: Colors.green,
      ),
    );
  }

  void _goToDetailScreen(Movie movie) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => MovieDetailScreen(movie: movie)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Cari Film", style: GoogleFonts.kaushanScript(fontSize: 28, color: Colors.white)),
        backgroundColor: const Color(0xFF0D1B2A),
        foregroundColor: Colors.white,
      ),
      backgroundColor: const Color(0xFF4A4A4A),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: TextField(
              controller: _searchController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: 'Search Title Here',
                hintStyle: const TextStyle(color: Colors.white54),
                prefixIcon: const Icon(Icons.search, color: Colors.white54),
                filled: true,
                fillColor: const Color(0xFF1B263B),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: const BorderSide(color: Colors.transparent),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: const BorderSide(color: Colors.white),
                ),
              ),
              onSubmitted: (value) => _searchMovies(value),
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _searchResults.isEmpty
                    ? Center(child: Text(_message, style: GoogleFonts.poppins(color: Colors.white70)))
                    : ListView.builder(
                        itemCount: _searchResults.length,
                        itemBuilder: (context, index) {
                          final movie = _searchResults[index];
                          return Card(
                            color: const Color(0xFF1B263B),
                            margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                            child: ListTile(
                              onTap: () => _goToDetailScreen(movie),
                              leading: movie.posterPath.isEmpty
                                  ? const Icon(Icons.movie, size: 50, color: Colors.white)
                                  : Image.network(
                                      'https://image.tmdb.org/t/p/w200${movie.posterPath}',
                                      width: 50,
                                      fit: BoxFit.cover,
                                    ),
                              title: Text(movie.title, style: GoogleFonts.poppins(color: Colors.white)),
                              subtitle: Text(movie.overview, maxLines: 2, overflow: TextOverflow.ellipsis, style: GoogleFonts.poppins(color: Colors.white60)),
                              trailing: IconButton(
                                icon: const Icon(Icons.add_circle, color: Colors.green, size: 28),
                                tooltip: 'Tambah ke Watchlist',
                                onPressed: () => _addFavorite(movie),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}