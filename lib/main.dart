import 'package:flutter/material.dart';
// 1. Import library date formatting
import 'package:intl/date_symbol_data_local.dart';
import 'homepage.dart';
import 'register_page.dart'; // used by the Sign up flow

// 2. Ubah main menjadi async
void main() async {
  // Baris ini diperlukan untuk memastikan Flutter siap sebelum menjalankan kode async
  WidgetsFlutterBinding.ensureInitialized();
  // 3. Inisialisasi locale 'id_ID' untuk format tanggal Bahasa Indonesia
  await initializeDateFormatting('id_ID', null);
  runApp(const MyApp());
}

/// Very small in-memory simulation of a user store.
///
/// This is for demo/testing only — don't use for production. Registered
/// credentials are stored in static fields and compared during login.
class UserDatabase {
  static String? registeredEmail;
  static String? registeredPassword;
}

/// Root widget for the app. Sets theme and the initial route to `LoginPage`.
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'E-Commerce Login',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFEE4D2D)),
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}

/// LoginPage provides a simple form where users can enter an email and
/// password and compare them against `UserDatabase` to simulate login.
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  /// Attempt to login using the values stored in `UserDatabase`.
  ///
  /// Shows SnackBar messages for missing account or wrong credentials.
  void _login() {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (UserDatabase.registeredEmail == null ||
        UserDatabase.registeredPassword == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Belum ada akun. Silakan daftar dulu.')),
      );
      return;
    }

    if (email == UserDatabase.registeredEmail &&
        password == UserDatabase.registeredPassword) {
      // Successful login: replace the route with `HomePage`.
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const HomePage()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Email atau password salah!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.shopping_cart_outlined,
                    color: Color(0xFFEE4D2D), size: 80),
                const SizedBox(height: 20),
                const Text(
                  "Welcome to E-Commerce",
                  style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.black),
                ),
                const SizedBox(height: 10),
                const Text(
                  "Sign in to continue shopping",
                  style: TextStyle(color: Colors.grey),
                ),
                const SizedBox(height: 40),
                // Email input
                TextField(
                  controller: _emailController,
                  decoration: InputDecoration(
                    labelText: 'Email',
                    prefixIcon: const Icon(Icons.email_outlined),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                // Password input
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Password',
                    prefixIcon: const Icon(Icons.lock_outline),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                const SizedBox(height: 30),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _login,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFEE4D2D),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      "Login",
                      style: TextStyle(color: Colors.white, fontSize: 18),
                    ),
                  ),
                ),
                const SizedBox(height: 15),
                // Link to RegisterPage
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text("Don’t have an account? "),
                    TextButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (_) => const RegisterPage()),
                        );
                      },
                      child: const Text(
                        "Sign up",
                        style: TextStyle(color: Color(0xFFEE4D2D)),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// A small utility page used during testing to quickly navigate into the
// `HomePage`. Not used in the normal login flow.
class MainMenuPage extends StatelessWidget {
  const MainMenuPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Main Menu")),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const HomePage()),
            );
          },
          child: const Text("Masuk ke Homepage"),
        ),
      ),
    );
  }
}