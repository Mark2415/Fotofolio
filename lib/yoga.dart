// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'header.dart'; // Pastikan path ini benar

class YogaPage extends StatelessWidget {
  final String userName;
  final Function(int) onNavigate;
  const YogaPage({super.key, required this.userName, required this.onNavigate});
  
  @override
  Widget build(BuildContext context) {
     return Scaffold(
      backgroundColor: Colors.grey[200],
       body: Column(
        children: [
          AppHeader(
            userName: userName,
            title: 'Yoga',
            tabs: [
              HeaderTabItem(icon: Icons.home, label: 'Home', onTap: () => onNavigate(0)),
              HeaderTabItem(icon: Icons.restaurant_menu, label: 'Diet Plan', onTap: () => onNavigate(1)),
              HeaderTabItem(icon: Icons.fitness_center, label: 'Exercises', onTap: () => onNavigate(2)),
              HeaderTabItem(icon: Icons.medical_services_outlined, label: 'Medical Tips', onTap: () => onNavigate(3)),
            ],
          ),
          Expanded(
            child: SingleChildScrollView(
              child: _buildYogaTimerAndMusic(),
            ),
          ),
        ],
         ),
     );
  }

  Widget _buildYogaTimerAndMusic() {
    return Container(
      margin: const EdgeInsets.all(24.0),
      padding: const EdgeInsets.all(20.0),
      decoration: BoxDecoration(
        color: const Color(0xFFF9F0BE),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.2), spreadRadius: 2, blurRadius: 8)],
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            decoration: BoxDecoration(color: Colors.grey[300], borderRadius: BorderRadius.circular(20)),
            child: const Text('STAND BY', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black54, letterSpacing: 2)),
          ),
          const SizedBox(height: 20),
          
          // --- PERBAIKAN: Mengganti Row dengan Wrap ---
          Wrap(
            alignment: WrapAlignment.center, // Pusatkan item di setiap baris
            crossAxisAlignment: WrapCrossAlignment.center, // Sejajarkan item secara vertikal
            spacing: 8.0, // Jarak horizontal antar item
            runSpacing: 4.0, // Jarak vertikal jika ada baris baru
            children: [
              _buildTimeAdjustButton(label: '-1S'),
              _buildTimeAdjustButton(label: '-1M'),
              _buildTimeAdjustButton(label: '-1H'),
              _buildTimerDisplay(), // Timer akan berada di antara tombol
              _buildTimeAdjustButton(label: '+1H'),
              _buildTimeAdjustButton(label: '+1M'),
              _buildTimeAdjustButton(label: '+1S'),
            ],
          ),
          const SizedBox(height: 10),

          Container(
            padding: const EdgeInsets.all(10),
            decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle),
            child: const Icon(Icons.refresh, color: Color(0xFF8A2BE2)),
          ),
          const SizedBox(height: 15),
          Container(
            width: 100, height: 35,
            decoration: BoxDecoration(color: const Color(0xFF8A2BE2), borderRadius: BorderRadius.circular(20)),
            child: const Center(child: Text('Stop', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold))),
          ),
          const SizedBox(height: 30),
          const Text('Waiting for music info', style: TextStyle(color: Colors.black54, fontSize: 14)),
          const SizedBox(height: 10),
          _buildMusicPlayerControls(),
        ],
      ),
    );
  }

  // Ukuran dikembalikan agar lebih mudah dibaca, karena Wrap akan menanganinya
  Widget _buildTimeAdjustButton({required String label}) {
    return Container(
      width: 40, height: 40,
      decoration: BoxDecoration(
        color: Colors.white, shape: BoxShape.circle,
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), spreadRadius: 1, blurRadius: 3)],
      ),
      child: Center(child: Text(label, style: const TextStyle(fontSize: 14, color: Colors.black54))),
    );
  }

  // Ukuran dikembalikan agar lebih jelas
  Widget _buildTimerDisplay() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8), // Beri margin agar ada jarak
      width: 110, height: 45,
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(30),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), spreadRadius: 1, blurRadius: 3)],
      ),
      child: const Center(child: Text('00:00:00', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF8A2BE2)))),
    );
  }

  Widget _buildMusicPlayerControls() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), spreadRadius: 1, blurRadius: 3)],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Icon(Icons.queue_music, color: Colors.grey[700], size: 28),
          Icon(Icons.skip_previous, color: Colors.grey[700], size: 36),
          Icon(Icons.play_arrow, color: Colors.grey[700], size: 36),
          Icon(Icons.skip_next, color: Colors.grey[700], size: 36),
          Icon(Icons.volume_up, color: Colors.grey[700], size: 28),
        ],
      ),
    );
  }
}