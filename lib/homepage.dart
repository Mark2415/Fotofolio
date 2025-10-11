// homepage.dart

// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'package:week_8_uts/profile_page.dart';
import 'package:week_8_uts/wishlist_page.dart';
import 'package:week_8_uts/wishlist_data.dart';
import 'package:week_8_uts/cart_page.dart'; // Import halaman keranjang baru
import 'package:week_8_uts/cart_data.dart'; // Import data keranjang

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _searchController = TextEditingController();
  String _searchQuery = "";

  // Data produk tetap sama
  final List<Map<String, dynamic>> _products = [
     {
      'nama': 'Ecohome Cubic Air fryer',
      'brand': 'Ecohome',
      'harga': 380000,
      'gambar': 'assets/images/Ecohome_Cubic_Air_fryer_Oven.jpg',
    },
    {
      'nama': 'Air Jordan Retro High',
      'brand': 'NIKE',
      'harga': 450000,
      'gambar': 'assets/images/Air_Jordan_Retro_High.jpg',
    },
    {
      'nama': 'AC Inverter',
      'brand': 'Sharp',
      'harga': 500000,
      'gambar': 'assets/images/AC_inverter.jpg',
    },
    {
      'nama': 'Slow juicer Ninja',
      'brand': 'Ninja',
      'harga': 360000,
      'gambar': 'assets/images/Slow_juicer_ninja.jpg',
    },
  ];

  List<Map<String, dynamic>> get _filteredProducts {
    if (_searchQuery.isEmpty) return _products;
    return _products
        .where((item) => item['nama'].toLowerCase().contains(_searchQuery.toLowerCase()))
        .toList();
  }

  void _addToWishlist(Map<String, dynamic> produk) {
    // Cek berdasarkan nama produk agar tidak duplikat
    if (WishlistData.wishlistItems.any((item) => item['nama'] == produk['nama'])) {
       ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text("${produk['nama']} sudah ada di wishlist!"),
        backgroundColor: Colors.orangeAccent,
        duration: const Duration(seconds: 1),
      ));
    } else {
       WishlistData.wishlistItems.add(produk);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text("${produk['nama']} ditambahkan ke wishlist!"),
        backgroundColor: Colors.green,
        duration: const Duration(seconds: 1),
      ));
    }
  }

  // Fungsi baru untuk menambahkan item ke keranjang
  void _addToCart(Map<String, dynamic> produk) {
    setState(() {
      CartData.addToCart(produk);
    });
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text("${produk['nama']} ditambahkan ke keranjang!"),
      backgroundColor: Colors.blue,
      duration: const Duration(seconds: 1),
    ));
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        automaticallyImplyLeading: false, // Menghilangkan tombol back
        backgroundColor: const Color(0xFFEE4D2D),
        title: Container(
          height: 40,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
          ),
          child: TextField(
            controller: _searchController,
            onChanged: (value) {
              setState(() => _searchQuery = value);
            },
            decoration: const InputDecoration(
              hintText: 'Search',
              prefixIcon: Icon(Icons.search),
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(vertical: 10),
            ),
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.shopping_cart_outlined, color: Colors.white),
            onPressed: () {
              // Navigasi ke halaman Keranjang, bukan Checkout
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const CartPage()),
              );
            },
          )
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: GridView.builder(
            // ... (kode GridView tetap sama) ...
            physics: const BouncingScrollPhysics(),
            itemCount: _filteredProducts.length,
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 0.62,
            ),
            itemBuilder: (context, index) {
              final produk = _filteredProducts[index];
              return Container(
                // ... (kode Container styling tetap sama) ...
                 decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.2),
                      blurRadius: 6,
                      offset: const Offset(0, 3),
                    )
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // ... (Kode untuk gambar, nama, brand, harga tetap sama) ...
                     ClipRRect(
                      borderRadius: const BorderRadius.vertical(
                          top: Radius.circular(16)),
                      child: Image.asset(
                        produk['gambar'],
                        height: 140,
                        width: double.infinity,
                        fit: BoxFit.cover,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        produk['nama'],
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8.0),
                      child: Text(
                        produk['brand'],
                        style:
                            TextStyle(color: Colors.grey[600], fontSize: 12),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8.0, vertical: 4.0),
                      child: Text(
                        "Rp ${produk['harga'].toString().replaceAllMapped(
                          RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'),
                          (Match m) => '${m[1]}.',
                        )}",
                        style: const TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 14),
                      ),
                    ),
                    const Spacer(), // Gunakan spacer agar tombol selalu di bawah
                    Align(
                      alignment: Alignment.bottomRight,
                      child: Padding(
                        padding:
                            const EdgeInsets.only(right: 10, bottom: 6),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            InkWell(
                              onTap: () => _addToWishlist(produk),
                              child: const Icon(
                                Icons.star_border,
                                color: Colors.orange,
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 10),
                            // Fungsikan tombol Add to Cart
                            InkWell(
                              onTap: () => _addToCart(produk),
                              child: Container(
                                decoration: const BoxDecoration(
                                  shape: BoxShape.circle,
                                  color: Colors.black,
                                ),
                                padding: const EdgeInsets.all(6),
                                child: const Icon(Icons.add,
                                    color: Colors.white, size: 20),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 4),
                  ],
                ),
              );
            },
          ),
        ),
      ),
      // ... (BottomNavigationBar tetap sama) ...
        bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        selectedItemColor: const Color(0xFFEE4D2D),
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          if (index == 0) {
            // Sudah di home, tidak perlu navigasi
          } else if (index == 1) {
            Navigator.pushReplacement(context,
                MaterialPageRoute(builder: (_) => const WishlistPage()));
          } else if (index == 2) {
            Navigator.pushReplacement(context,
                MaterialPageRoute(builder: (_) => const ProfilePage()));
          }
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: "Home"),
          BottomNavigationBarItem(icon: Icon(Icons.star), label: "Wishlist"),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: "Profile"),
        ],
      ),
    );
  }
}