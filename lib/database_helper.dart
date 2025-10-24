import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'dart:async';
import 'movie.dart';

class DatabaseHelper {
  static const _databaseName = "UserWatchList.db";
  static const _databaseVersion = 1;

  static const table = 'movies';

  static const columnId = 'id';
  static const columnTitle = 'title';
  static const columnOverview = 'overview';
  static const columnPosterPath = 'posterPath';
  static const columnIsWatched = 'isWatched';
  static const columnRating = 'rating';

  DatabaseHelper._privateConstructor();
  static final DatabaseHelper instance = DatabaseHelper._privateConstructor();

  static Database? _database;
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  _initDatabase() async {
    String path = join(await getDatabasesPath(), _databaseName);
    return await openDatabase(path,
        version: _databaseVersion, onCreate: _onCreate);
  }

  Future _onCreate(Database db, int version) async {
    await db.execute('''
          CREATE TABLE $table (
            $columnId INTEGER PRIMARY KEY, 
            $columnTitle TEXT NOT NULL,
            $columnOverview TEXT NOT NULL,
            $columnPosterPath TEXT NOT NULL,
            $columnIsWatched INTEGER NOT NULL DEFAULT 0,
            $columnRating INTEGER NOT NULL DEFAULT 0
          )
          ''');
  }

  // Menambahkan film baru (dipakai di layar pencarian)
  Future<int> insert(Movie movie) async {
    Database db = await instance.database;
    return await db.insert(table, movie.toMap(),
        conflictAlgorithm: ConflictAlgorithm.ignore); // Abaikan jika id film sudah ada
  }

  // Memperbarui film yang ada (dipakai di layar favorit)
  Future<int> update(Movie movie) async {
    Database db = await instance.database;
    return await db.update(table, movie.toMap(),
        where: '$columnId = ?', whereArgs: [movie.id]);
  }

  // Mengambil semua film favorit
  Future<List<Movie>> getAllFavoriteMovies() async {
    Database db = await instance.database;
    final List<Map<String, dynamic>> maps = await db.query(table, orderBy: '$columnTitle ASC');

    return List.generate(maps.length, (i) {
      return Movie.fromMap(maps[i]);
    });
  }

  // Menghapus film
  Future<int> delete(int id) async {
    Database db = await instance.database;
    return await db.delete(table, where: '$columnId = ?', whereArgs: [id]);
  }
}