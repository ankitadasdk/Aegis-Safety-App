import 'package:location/location.dart';

class LocationService {
  final Location _location = Location();

  Future<bool> _requestPermission() async {
    var permission = await _location.hasPermission();
    if (permission == PermissionStatus.denied) {
      permission = await _location.requestPermission();
    }
    return permission == PermissionStatus.granted;
  }

  Future<LocationData?> getCurrentLocation() async {
    bool serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await _location.requestService();
      if (!serviceEnabled) return null;
    }

    bool hasPermission = await _requestPermission();
    if (!hasPermission) return null;

    return await _location.getLocation();
  }
}