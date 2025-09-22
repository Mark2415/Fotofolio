// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';

class AppHeader extends StatelessWidget {
  final String userName;
  final String title;
  final List<Widget> tabs;
  
  const AppHeader({
    super.key,
    required this.userName,
    required this.title,
    required this.tabs,
  });

  String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour >= 0 && hour < 11) return 'Good Morning';
    if (hour >= 11 && hour < 15) return 'Good Afternoon';
    return 'Good Evening';
  }

  @override
  Widget build(BuildContext context) {
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
                Text(_getGreeting(), style: const TextStyle(color: Colors.white, fontSize: 22)),
                Text(userName, style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
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
          Center(child: Text(title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold))),
          const SizedBox(height: 15),
          Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: tabs),
        ],
      ),
    );
  }
}

class HeaderTabItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const HeaderTabItem({super.key, required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
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
      ),
    );
  }
}