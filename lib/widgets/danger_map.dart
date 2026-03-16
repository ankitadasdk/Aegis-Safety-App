import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class DangerMap extends StatelessWidget {
  final LatLng initialPosition;
  final Set<Marker> markers;
  final Set<Circle> circles;
  final Set<Polyline> polylines;

  const DangerMap({
    super.key,
    required this.initialPosition,
    this.markers = const {},
    this.circles = const {},
    this.polylines = const {},
  });

  @override
  Widget build(BuildContext context) {
    return GoogleMap(
      initialCameraPosition: CameraPosition(
        target: initialPosition,
        zoom: 14,
      ),
      markers: markers,
      circles: circles,
      polylines: polylines,
      myLocationEnabled: true,
      myLocationButtonEnabled: true,
    );
  }
}