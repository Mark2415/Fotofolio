// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'models.dart';

class CustomToolbar extends StatelessWidget {
  final EditMode currentMode;
  final VoidCallback onNavigate;
  final VoidCallback onDraw;
  final VoidCallback onErase;
  final VoidCallback onAddNote;
  final VoidCallback onSave;
  final VoidCallback onUndo;
  final VoidCallback onRedo;
  final bool canUndo;
  final bool canRedo;
  final ValueChanged<Color> onColorChanged;
  final ValueChanged<double> onWidthChanged;
  final Color currentColor;
  final double currentWidth;

  const CustomToolbar({
    super.key,
    required this.currentMode,
    required this.onNavigate,
    required this.onDraw,
    required this.onErase,
    required this.onAddNote,
    required this.onSave,
    required this.onUndo,
    required this.onRedo,
    required this.canUndo,
    required this.canRedo,
    required this.onColorChanged,
    required this.onWidthChanged,
    required this.currentColor,
    required this.currentWidth,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
      decoration: const BoxDecoration(
        color: Color(0xFF4FC3F7),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const SizedBox(width: 48),
              const Text(
                'Simple Image Annotation',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
              Row(
                children: [
                  _ToolbarButton(
                    icon: Icons.undo,
                    onPressed: onUndo,
                    enabled: canUndo,
                  ),
                  const SizedBox(width: 8),
                  _ToolbarButton(
                    icon: Icons.redo,
                    onPressed: onRedo,
                    enabled: canRedo,
                  ),
                  const SizedBox(width: 8),
                  _ToolbarButton(
                    icon: Icons.save_alt_outlined,
                    onPressed: onSave,
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            height: 50,
            child: Row(
              children: [
                _ToolModeButton(
                  icon: Icons.touch_app_outlined,
                  label: 'Navigate',
                  isSelected: currentMode == EditMode.navigate,
                  onPressed: onNavigate,
                ),
                _ToolModeButton(
                  icon: Icons.brush,
                  label: 'Anotate',
                  isSelected: currentMode == EditMode.draw,
                  onPressed: onDraw,
                ),
                _ToolModeButton(
                  icon: Icons.cleaning_services,
                  label: 'Eraser',
                  isSelected: currentMode == EditMode.erase,
                  onPressed: onErase,
                ),
                _ToolModeButton(
                  icon: Icons.note_add_outlined,
                  label: 'Note',
                  isSelected: currentMode == EditMode.text,
                  onPressed: onAddNote,
                ),
                const Spacer(),
                GestureDetector(
                  onTap: () => onColorChanged(currentColor),
                  child: CircleAvatar(
                    backgroundColor: currentColor,
                    radius: 16,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Slider(
                    value: currentWidth,
                    min: 1.0,
                    max: 20.0,
                    onChanged: onWidthChanged,
                    activeColor: Colors.white,
                    inactiveColor: Colors.black26,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ToolbarButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onPressed;
  final bool enabled;

  const _ToolbarButton({
    required this.icon,
    required this.onPressed,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: enabled ? onPressed : null,
        borderRadius: BorderRadius.circular(24),
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: enabled
                ? Colors.white.withOpacity(0.9)
                : Colors.grey.withOpacity(0.5),
            borderRadius: BorderRadius.circular(24),
          ),
          child:
              Icon(icon, color: enabled ? const Color(0xFF01579B) : Colors.white70),
        ),
      ),
    );
  }
}

class _ToolModeButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isSelected;
  final VoidCallback onPressed;

  const _ToolModeButton({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? Colors.white : const Color(0xFF26A69A),
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            if (isSelected)
              BoxShadow(
                color: Colors.black.withOpacity(0.3),
                blurRadius: 4,
                offset: const Offset(0, 2),
              )
          ],
        ),
        child: Row(
          children: [
            Icon(
              icon,
              color: isSelected ? const Color(0xFF00796B) : Colors.white,
              size: 20,
            ),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                color: isSelected ? const Color(0xFF00796B) : Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}