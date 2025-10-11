// ignore_for_file: unused_field, unused_element, unused_local_variable, deprecated_member_use, sort_child_properties_last

import 'package:flutter/material.dart';
import 'main.dart'; // used to navigate back to LoginPage after registration

/// Lightweight model that represents registration form data.
/// This keeps the collected fields in one place and helps document what the
/// registration flow collects. The app currently doesn't persist this object
/// anywhere; it's provided for clarity.
class RegistrationData {
  final String nama;
  final String email;
  final String password;
  final String gender;
  final DateTime? birthdate;
  final bool agree;

  const RegistrationData({
    required this.nama,
    required this.email,
    required this.password,
    required this.gender,
    required this.birthdate,
    required this.agree,
  });
}

/// Registration screen where users provide name, email, password, gender,
/// birthdate and must accept terms. On successful submit the demo stores the
/// credentials in `UserDatabase` (see `main.dart`) and navigates back to the
/// login screen.
class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<StatefulWidget> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();

  // UI state flags
  bool _obscure = true; // show/hide password
  bool _agree = false; // terms acceptance
  String? _gender; // selected gender value ("L" or "P")
  DateTime? _tanggalLahir; // selected birthdate

  // Controllers for text inputs
  final _nama = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _tgllhrtext = TextEditingController(); // formatted date text

  // Simple validator used for required fields
  String? _required(String? v) {
    if (v == null || v.isEmpty) {
      return 'Wajib diisi';
    }
    return null;
  }

  /// Opens the date picker and updates `_tanggalLahir` and the visible
  /// text controller `_tgllhrtext` with a nicely formatted value.
  Future<void> _pickDate() async {
    final now = DateTime.now();
    final firstDate = DateTime(now.year - 100);
    final lastDate = DateTime(now.year + 1);
    final pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime(now.year - 20, now.month, now.day),
      firstDate: firstDate,
      lastDate: lastDate,
    );
    if (pickedDate != null) {
      setState(() {
        _tanggalLahir = pickedDate;
        _tgllhrtext.text =
            '${pickedDate.day.toString().padLeft(2, '0')}-${pickedDate.month.toString().padLeft(2, '0')}-${pickedDate.year}';
      });
    }
  }

  /// Handles the registration submit logic.
  ///
  /// - Ensures terms are accepted.
  /// - Validates the form fields.
  /// - Stores the registered email/password in the demo `UserDatabase`.
  /// - Shows a SnackBar and navigates back to the login screen.
  void _submit() {
    if (!_agree) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Centang persetujuan terlebih dahulu!')),
      );
      return;
    }

    if (!_formKey.currentState!.validate()) return;

    // Store credentials in the temporary in-memory user store.
    UserDatabase.registeredEmail = _email.text.trim();
    UserDatabase.registeredPassword = _password.text.trim();

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Pendaftaran berhasil! Silakan login.')),
    );

    // Replace the route with the login screen so the user can sign in.
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Registrasi")),
      body: SafeArea(
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Name field
                TextFormField(
                  controller: _nama,
                  decoration: const InputDecoration(labelText: "Nama"),
                  validator: _required,
                  textInputAction: TextInputAction.next,
                ),
                const SizedBox(height: 12),

                // Email field
                TextFormField(
                  controller: _email,
                  decoration: const InputDecoration(labelText: "Email"),
                  validator: _required,
                  textInputAction: TextInputAction.next,
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 12),

                // Password with visibility toggle
                TextFormField(
                  controller: _password,
                  decoration: InputDecoration(
                    labelText: "Password",
                    suffixIcon: IconButton(
                      icon: Icon(_obscure
                          ? Icons.visibility
                          : Icons.visibility_off),
                      onPressed: () => setState(() => _obscure = !_obscure),
                      tooltip: _obscure ? 'Tampilkan' : 'Sembunyikan',
                    ),
                  ),
                  obscureText: _obscure,
                  validator: _required,
                  textInputAction: TextInputAction.next,
                  keyboardType: TextInputType.visiblePassword,
                ),
                const SizedBox(height: 12),

                // Gender radio buttons
                const Text("Jenis Kelamin",
                    style: TextStyle(fontWeight: FontWeight.w600)),
                Row(
                  children: [
                    Expanded(
                      child: RadioListTile<String>(
                        title: const Text("Laki-laki"),
                        value: "L",
                        groupValue: _gender,
                        onChanged: (V) => setState(() => _gender = V),
                        contentPadding: EdgeInsets.zero,
                      ),
                    ),
                    Expanded(
                      child: RadioListTile<String>(
                        title: const Text("Perempuan"),
                        value: "P",
                        groupValue: _gender,
                        onChanged: (V) => setState(() => _gender = V),
                        contentPadding: EdgeInsets.zero,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Birthdate picker (read-only text field)
                TextFormField(
                  controller: _tgllhrtext,
                  readOnly: true,
                  decoration: InputDecoration(
                    labelText: "Tanggal Lahir",
                    suffixIcon: IconButton(
                      onPressed: _pickDate,
                      icon: const Icon(Icons.date_range),
                      tooltip: 'Pilih Tanggal',
                    ),
                  ),
                  onTap: _pickDate,
                ),
                const SizedBox(height: 12),

                // Terms agreement checkbox
                CheckboxListTile(
                  value: _agree,
                  onChanged: (v) => setState(() => _agree = v ?? false),
                  title: const Text("Saya menyetujui syarat dan ketentuan"),
                  controlAffinity: ListTileControlAffinity.leading,
                ),
                const SizedBox(height: 12),

                // Submit button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _submit,
                    icon: const Icon(Icons.check),
                    label: const Text("Daftar"),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
