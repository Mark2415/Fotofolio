// checkout_page.dart

// ignore_for_file: unnecessary_to_list_in_spreads, deprecated_member_use

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:week_8_uts/cart_data.dart'; // Import CartItem

/// CheckoutPage displays a review of selected cart items, collects shipping
/// address and payment method, and calculates the final payable amount.
///
/// It expects a list of `CartItem` in the constructor (`checkoutItems`) which
/// are the items the user selected from the cart for checkout.
class CheckoutPage extends StatefulWidget {
  // The list of items to be processed in this checkout flow.
  final List<CartItem> checkoutItems;

  const CheckoutPage({super.key, required this.checkoutItems});

  @override
  State<CheckoutPage> createState() => _CheckoutPageState();
}

class _CheckoutPageState extends State<CheckoutPage> {
  // --- USER-SETTABLE / UI STATE ---
  String _selectedAddress = "Alamat belum diatur. Ketuk untuk mengatur.";
  String? _selectedPaymentMethod;
  
  // State untuk opsi pengiriman, 'Instant' menjadi default
  String _selectedShippingMethod = 'Instant'; 

  bool _isDamageProtection = true;
  bool _isDropshipper = false;

  // --- CALCULATION STATE ---
  double _subtotal = 0;
  final double _protectionCost = 2700;
  // Biaya pengiriman sekarang dinamis, diinisialisasi dengan biaya 'Instant'
  double _shippingCost = 20000; 
  final double _serviceFee = 1000;
  double _totalPayment = 0;
  
  // UI constants and formatters
  static const Color shopeeOrange = Color(0xFFEE4D2D);
  final currencyFormatter = NumberFormat.currency(locale: 'id_ID', symbol: 'Rp', decimalDigits: 0);
  // Formatter untuk tanggal pengiriman
  final DateFormat _dateFormatter = DateFormat('d MMM', 'id_ID');

  @override
  void initState() {
    super.initState();
    _calculatePayment();
  }

  /// Menghitung total pembayaran berdasarkan item dan opsi yang dipilih.
  void _calculatePayment() {
    _subtotal = widget.checkoutItems.fold(
      0, (sum, item) => sum + (item.product['harga'] * item.quantity));
      
    double currentProtectionCost = _isDamageProtection ? _protectionCost : 0;
    
    // Rumus baru tanpa diskon
    _totalPayment = _subtotal + currentProtectionCost + _shippingCost + _serviceFee;

    if (_totalPayment < 0) {
      _totalPayment = 0;
    }
    
    setState(() {});
  }

