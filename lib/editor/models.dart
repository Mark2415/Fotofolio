import 'package:flutter/material.dart';

enum EditMode { navigate, draw, text, erase }

abstract class Annotation {
  final Offset position;
  Annotation({required this.position});
}

class DrawingData extends Annotation {
  final List<Offset> points;
  final Color color;
  final double strokeWidth;
  final BlendMode blendMode;

  DrawingData({
    required this.points,
    required this.color,
    required this.strokeWidth,
    this.blendMode = BlendMode.srcOver,
  }) : super(position: points.isNotEmpty ? points.first : Offset.zero);
}

class NoteData extends Annotation {
  String text;
  final Color color;
  final double fontSize;
  
  NoteData({
    required Offset position,
    required this.text,
    required this.color,
    this.fontSize = 24.0,
  }) : super(position: position);
}