import 'dart:io' show Platform;
import 'package:camera/camera.dart';
import 'package:record/record.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path_provider/path_provider.dart';

class EvidenceRecorder {
  CameraController? _cameraController;
  final AudioRecorder _audioRecorder = AudioRecorder();
  bool _isRecordingVideo = false;
  bool _isRecordingAudio = false;

  // Added a setup method to pre-initialize the camera for better performance
  Future<void> setup() async {
    if (Platform.isAndroid || Platform.isIOS) {
      try {
        final cameras = await availableCameras();
        if (cameras.isNotEmpty) {
          _cameraController = CameraController(
            cameras.first, 
            ResolutionPreset.medium,
            enableAudio: false,
          );
          await _cameraController!.initialize();
        }
      } catch (e) {
        print('Pre-initialization camera error: $e');
      }
    }
  }

  Future<void> startRecording() async {
    print('Starting evidence recording...');

    // 1. Request permissions properly
    Map<Permission, PermissionStatus> statuses = await [
      Permission.camera,
      Permission.microphone,
    ].request();

    if (statuses[Permission.microphone] != PermissionStatus.granted) {
      print('Microphone permission denied');
      return;
    }

    // 2. VIDEO RECORDING (Android/iOS focus)
    if (!Platform.isWindows && !Platform.isLinux) {
      try {
        // If not initialized yet, do it now
        if (_cameraController == null || !_cameraController!.value.isInitialized) {
          await setup();
        }

        if (_cameraController != null && _cameraController!.value.isInitialized) {
          await _cameraController!.startVideoRecording();
          _isRecordingVideo = true;
          print('Video recording started');
        }
      } catch (e) {
        print('Video recording start error: $e');
      }
    }

    // 3. AUDIO RECORDING
    try {
      final dir = await getApplicationDocumentsDirectory();
      final timestamp = DateTime.now().millisecondsSinceEpoch;
      // Fixed: Using path join logic for better platform compatibility
      final filePath = '${dir.path}${Platform.pathSeparator}sos_audio_$timestamp.${_getAudioExtension()}';

      final config = RecordConfig(
        encoder: _getAudioEncoder(),
        bitRate: 128000,
        sampleRate: 44100,
      );

      // Check for permission right before starting
      if (await _audioRecorder.hasPermission()) {
        await _audioRecorder.start(config, path: filePath);
        _isRecordingAudio = true;
        print('Audio recording started at: $filePath');
      }
    } catch (e) {
      print('Audio recording error: $e');
    }
  }

  String _getAudioExtension() {
    if (Platform.isWindows || Platform.isLinux) return 'wav';
    return 'm4a';
  }

  AudioEncoder _getAudioEncoder() {
    if (Platform.isWindows || Platform.isLinux) return AudioEncoder.pcm16bits;
    return AudioEncoder.aacLc;
  }

  Future<void> stopRecording() async {
    print('Stopping evidence recording...');
    
    // Stop Video
    if (_isRecordingVideo && _cameraController != null) {
      try {
        final XFile file = await _cameraController!.stopVideoRecording();
        print('Video saved: ${file.path}');
        _isRecordingVideo = false;
        // Don't dispose yet if you want to reuse it, but for SOS we can reset
      } catch (e) {
        print('Error stopping video: $e');
      }
    }

    // Stop Audio
    if (_isRecordingAudio) {
      try {
        final path = await _audioRecorder.stop();
        print('Audio saved: $path');
        _isRecordingAudio = false;
      } catch (e) {
        print('Error stopping audio: $e');
      }
    }
  }

  void dispose() {
    _cameraController?.dispose();
    _audioRecorder.dispose();
  }
}