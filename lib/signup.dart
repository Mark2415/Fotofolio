// ignore_for_file: deprecated_member_use, sort_child_properties_last, unused_field

import 'package:flutter/material.dart';
import 'main.dart'; // Untuk bisa navigasi ke MainPage

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<StatefulWidget> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _tgllhrtext = TextEditingController();
  
  bool _obscure = true;
  bool _agree = false;
  String? _gender;
  String? _kotaLahir;
  
  final List<String> _kota = const ['Jakarta', 'Bandung', 'Surabaya', 'Denpasar', 'Makasar', 'Jomokerto','Ngawilly'];
  
  @override
  void dispose() {
    _name.dispose();
    _email.dispose();
    _password.dispose();
    _tgllhrtext.dispose();
    super.dispose();
  }

  String? _required(String? v) => (v == null || v.isEmpty) ? 'Wajib diisi' : null;

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime(now.year - 20),
      firstDate: DateTime(now.year - 100),
      lastDate: now,
    );
    if (pickedDate != null) {
      setState(() {
        _tgllhrtext.text = '${pickedDate.day.toString().padLeft(2, '0')}-${pickedDate.month.toString().padLeft(2, '0')}-${pickedDate.year}';
      });
    }
  }

  void _submit() {
    if (!_agree) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Anda harus menyetujui syarat dan ketentuan')));
      return;
    }
    if (_formKey.currentState!.validate()) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => MainPage(userName: _name.text)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      _buildHeader(),
                      _buildForm(),
                    ],
                  ),
                ),
              ),
              _buildSubmitButton(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 24).copyWith(bottom: 24),
      decoration: const BoxDecoration(color: Color(0xFFF9C8A9)),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Good Morning', style: TextStyle(fontSize: 28, color: Colors.white)),
          Text('Sign-up', style: TextStyle(fontSize: 40, color: Colors.white, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildForm() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextFormField(controller: _name, decoration: const InputDecoration(labelText: "Nama"), validator: _required, textInputAction: TextInputAction.next),
          const SizedBox(height: 12),
          TextFormField(controller: _email, decoration: const InputDecoration(labelText: "Email"), validator: _required, textInputAction: TextInputAction.next, keyboardType: TextInputType.emailAddress),
          const SizedBox(height: 12),
          TextFormField(
            controller: _password,
            validator: _required,
            obscureText: _obscure,
            decoration: InputDecoration(
              labelText: "Password",
              suffixIcon: IconButton(
                icon: Icon(_obscure ? Icons.visibility : Icons.visibility_off),
                onPressed: () => setState(() => _obscure = !_obscure),
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Text("Jenis Kelamin", style: TextStyle(fontSize: 16)),
          Row(
            children: [
              Expanded(child: RadioListTile<String>(title: const Text("Laki-laki"), value: "L", groupValue: _gender, onChanged: (v) => setState(() => _gender = v), contentPadding: EdgeInsets.zero)),
              Expanded(child: RadioListTile<String>(title: const Text("Perempuan"), value: "P", groupValue: _gender, onChanged: (v) => setState(() => _gender = v), contentPadding: EdgeInsets.zero)),
            ],
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            decoration: const InputDecoration(labelText: "Kota Lahir"),
            items: _kota.map((e) => DropdownMenuItem<String>(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => _kotaLahir = v),
            validator: _required,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _tgllhrtext,
            readOnly: true,
            onTap: _pickDate,
            validator: _required,
            decoration: const InputDecoration(labelText: "Tanggal Lahir", suffixIcon: Icon(Icons.calendar_today)),
          ),
          const SizedBox(height: 12),
          CheckboxListTile(
            value: _agree,
            onChanged: (v) => setState(() => _agree = v ?? false),
            title: const Text("Saya menyetujui syarat dan ketentuan"),
            controlAffinity: ListTileControlAffinity.leading,
            contentPadding: EdgeInsets.zero,
          ),
        ],
      ),
    );
  }

  Widget _buildSubmitButton() {
    return Container(
      color: Colors.grey[800],
      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      child: SizedBox(
        width: double.infinity,
        child: ElevatedButton.icon(
          onPressed: _submit,
          icon: const Icon(Icons.check),
          label: const Text("Daftar"),
          style: ElevatedButton.styleFrom(
            foregroundColor: Colors.black,
            backgroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: const StadiumBorder(),
          ),
        ),
      ),
    );
  }
}