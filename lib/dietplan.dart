// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'header.dart';

class DietPlanPage extends StatelessWidget {
  final String userName;
  final Function(int) onNavigate;
  const DietPlanPage({super.key, required this.userName, required this.onNavigate});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      body: Column(
        children: [
          AppHeader(
            userName: userName,
            title: 'Diet Plan',
            tabs: [
              HeaderTabItem(icon: Icons.home, label: 'Home', onTap: () => onNavigate(0)),
              HeaderTabItem(icon: Icons.fitness_center, label: 'Exercises', onTap: () => onNavigate(2)),
              HeaderTabItem(icon: Icons.medical_services_outlined, label: 'Medical Tips', onTap: () => onNavigate(3)),
              HeaderTabItem(icon: Icons.self_improvement, label: 'Yoga', onTap: () => onNavigate(4)),
            ],
          ),
          Expanded(child: Center(child: _buildDietList())),
        ],
      ),
    );
  }

  Widget _buildDietList() {
    return SingleChildScrollView(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _buildDietListItem(icon: Icons.free_breakfast, label: 'Breakfast'),
                  const SizedBox(height: 16),
                  _buildDietListItem(icon: Icons.lunch_dining, label: 'Lunch'),
                  const SizedBox(height: 16),
                  _buildDietListItem(icon: Icons.dinner_dining, label: 'Dinner'),
                ],
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const SizedBox(height: 30),
                  _buildDietListItem(icon: Icons.apple, label: 'Fruit'),
                  const SizedBox(height: 16),
                  _buildDietListItem(icon: Icons.bakery_dining, label: 'Snack'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDietListItem({required IconData icon, required String label}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(30),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.2), spreadRadius: 1, blurRadius: 5)],
      ),
      child: Row(
        children: [
          CircleAvatar(backgroundColor: const Color(0xFFD4B5F7), child: Icon(icon, color: Colors.white)),
          const SizedBox(width: 12),
          Text(label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.black54)),
        ],
      ),
    );
  }
}