// cart_data.dart

// Simple data model for the shopping cart used by the app.
// This file intentionally keeps the model minimal: a `CartItem` wraps a
// product (represented as a `Map`) and a mutable `quantity`.

/// Represents one entry in the shopping cart.
///
/// `product` is a map containing the product details used by the UI. Common
/// keys expected by the rest of the app are:
/// - `'nama'` (String): product name
/// - `'harga'` (num): product price
/// - `'gambar'` (String): asset path for the product image
///
/// `quantity` is the number of units of this product in the cart.
class CartItem {
  final Map<String, dynamic> product;
  int quantity;

  CartItem({required this.product, this.quantity = 1});
}

/// Static holder for cart state shared across the app.
///
/// For this simple example the cart is stored in-memory as a static list.
/// In a production app you would usually replace this with a scoped state
/// management solution or persist the cart to local storage.
class CartData {
  // List of items currently in the cart. Each element is a `CartItem`.
  static final List<CartItem> cartItems = [];

  /// Adds a product to the cart.
  ///
  /// If a product with the same `'nama'` already exists in the cart, this
  /// function increases its `quantity`. Otherwise it creates a new
  /// `CartItem` and appends it to `cartItems`.
  static void addToCart(Map<String, dynamic> product) {
    // Check if product already exists in the cart (match by 'nama'). If so,
    // increment the quantity for that item and return early.
    for (var item in cartItems) {
      if (item.product['nama'] == product['nama']) {
        item.quantity++; // Product found: increase quantity
        return;
      }
    }

    // Product not found: add as a new cart item with default quantity 1.
    cartItems.add(CartItem(product: product));
  }
}