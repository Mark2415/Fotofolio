/// Simple in-memory holder for wishlist items used by the demo app.
///
/// Each wishlist item is represented as a `Map<String, dynamic>` matching
/// the product map shape used elsewhere (keys like 'nama', 'harga', 'gambar').
/// This class is intentionally minimal; replace with a proper persistence
/// or state-management solution in larger apps.
class WishlistData {
  // The list of products the user added to their wishlist.
  static List<Map<String, dynamic>> wishlistItems = [];
}