  /// Menampilkan dialog untuk memasukkan alamat pengiriman.
  Future<void> _showAddressDialog() async {
    final TextEditingController addressController = TextEditingController(text: _selectedAddress.contains('belum diatur') ? '' : _selectedAddress);
    String? result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Masukkan Alamat Pengiriman'),
        content: TextField(
          controller: addressController,
          autofocus: true,
          maxLines: 3,
          decoration: const InputDecoration(hintText: 'Contoh: Jl. Merdeka No. 1, Jakarta'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Batal'),
          ),
          TextButton(
            onPressed: () {
              if(addressController.text.isNotEmpty) {
                 Navigator.pop(context, addressController.text);
              }
            },
            child: const Text('Simpan'),
          ),
        ],
      ),
    );

    if (result != null) {
      setState(() {
        _selectedAddress = result;
      });
    }
  }

  /// Menampilkan pilihan metode pembayaran di bottom sheet.
  void _showPaymentMethods() {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return Wrap(
          children: <Widget>[
            const ListTile(
              title: Text('Pilih Metode Pembayaran', style: TextStyle(fontWeight: FontWeight.bold)),
            ),
            ListTile(
              leading: const Icon(Icons.qr_code),
              title: const Text('QRIS'),
              onTap: () {
                setState(() => _selectedPaymentMethod = 'QRIS');
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.account_balance_wallet),
              title: const Text('Virtual Account (VA)'),
              onTap: () {
                setState(() => _selectedPaymentMethod = 'Virtual Account (VA)');
                Navigator.pop(context);
              },
            ),
          ],
        );
      },
    );
  }

  /// Fungsi helper untuk menghitung dan memformat tanggal pengiriman.
  String _getDeliveryDate(int daysToAdd) {
    final deliveryDate = DateTime.now().add(Duration(days: daysToAdd));
    return _dateFormatter.format(deliveryDate);
  }

  /// Menampilkan pilihan Opsi Pengiriman di bottom sheet.
  void _showShippingOptions() {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return Wrap(
          children: <Widget>[
            const ListTile(
              title: Text('Pilih Opsi Pengiriman', style: TextStyle(fontWeight: FontWeight.bold)),
            ),
            // Opsi 1: Instant
            ListTile(
              leading: const Icon(Icons.flash_on, color: Colors.amber),
              title: const Text('Instant (recomended👍)'),
              subtitle: Text('Akan diterima pada tanggal ${_getDeliveryDate(7)}'),
              trailing: Text(currencyFormatter.format(20000)),
              onTap: () {
                setState(() {
                  _selectedShippingMethod = 'Instant';
                  _shippingCost = 20000;
                });
                _calculatePayment();
                Navigator.pop(context);
              },
            ),
            // Opsi 2: Normal
            ListTile(
              leading: const Icon(Icons.local_shipping, color: Colors.blue),
              title: const Text('Normal'),
              subtitle: Text('Akan diterima pada tanggal ${_getDeliveryDate(14)}'),
              trailing: Text(currencyFormatter.format(15000)),
              onTap: () {
                setState(() {
                  _selectedShippingMethod = 'Normal';
                  _shippingCost = 15000;
                });
                _calculatePayment();
                Navigator.pop(context);
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _buildAppBar(),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildAddressSection(),
            const SizedBox(height: 8),
            _buildProductSection(),
            const SizedBox(height: 8),
            _buildShippingSection(), // Widget pengiriman yang sudah diubah
            const SizedBox(height: 8),
            // Voucher section dihilangkan
            _buildPaymentMethodSection(),
            const SizedBox(height: 8),
            _buildPaymentDetailsSection(), // Rincian pembayaran yang sudah diubah
            const SizedBox(height: 8),
            _buildDropshipperSection(),
            const SizedBox(height: 16),
          ],
        ),
      ),
      bottomNavigationBar: _buildBottomBar(),
    );
  }

  AppBar _buildAppBar() {
    return AppBar(
      leading: IconButton(
        icon: const Icon(Icons.arrow_back),
        onPressed: () => Navigator.of(context).pop(),
      ),
      title: const Text('Checkout', style: TextStyle(fontWeight: FontWeight.bold)),
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
      elevation: 1,
    );
  }

  Widget _buildAddressSection() {
    return InkWell(
      onTap: _showAddressDialog,
      child: Container(
        color: Colors.white,
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(Icons.location_on_outlined, color: shopeeOrange),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Alamat Pengiriman', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(
                    _selectedAddress,
                    style: TextStyle(color: _selectedAddress.contains('belum diatur') ? Colors.red : Colors.black54),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey[400]),
          ],
        ),
      ),
    );
  }

  Widget _buildProductSection() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          const Row(
            children: [
              Icon(Icons.store_mall_directory_outlined, color: shopeeOrange),
              SizedBox(width: 8),
              Text('Uplu Official Store', style: TextStyle(fontWeight: FontWeight.bold)),
            ],
          ),
          const Divider(height: 24),
          ...widget.checkoutItems.map((item) => Padding(
            padding: const EdgeInsets.only(bottom: 12.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset(item.product['gambar'], width: 60, height: 60, fit: BoxFit.cover),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(item.product['nama']),
                      Text('Qty: ${item.quantity}', style: const TextStyle(color: Colors.black54)),
                    ],
                  ),
                ),
                Text(currencyFormatter.format(item.product['harga'] * item.quantity), style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
          )).toList(),
          const Divider(height: 24),
          Row(
            children: [
              SizedBox(
                width: 24, height: 24,
                child: Checkbox(
                  value: _isDamageProtection,
                  onChanged: (val) {
                    setState(() => _isDamageProtection = val!);
                    _calculatePayment();
                  },
                  activeColor: shopeeOrange,
                ),
              ),
              const SizedBox(width: 8),
              const Text('Proteksi Kerusakan +', style: TextStyle(fontWeight: FontWeight.bold)),
              const Spacer(),
              Text(currencyFormatter.format(_protectionCost), style: const TextStyle(fontWeight: FontWeight.bold)),
            ],
          ),
        ],
      ),
    );
  }
  
  // --- WIDGET PENGIRIMAN BARU ---
  /// Menampilkan opsi pengiriman yang dipilih dan membuka pilihan saat diketuk.
  Widget _buildShippingSection() {
    return InkWell(
      onTap: _showShippingOptions, // Panggil bottom sheet saat diketuk
      child: Container(
        color: Colors.white,
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Opsi Pengiriman', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                Text(currencyFormatter.format(_shippingCost), style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(_selectedShippingMethod, style: const TextStyle(fontWeight: FontWeight.bold)),
                      Text(
                        'Akan diterima pada tanggal ${_getDeliveryDate(_selectedShippingMethod == 'Instant' ? 7 : 14)}',
                        style: const TextStyle(fontSize: 12, color: Colors.black54)
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPaymentMethodSection() {
    return InkWell(
      onTap: _showPaymentMethods,
      child: Container(
        color: Colors.white,
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Metode Pembayaran', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                Text('Lihat Semua >', style: TextStyle(color: Colors.grey)),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Text(
                  _selectedPaymentMethod ?? 'Pilih Metode Pembayaran',
                  style: TextStyle(color: _selectedPaymentMethod == null ? Colors.red : Colors.black),
                ),
                const Spacer(),
                const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
              ],
            ),
          ],
        ),
      ),
    );
  }

  // --- WIDGET RINCIAN PEMBAYARAN BARU ---
  /// Menampilkan rincian pembayaran tanpa voucher.
  Widget _buildPaymentDetailsSection() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Rincian Pembayaran', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 12),
          _buildDetailRow('Subtotal Pesanan', currencyFormatter.format(_subtotal)),
          _buildDetailRow('Total Proteksi Produk', currencyFormatter.format(_isDamageProtection ? _protectionCost : 0)),
          _buildDetailRow('Subtotal Pengiriman', currencyFormatter.format(_shippingCost)),
          _buildDetailRow('Biaya Layanan', currencyFormatter.format(_serviceFee), hasInfo: true),
          // Baris voucher diskon dihilangkan
          const Divider(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Total Pembayaran', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text(currencyFormatter.format(_totalPayment), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: shopeeOrange)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBottomBar() {
    return Container(
      height: 60,
      color: Colors.white,
      child: Row(
        children: [
          Expanded(
            flex: 3,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                const Text('Total Pembayaran'),
                Text(currencyFormatter.format(_totalPayment), style: const TextStyle(fontWeight: FontWeight.bold, color: shopeeOrange, fontSize: 16)),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: InkWell(
              onTap: () {
                if(_selectedAddress.contains('belum diatur')) {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Alamat tidak boleh kosong!'), backgroundColor: Colors.red,));
                  return;
                }
                if(_selectedPaymentMethod == null) {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Metode pembayaran harus dipilih!'), backgroundColor: Colors.red,));
                  return;
                }

                showDialog(context: context, builder: (ctx) => AlertDialog(
                  title: const Text('Pesanan Berhasil'),
                  content: Text('Pesanan Anda dengan total ${currencyFormatter.format(_totalPayment)} telah berhasil dibuat.'),
                  actions: [TextButton(onPressed: ()=> Navigator.of(ctx).pop(), child: const Text('OK'))],
                ));

              },
              child: Container(
                margin: const EdgeInsets.only(left: 16),
                color: shopeeOrange,
                child: const Center(
                  child: Text('Buat Pesanan', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // -- SUPPORTING WIDGETS --

  Widget _buildDropshipperSection() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text('Kirim sebagai Dropshipper'),
          Switch(
            value: _isDropshipper,
            onChanged: (val) => setState(() => _isDropshipper = val),
            activeColor: shopeeOrange,
          ),
        ],
      ),
    );
  }
  
  Widget _buildDetailRow(String label, String value, {bool hasInfo = false, bool isDiscount = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Text(label, style: const TextStyle(color: Colors.black54)),
              if(hasInfo) ...[
                const SizedBox(width: 4),
                const Icon(Icons.info_outline, size: 14, color: Colors.grey),
              ]
            ],
          ),
          Text(value, style: TextStyle(fontWeight: FontWeight.bold, color: isDiscount ? Colors.green : Colors.black)),
        ],
      ),
    );
  }
}