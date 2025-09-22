// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'header.dart';

class ExercisesPage extends StatelessWidget {
  final String userName;
  final Function(int) onNavigate;
  const ExercisesPage({super.key, required this.userName, required this.onNavigate});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      body: Column(
        children: [
          AppHeader(
            userName: userName,
            title: 'Exercises',
            tabs: [
              HeaderTabItem(icon: Icons.home, label: 'Home', onTap: () => onNavigate(0)),
              HeaderTabItem(icon: Icons.restaurant_menu, label: 'Diet Plan', onTap: () => onNavigate(1)),
              HeaderTabItem(icon: Icons.medical_services_outlined, label: 'Medical Tips', onTap: () => onNavigate(3)),
              HeaderTabItem(icon: Icons.self_improvement, label: 'Yoga', onTap: () => onNavigate(4)),
            ],
          ),
          Expanded(
            child: SingleChildScrollView(
              child: _buildExerciseCategories(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildExerciseCategories() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        children: [
          _buildExerciseButton(icon: Icons.accessibility_new, label: 'Upper Body', isFullWidth: true),
          const SizedBox(height: 16),
          _buildExerciseButton(icon: Icons.accessibility_new, label: 'Lower Body', isFullWidth: true),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(child: _buildExerciseButton(icon: Icons.directions_run, label: 'Cardio')),
              const SizedBox(width: 16),
              Expanded(child: _buildExerciseButton(icon: Icons.directions_bike, label: 'Core')),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildExerciseButton({required IconData icon, required String label, bool isFullWidth = false}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(isFullWidth ? 30 : 20),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.2), spreadRadius: 1, blurRadius: 5)],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircleAvatar(backgroundColor: const Color(0xFFD4B5F7), radius: 25, child: Icon(icon, color: Colors.white, size: 30)),
          const SizedBox(width: 16),
          Text(label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.black54)),
        ],
      ),
    );
  }
}