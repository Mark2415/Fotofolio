// wishlist_page.dart

import 'package:flutter/material.dart';
import 'package:week_8_uts/cart_data.dart'; // Import CartData - helper that manages cart items
import 'package:week_8_uts/wishlist_data.dart';
import 'package:week_8_uts/homepage.dart';

/// A page that displays the user's wishlist.
///
/// The wishlist is a simple in-memory list stored in `WishlistData.wishlistItems`.
/// This page shows each wishlist item as a [ListTile] with an image, name,
/// brand, and actions to add the item to the cart or remove it from the
/// wishlist. When an item is added to the cart the shared `CartData` helper
/// is updated and a brief [SnackBar] is shown as feedback.
class WishlistPage extends StatefulWidget {
  const WishlistPage({super.key});

  @override
  State<WishlistPage> createState() => _WishlistPageState();
}

class _WishlistPageState extends State<WishlistPage> {

  void _addToCart(Map<String, dynamic> product) {
    // Adds the selected product to the shared CartData and refreshes the UI
    setState(() {
      CartData.addToCart(product);
    });

    // Provide transient feedback to the user using a SnackBar
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text("${product['nama']} ditambahkan ke keranjang!"),
      backgroundColor: Colors.blue,
      duration: const Duration(seconds: 1),
    ));
  }

  @override
  Widget build(BuildContext context) {
    // Read the live wishlist from the shared holder. The list is mutable and
    // updates here will immediately reflect in the UI because we call setState().
    final wishlist = WishlistData.wishlistItems;

    return Scaffold(
      appBar: AppBar(
        // Page title and styling
        title: const Text("Wishlist", style: TextStyle(color: Colors.white)),
        backgroundColor: const Color(0xFFEE4D2D),
        // Leading back button returns to HomePage using pushReplacement so
        // that the wishlist is not left in the navigation stack.
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (_) => const HomePage()),
            );
          },
        ),
      ),

      // If the wishlist is empty show a friendly placeholder message; otherwise
      // render each wishlist entry in a Card containing an image, title,
      // subtitle (brand) and action buttons.
      body: wishlist.isEmpty
          ? const Center(
              child: Text(
                "Belum ada produk di wishlist 😢",
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            )
          : ListView.builder(
              itemCount: wishlist.length,
              itemBuilder: (context, index) {
                final item = wishlist[index];

                // Each wishlist item is displayed inside a Card for nice visual
                // separation. ListTile provides a consistent leading/title/
                // subtitle/trailing layout.
                return Card(
                  margin:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: ListTile(
                    leading: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.asset(
                        // Path to the local asset image for the product
                        item['gambar'],
                        width: 55,
                        height: 55,
                        fit: BoxFit.cover,
                      ),
                    ),
                    title: Text(
                      item['nama'],
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(item['brand']),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // Button: add the item to the shared cart
                        IconButton(
                          icon: const Icon(Icons.add_shopping_cart, color: Colors.green),
                          onPressed: () => _addToCart(item),
                        ),

                        // Button: remove the item from the wishlist and show a
                        // confirmation SnackBar. We use setState to update the UI
                        // immediately after removing the item from the list.
                        IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () {
                            setState(() {
                              wishlist.removeAt(index);
                            });
                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content:
                                  Text("${item['nama']} dihapus dari wishlist!"),
                              backgroundColor: Colors.redAccent,
                              duration: const Duration(seconds: 2),
                            ));
                          },
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}