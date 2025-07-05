import 'package:flutter/material.dart';
import '../theme/octo_theme.dart';
import 'octo_button_variant.dart';

class OctoButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final bool expand;
  final OctoButtonVariant variant;

  const OctoButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.icon,
    this.expand = false,
    this.variant = OctoButtonVariant.primary,
  });

  @override
  Widget build(BuildContext context) {
    final Color backgroundColor;
    final Color foregroundColor;
    final bool isDisabled = onPressed == null || variant == OctoButtonVariant.disabled;

    switch (variant) {
      case OctoButtonVariant.primary:
        backgroundColor = OctoColors.purpleNeon;
        foregroundColor = Colors.black;
        break;
      case OctoButtonVariant.cyan:
        backgroundColor = OctoColors.borderNeon;
        foregroundColor = Colors.black;
        break;
      case OctoButtonVariant.danger:
        backgroundColor = OctoColors.orangeNeon;
        foregroundColor = Colors.black;
        break;
      case OctoButtonVariant.disabled:
        backgroundColor = OctoColors.disabled;
        foregroundColor = Colors.grey.shade300;
        break;
    }

    final Widget child = Row(
      mainAxisSize: expand ? MainAxisSize.max : MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (icon != null) Icon(icon, size: 18),
        if (icon != null) const SizedBox(width: 8),
        Text(label),
      ],
    );

    return ElevatedButton(
      onPressed: isDisabled ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor,
        foregroundColor: foregroundColor,
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
        minimumSize: expand ? const Size.fromHeight(48) : null,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
      ),
      child: child,
    );
  }
}
