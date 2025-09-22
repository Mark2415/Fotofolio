// ignore_for_file: file_names, deprecated_member_use

import 'package:flutter/material.dart';

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
        primarySwatch: Colors.blue,
        fontFamily: 'Roboto',
      ),
      home: const MedicalTipsPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MedicalTipsPage extends StatefulWidget {
  const MedicalTipsPage({super.key});

  @override
  State<MedicalTipsPage> createState() => _MedicalTipsPageState();
}

class _MedicalTipsPageState extends State<MedicalTipsPage> {
  String currentUserName = "Mailbin 📪";
  int _bottomNavIndex = 0;
  
     // Fungsi untuk mendapatkan salam
  String _getGreeting() {
    final hour = DateTime.now().hour;
    
    // 00:00 - 10:59 -> Pagi
    if (hour >= 0 && hour < 11) {
      return 'Good Morning';
    } 
    // 11:00 - 14:59 -> Siang
    else if (hour >= 11 && hour < 15) {
      return 'Good Afternoon';
    } 
    // 15:00 - 23:59 -> Sore/Malam
    else if (hour >= 15 && hour < 24) {
      return 'good evening';
    } 
    // Default -> Have a good day
    else {
      return 'Have a good day';
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHeaderAndTabs(),
            _buildStaticMedicalTip(), // Menggunakan widget statis, bukan carousel
          ],
        ),
      ),
      bottomNavigationBar: _buildBottomNavigationBar(),
    );
  }

  Widget _buildHeaderAndTabs() {
    return Container(
      padding: const EdgeInsets.only(top: 60, bottom: 20),
      decoration: const BoxDecoration(
        color: Color(0xFFF9C8A9),
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(30),
          bottomRight: Radius.circular(30),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _getGreeting(),
                  style: const TextStyle(color: Colors.white, fontSize: 22),
                ),
                Text(
                  currentUserName,
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 32,
                      fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.8),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: const TextField(
                    decoration: InputDecoration(
                      icon: Icon(Icons.search, color: Colors.grey),
                      hintText: 'Search',
                      border: InputBorder.none,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          const Center(
            child: Text(
              'Medical Tips',
              style: TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(height: 15),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildHeaderTabItem(icon: Icons.home, label: 'Home'),
              _buildHeaderTabItem(icon: Icons.restaurant_menu, label: 'Diet Plan'),
              _buildHeaderTabItem(icon: Icons.fitness_center, label: 'Exercises'),
              _buildHeaderTabItem(icon: Icons.self_improvement, label: 'Yoga'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildHeaderTabItem({required IconData icon, required String label}) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.3),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(icon, color: Colors.white, size: 24),
        ),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.white, fontSize: 12))
      ],
    );
  }

  // WIDGET BARU YANG LEBIH SEDERHANA (TANPA CAROUSEL)
  Widget _buildStaticMedicalTip() {
    return Container(
      margin: const EdgeInsets.all(24.0),
      padding: const EdgeInsets.symmetric(vertical: 20.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            spreadRadius: 2,
            blurRadius: 8,
          ),
        ],
      ),
      child: Column(
        children: [
          // Konten statis di dalam kartu
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 30.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                CircleAvatar(
                  radius: 25,
                  backgroundColor: const Color(0xFFD4B5F7),
                  child: Icon(Icons.medical_services_outlined, color: Colors.white, size: 30),
                ),
                const SizedBox(width: 16),
                const Expanded(
                  child: Text(
                    "Awesome Medical Tips (just image this is carosel)",
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.black54,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          // Tombol kontrol yang hanya sebagai hiasan
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                icon: Icon(Icons.skip_previous, color: Colors.grey[700]),
                onPressed: () {}, // Tidak ada aksi
              ),
              const SizedBox(width: 20),
              IconButton(
                icon: Icon(Icons.pause, color: Colors.grey[700]),
                onPressed: () {}, // Tidak ada aksi
              ),
              const SizedBox(width: 20),
              IconButton(
                icon: Icon(Icons.skip_next, color: Colors.grey[700]),
                onPressed: () {}, // Tidak ada aksi
              ),
            ],
          )
        ],
      ),
    );
  }

  Widget _buildBottomNavigationBar() {
    return BottomNavigationBar(
      currentIndex: _bottomNavIndex,
      onTap: (index) {
        setState(() {
          _bottomNavIndex = index;
        });
      },
      type: BottomNavigationBarType.fixed,
      backgroundColor: Colors.white,
      selectedItemColor: const Color(0xFF8A2BE2),
      unselectedItemColor: Colors.grey,
      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.today_outlined),
          activeIcon: Icon(Icons.today),
          label: 'Today',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.settings_outlined),
          activeIcon: Icon(Icons.settings),
          label: 'Settings',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.event_outlined),
          activeIcon: Icon(Icons.event),
          label: 'Tomorrow',
        ),
      ],
    );
  }
}