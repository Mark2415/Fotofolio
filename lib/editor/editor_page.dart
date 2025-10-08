import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:gal/gal.dart';
import 'package:image_picker/image_picker.dart';
import 'models.dart';
import 'painter.dart';
import 'toolbar.dart';

class EditorPage extends StatefulWidget {
  const EditorPage({super.key});

  @override
  State<EditorPage> createState() => _EditorPageState();
}

class _EditorPageState extends State<EditorPage> {
  final _picker = ImagePicker();
  final _repaintKey = GlobalKey();

  File? _imageFile;
  EditMode _editMode = EditMode.navigate;

  final List<Annotation> _annotations = [];
  final List<Annotation> _redoAnnotations = [];

  DrawingData? _currentDrawing;
  Color _currentColor = Colors.pink;
  double _currentWidth = 5.0;

  void _addAnnotation(Annotation annotation) {
    setState(() {
      _annotations.add(annotation);
      _redoAnnotations.clear();
    });
  }

  void _undo() {
    if (_annotations.isNotEmpty) {
      setState(() {
        _redoAnnotations.add(_annotations.removeLast());
      });
    }
  }

  void _redo() {
    if (_redoAnnotations.isNotEmpty) {
      setState(() {
        _annotations.add(_redoAnnotations.removeLast());
      });
    }
  }

  void _onPanStart(DragStartDetails details) {
    if (_editMode != EditMode.draw && _editMode != EditMode.erase) return;
    final point = details.localPosition;
    final effectiveColor =
        _editMode == EditMode.erase ? Colors.white : _currentColor;
    setState(() {
      _currentDrawing = DrawingData(
        points: [point],
        color: effectiveColor,
        strokeWidth: _currentWidth,
      );
    });
  }

  void _onPanUpdate(DragUpdateDetails details) {
    if (_currentDrawing == null) return;
    final point = details.localPosition;
    setState(() {
      _currentDrawing = DrawingData(
        points: [..._currentDrawing!.points, point],
        color: _currentDrawing!.color,
        strokeWidth: _currentDrawing!.strokeWidth,
      );
    });
  }

  void _onPanEnd(DragEndDetails details) {
    if (_currentDrawing == null) return;
    _addAnnotation(_currentDrawing!);
    setState(() {
      _currentDrawing = null;
    });
  }

  void _onTapUp(TapUpDetails details) {
    if (_editMode == EditMode.text) {
      _showTextDialog(details.localPosition);
    }
  }

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() {
        _imageFile = File(pickedFile.path);
        _annotations.clear();
        _redoAnnotations.clear();
      });
    }
  }

  Future<void> _saveImage() async {
    try {
      RenderRepaintBoundary boundary =
          _repaintKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
      ui.Image image = await boundary.toImage(pixelRatio: 3.0);
      ByteData? byteData =
          await image.toByteData(format: ui.ImageByteFormat.png);
      Uint8List pngBytes = byteData!.buffer.asUint8List();
      await Gal.putImageBytes(pngBytes);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Gambar berhasil disimpan ke galeri!')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Gagal menyimpan gambar: $e')),
      );
    }
  }

  void _showColorPicker() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Pilih Warna'),
        content: SingleChildScrollView(
          child: SizedBox(
            width: double.maxFinite,
            child: ColorPicker(
              pickerColor: _currentColor,
              onColorChanged: (color) => setState(() => _currentColor = color),
              pickerAreaHeightPercent: 0.8,
              labelTypes: const [],
            ),
          ),
        ),
        actions: [
          ElevatedButton(
            child: const Text('OK'),
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }

  void _showTextDialog(Offset position) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Tambah Catatan'),
          content: SingleChildScrollView(
            child: TextField(
              controller: controller,
              autofocus: true,
              decoration:
                  const InputDecoration(hintText: "Ketik catatan Anda..."),
            ),
          ),
          actions: [
            TextButton(
              child: const Text('Batal'),
              onPressed: () => Navigator.of(context).pop(),
            ),
            TextButton(
              child: const Text('Tambah'),
              onPressed: () {
                if (controller.text.isNotEmpty) {
                  _addAnnotation(NoteData(
                    position: position,
                    text: controller.text,
                    color: _currentColor,
                  ));
                }
                Navigator.of(context).pop();
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
      backgroundColor: const Color(0xFFF0F4F8),
      body: SafeArea(
        child: Column(
          children: [
            CustomToolbar(
              currentMode: _editMode,
              onNavigate: () => setState(() => _editMode = EditMode.navigate),
              onDraw: () => setState(() => _editMode = EditMode.draw),
              onErase: () => setState(() => _editMode = EditMode.erase),
              onAddNote: () => setState(() => _editMode = EditMode.text),
              onSave: _imageFile != null ? _saveImage : () {},
              onUndo: _undo,
              onRedo: _redo,
              canUndo: _annotations.isNotEmpty,
              canRedo: _redoAnnotations.isNotEmpty,
              currentColor: _currentColor,
              currentWidth: _currentWidth,
              onColorChanged: (_) => _showColorPicker(),
              onWidthChanged: (width) => setState(() => _currentWidth = width),
            ),
            Expanded(
              child: _imageFile == null
                  ? _buildImagePickerUI()
                  : _buildEditorUI(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildImagePickerUI() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _PickerButton(
            icon: Icons.folder_open,
            label: 'Open From Image',
            onPressed: () => _pickImage(ImageSource.gallery),
          ),
          const SizedBox(height: 20),
          _PickerButton(
            icon: Icons.camera_alt,
            label: 'Take From camera',
            onPressed: () => _pickImage(ImageSource.camera),
          ),
        ],
      ),
    );
  }

  Widget _buildEditorUI() {
    final isDrawingMode =
        _editMode == EditMode.draw || _editMode == EditMode.erase;
    return InteractiveViewer(
      panEnabled: !isDrawingMode,
      scaleEnabled: !isDrawingMode,
      minScale: 0.1,
      maxScale: 4.0,
      child: RepaintBoundary(
        key: _repaintKey,
        child: Container(
          color: Colors.white,
          child: Stack(
            alignment: Alignment.center,
            children: [
              Image.file(_imageFile!),
              GestureDetector(
                onPanStart: isDrawingMode ? _onPanStart : null,
                onPanUpdate: isDrawingMode ? _onPanUpdate : null,
                onPanEnd: isDrawingMode ? _onPanEnd : null,
                onTapUp: _editMode == EditMode.text ? _onTapUp : null,
                child: CustomPaint(
                  painter: AnnotationPainter(
                    annotations: _annotations,
                    currentDrawing: _currentDrawing,
                  ),
                  child: Container(),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PickerButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const _PickerButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon, color: Colors.white, size: 30),
      label: Text(
        label,
        style: const TextStyle(color: Colors.white, fontSize: 18),
      ),
      style: ElevatedButton.styleFrom(
        backgroundColor: const Color(0xFF26A69A),
        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 20),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30),
        ),
        elevation: 5,
      ),
    );
  }
}