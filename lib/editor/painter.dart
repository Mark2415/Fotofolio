// ignore_for_file: deprecated_member_use

import 'dart:ui';
import 'package:flutter/material.dart';
import 'models.dart';

class AnnotationPainter extends CustomPainter {
  final List<Annotation> annotations;
  final DrawingData? currentDrawing;

  AnnotationPainter({
    required this.annotations,
    this.currentDrawing,
  });

  @override
  void paint(Canvas canvas, Size size) {
    for (var annotation in annotations) {
      if (annotation is DrawingData) {
        final drawing = annotation;
        final paint = Paint()
          ..color = drawing.color
          ..strokeWidth = drawing.strokeWidth
          ..style = PaintingStyle.stroke
          ..strokeCap = StrokeCap.round
          ..blendMode = drawing.blendMode;

        final path = Path();
        if (drawing.points.isNotEmpty) {
          path.moveTo(drawing.points.first.dx, drawing.points.first.dy);
          for (var i = 1; i < drawing.points.length; i++) {
            path.lineTo(drawing.points[i].dx, drawing.points[i].dy);
          }
        }
        canvas.drawPath(path, paint);
      } else if (annotation is NoteData) {
        final note = annotation;
        final textSpan = TextSpan(
          text: note.text,
          style: TextStyle(
            color: note.color,
            fontSize: note.fontSize,
            backgroundColor: Colors.black.withOpacity(0.5),
          ),
        );
        final textPainter = TextPainter(
          text: textSpan,
          textAlign: TextAlign.center,
          textDirection: TextDirection.ltr,
        );
        textPainter.layout();
        textPainter.paint(canvas, note.position);
      }
    }

    if (currentDrawing != null && currentDrawing!.points.isNotEmpty) {
      final paint = Paint()
        ..color = currentDrawing!.color
        ..strokeWidth = currentDrawing!.strokeWidth
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..blendMode = currentDrawing!.blendMode;

      final path = Path();
      path.moveTo(
          currentDrawing!.points.first.dx, currentDrawing!.points.first.dy);
      for (var i = 1; i < currentDrawing!.points.length; i++) {
        path.lineTo(
            currentDrawing!.points[i].dx, currentDrawing!.points[i].dy);
      }
      canvas.drawPath(path, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}