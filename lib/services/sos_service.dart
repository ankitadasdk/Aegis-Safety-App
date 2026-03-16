import 'package:flutter/material.dart';
import 'package:shake/shake.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:permission_handler/permission_handler.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class SosService {
  final Function() onSosTriggered;
  stt.SpeechToText? _speech;
  bool _isListening = false;
  String _lastWords = '';
  String? _authToken;
  String _backendUrl;
  
  ShakeDetector? _shakeDetector;

  SosService({
    required this.onSosTriggered, 
    String? authToken, 
    String backendUrl = 'http://172.20.21.39:8000' // Using your laptop IP
  }) : _authToken = authToken, _backendUrl = backendUrl {
    _init();
  }

  void _init() async {
    // 1. Shake Detector Initialization
    _shakeDetector = ShakeDetector.autoStart(
      onPhoneShake: (event) { // <--- Add 'event' here
        print('🚨 Shake detected! Triggering SOS...');
        onSosTriggered();
      },
      minimumShakeCount: 3,
      shakeSlopTimeMS: 500,
      shakeCountResetTime: 3000, 
      shakeThresholdGravity: 2.7,
    );

    // 2. Speech to Text Initialization
    _speech = stt.SpeechToText();
    await _initVoice();
  }
  
  Future<void> _initVoice() async {
    var status = await Permission.microphone.status;
    if (status.isDenied) {
      await Permission.microphone.request();
    }

    bool available = await _speech!.initialize(
      onError: (error) {
        print('⚠️ Speech error: $error');
        _isListening = false;
        // If it's a timeout, try to restart after a delay
        if (error.errorMsg == 'error_speech_timeout' || error.errorMsg == 'error_client') {
          Future.delayed(const Duration(seconds: 2), () => _startListening());
        }
      },
      onStatus: (status) {
        print('🎙️ Speech status: $status');
        // If the engine stops, wait 1 second then restart to prevent the loop
        if (status == 'notListening' || status == 'done') {
          _isListening = false;
          Future.delayed(const Duration(seconds: 1), () => _startListening()); 
        }
      },
    );
    
    if (available) {
      _startListening();
    }
  }

  void _startListening() {
    // Double check to ensure we don't start multiple instances
    if (_isListening || _speech!.isListening) return;
    _isListening = true;

    _speech!.listen(
      onResult: (result) {
        _lastWords = result.recognizedWords;
        print('Recognized: $_lastWords');
        
        // Custom trigger phrases
        if (_lastWords.toLowerCase().contains('i need help') || 
            _lastWords.toLowerCase().contains('help me')) {
          onSosTriggered();
        }
      },
      listenFor: const Duration(minutes: 5),
      pauseFor: const Duration(seconds: 10),
      listenMode: stt.ListenMode.deviceDefault,
    );
  }

  Future<bool> triggerSOS(double lat, double lon) async {
    // If you haven't implemented login yet, we'll bypass the token check for testing
    final url = '$_backendUrl/sos/trigger';
    
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          if (_authToken != null) 'Authorization': 'Bearer $_authToken',
        },
        body: jsonEncode({
          'latitude': lat,
          'longitude': lon,
        }),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('✅ Backend notified successfully!');
        return true;
      } else {
        print('❌ Backend error: ${response.statusCode}');
        return false;
      }
    } catch (e) {
      print('❌ Network Error: $e');
      return false;
    }
  }

  void updateAuthToken(String token) {
    _authToken = token;
  }

  void dispose() {
    _shakeDetector?.stopListening(); 
    _speech?.stop();
    _isListening = false;
  }
}