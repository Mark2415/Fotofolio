// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'header.dart';

class HomePage extends StatelessWidget {
  final String userName;
  final Function(int) onNavigate;
  const HomePage({super.key, required this.userName, required this.onNavigate});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: Column(
        children: [
          AppHeader(
            userName: userName,
            title: "Home",
            tabs: [
              HeaderTabItem(icon: Icons.restaurant_menu, label: 'Diet Plan', onTap: () => onNavigate(1)),
              HeaderTabItem(icon: Icons.fitness_center, label: 'Exercises', onTap: () => onNavigate(2)),
              HeaderTabItem(icon: Icons.medical_services_outlined, label: 'Medical Tips', onTap: () => onNavigate(3)),
              HeaderTabItem(icon: Icons.self_improvement, label: 'Yoga', onTap: () => onNavigate(4)),
            ],
          ),
          Expanded(
            child: SingleChildScrollView(
              child: _buildMainMenu(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainMenu() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: GridView.count(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        children: [
          _buildMenuItem(icon: Icons.restaurant_menu, label: 'Diet Plan', onTap: () => onNavigate(1)),
          _buildMenuItem(icon: Icons.fitness_center, label: 'Exercises', onTap: () => onNavigate(2)),
          _buildMenuItem(icon: Icons.medical_services_outlined, label: 'Medical Tips', onTap: () => onNavigate(3)),
          _buildMenuItem(icon: Icons.self_improvement, label: 'Yoga', onTap: () => onNavigate(4)),
        ],
      ),
    );
  }

  Widget _buildMenuItem({required IconData icon, required String label, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(15),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.1),
              spreadRadius: 2,
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 50, color: const Color(0xFF8A2BE2)),
            const SizedBox(height: 10),
            Text(label, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.black54)),
          ],
        ),
      ),
    );
  }
}