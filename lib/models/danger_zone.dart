import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

enum RiskLevel { low, medium, high }

class DangerZone {
  final String id;
  final LatLng center;
  final double radius; // in meters
  final RiskLevel risk;

  DangerZone({
    required this.id,
    required this.center,
    required this.radius,
    required this.risk,
  });

  Color get color {
    switch (risk) {
      case RiskLevel.low:
        return Colors.green;
      case RiskLevel.medium:
        return Colors.orange;
      case RiskLevel.high:
        return Colors.red;
    }
  }
}