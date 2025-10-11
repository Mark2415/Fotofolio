import 'package:flutter/material.dart';
import 'main.dart';

/// Simple profile screen showing an avatar, the user's basic info and a few
/// action tiles. The logout tile navigates back to the `MainMenuPage`.
class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Profil Saya"),
        backgroundColor: Colors.redAccent,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // User avatar (replace `images/profile.png` with real image)
            const CircleAvatar(
              radius: 50,
              backgroundImage: AssetImage("images/profile.png"),
            ),
            const SizedBox(height: 20),
            // Placeholder name and email. In a real app these would be loaded
            // from the authenticated user's profile data.
            const Text(
              "Nama User",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const Text(
              "user@email.com",
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 30),

            // Action tiles for account settings and order history. Currently
            // they have empty handlers and can be wired to real pages.
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text("Pengaturan Akun"),
              onTap: () {},
            ),
            ListTile(
              leading: const Icon(Icons.history),
              title: const Text("Riwayat Pesanan"),
              onTap: () {},
            ),

            // Logout action. Here it navigates to `MainMenuPage` — in a real
            // application you would also clear authentication state.
            ListTile(
              leading: const Icon(Icons.logout, color: Colors.redAccent),
              title: const Text("Keluar"),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const MainMenuPage()),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
