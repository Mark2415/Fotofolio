import 'package:flutter/material.dart';
import 'signup.dart'; // Ganti 'proyek_utama' dengan nama folder proyek Anda
import 'home.dart';
import 'dietplan.dart';
import 'exercises.dart';
import 'medical_tips.dart';
import 'yoga.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Health App UI',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        fontFamily: 'Roboto',
      ),
      home: const RegisterPage(), // Aplikasi dimulai dari halaman registrasi
      debugShowCheckedModeBanner: false,
    );
  }
}

// Kerangka Utama Aplikasi setelah Login
class MainPage extends StatefulWidget {
  final String userName;
  const MainPage({super.key, required this.userName});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  late final List<Widget> s;

  @override
  void initState() {
    super.initState();
    s = [
      HomePage(userName: widget.userName, onNavigate: _navigateTo),
      DietPlanPage(userName: widget.userName, onNavigate: _navigateTo),
      ExercisesPage(userName: widget.userName, onNavigate: _navigateTo),
      MedicalTipsPage(userName: widget.userName, onNavigate: _navigateTo),
      YogaPage(userName: widget.userName, onNavigate: _navigateTo),
    ];
  }

  void _navigateTo(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _onItemTapped(int index) {
    if (index == 0) {
      _navigateTo(0); // Tombol "Today" kembali ke HomePage
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Halaman belum tersedia')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: s,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex == 0 ? 0 : 1,
        onTap: _onItemTapped,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        selectedItemColor: const Color(0xFF8A2BE2),
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.today_outlined), activeIcon: Icon(Icons.today), label: 'Today'),
          BottomNavigationBarItem(icon: Icon(Icons.settings_outlined), activeIcon: Icon(Icons.settings), label: 'Settings'),
          BottomNavigationBarItem(icon: Icon(Icons.event_outlined), activeIcon: Icon(Icons.event), label: 'Tomorrow'),
        ],
      ),
    );
  }
}