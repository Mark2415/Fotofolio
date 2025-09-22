// ignore_for_file: deprecated_member_use

import 'dart:async';
import 'package:flutter/material.dart';
import 'header.dart';

class MedicalTipsPage extends StatefulWidget {
  final String userName;
  final Function(int) onNavigate;
  const MedicalTipsPage({super.key, required this.userName, required this.onNavigate});
  
  @override
  State<MedicalTipsPage> createState() => _MedicalTipsPageState();
}

class _MedicalTipsPageState extends State<MedicalTipsPage> {
  late final PageController _pageController;
  Timer? _timer;
  int _currentPage = 0;

  final List<String> medicalFacts = [
    "Hydration is key. Drinking enough water can boost your metabolism.",
    "Fiber-rich foods like oats and beans keep you feeling full longer.",
    "Protein is essential for muscle repair and growth after exercise.",
    "Don't skip breakfast! It kickstarts your metabolism for the day.",
    "Healthy fats from avocados and nuts are crucial for brain health.",
  ];

  @override
  void initState() {
    super.initState();
    _pageController = PageController(initialPage: 0);
    _startTimer();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _pageController.dispose();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 10), (timer) { 
      if (!mounted) return;
      _currentPage = (_currentPage + 1) % medicalFacts.length;
      if (_pageController.hasClients) {
        _pageController.animateToPage(_currentPage, duration: const Duration(milliseconds: 800), curve: Curves.easeInOut);
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      body: Column(
        children: [
          AppHeader(
            userName: widget.userName,
            title: 'Medical Tips',
            tabs: [
              HeaderTabItem(icon: Icons.home, label: 'Home', onTap: () => widget.onNavigate(0)),
              HeaderTabItem(icon: Icons.restaurant_menu, label: 'Diet Plan', onTap: () => widget.onNavigate(1)),
              HeaderTabItem(icon: Icons.fitness_center, label: 'Exercises', onTap: () => widget.onNavigate(2)),
              HeaderTabItem(icon: Icons.self_improvement, label: 'Yoga', onTap: () => widget.onNavigate(4)),
            ],
          ),
          Expanded(
            child: Center(
              child: _buildTipsCarousel(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTipsCarousel() {
    return Container(
      height: 200,
      margin: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.2), spreadRadius: 2, blurRadius: 8)],
      ),
      child: PageView.builder(
        controller: _pageController,
        itemCount: medicalFacts.length,
        itemBuilder: (context, index) {
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
            child: Row(
              children: [
                const CircleAvatar(radius: 25, backgroundColor: Color(0xFFD4B5F7), child: Icon(Icons.medical_services_outlined, color: Colors.white)),
                const SizedBox(width: 16),
                Expanded(child: Text(medicalFacts[index], style: const TextStyle(fontSize: 16, color: Colors.black54, height: 1.5))),
              ],
            ),
          );
        },
      ),
    );
  }
}