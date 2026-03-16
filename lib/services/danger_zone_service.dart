import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../models/danger_zone.dart';

class DangerZoneService {
  // Mock data – in a real app, fetch from API with past crime data and time.
  static List<DangerZone> getMockZones(LatLng currentLocation) {
    return [
      DangerZone(
        id: '1',
        center: LatLng(currentLocation.latitude + 0.01, currentLocation.longitude + 0.01),
        radius: 300,
        risk: RiskLevel.high,
      ),
      DangerZone(
        id: '2',
        center: LatLng(currentLocation.latitude - 0.015, currentLocation.longitude - 0.015),
        radius: 500,
        risk: RiskLevel.medium,
      ),
      DangerZone(
        id: '3',
        center: LatLng(currentLocation.latitude + 0.02, currentLocation.longitude - 0.02),
        radius: 200,
        risk: RiskLevel.low,
      ),
    ];
  }
}