import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'movie.dart';

class MovieDetailScreen extends StatelessWidget {
  final Movie movie;
  // ignore: use_super_parameters
  const MovieDetailScreen({Key? key, required this.movie}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final posterUrl = 'https://image.tmdb.org/t/p/w500${movie.posterPath}';
    return Scaffold(
      appBar: AppBar(
        title: Text("Movie Detail",
            style:
                GoogleFonts.kaushanScript(fontSize: 28, color: Colors.white)),
        backgroundColor: const Color(0xFF0D1B2A),
        foregroundColor: Colors.white,
      ),
      backgroundColor: const Color(0xFF4A4A4A),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image.network(
              posterUrl,
              width: double.infinity,
              height: 500,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) => Container(
                height: 500,
                color: Colors.grey.shade800,
                child: const Icon(Icons.movie_creation_outlined,
                    color: Colors.white, size: 100),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    movie.title,
                    style: GoogleFonts.poppins(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "Overview",
                    style: GoogleFonts.poppins(
                      fontSize: 22,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    movie.overview.isEmpty
                        ? "No overview available."
                        : movie.overview,
                    style: GoogleFonts.poppins(
                      fontSize: 16,
                      height: 1.6,
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
