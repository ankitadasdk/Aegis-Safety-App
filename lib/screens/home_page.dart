import 'package:flutter/material.dart';
import '../services/sos_service.dart'; 

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late SosService _sosService;
  bool _isSending = false;

  @override
  void initState() {
    super.initState();
    // Initialize the SOS service with your laptop's IP address
    _sosService = SosService(
      onSosTriggered: _handleEmergency,
      backendUrl: 'http://172.20.21.39:8000', 
    );
  }

  void _handleEmergency() async {
    if (_isSending) return;
    
    setState(() => _isSending = true);

    // Using test coordinates - link to geolocator for real-time GPS
    bool success = await _sosService.triggerSOS(16.506, 80.648);

    if (mounted) {
      setState(() => _isSending = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(success ? "🚨 SOS Alert Sent Successfully!" : "❌ Connection Failed"),
          backgroundColor: success ? Colors.green : Colors.red,
          duration: const Duration(seconds: 3),
        ),
      );
    }
  }

  @override
  void dispose() {
    _sosService.dispose(); // Cleanup listeners to prevent memory leaks
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F1115), // Deep Midnight Black for better visibility
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20.0),
          child: Column(
            children: [
              const SizedBox(height: 30),
              _buildMinimalHeader(),
              const SizedBox(height: 40),
              
              // Large SOS Button (Centerpiece)
              Expanded(
                flex: 4,
                child: _buildEmergencyButton(),
              ),
              
              const SizedBox(height: 40),
              
              // Quick Action Grid
              Expanded(
                flex: 3,
                child: _buildActionGrid(),
              ),
              
              _buildLocationBar(),
              const SizedBox(height: 10),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMinimalHeader() {
    return Row(
      children: [
        const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("SYSTEM ACTIVE", 
              style: TextStyle(color: Colors.greenAccent, fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
            Text("Women Safety", // Updated Project Name
              style: TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.bold)),
          ],
        ),
        const Spacer(),
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(12)),
          child: const Icon(Icons.shield, color: Colors.blueAccent, size: 20),
        )
      ],
    );
  }

  Widget _buildEmergencyButton() {
    return Center(
      child: Stack(
        alignment: Alignment.center,
        children: [
          // Decorative outer ring
          Container(
            width: 270,
            height: 270,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: Colors.redAccent.withOpacity(0.1), width: 2),
            ),
          ),
          // Interactive Button
          GestureDetector(
            onLongPress: _handleEmergency, // Long press to prevent accidents
            child: Container(
              width: 220,
              height: 220,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.redAccent.withOpacity(0.3),
                    blurRadius: 40,
                    spreadRadius: 5,
                  )
                ],
                gradient: const RadialGradient(
                  colors: [Color(0xFFFF3B30), Color(0xFF8E0000)],
                ),
              ),
              child: Center(
                child: _isSending 
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.warning_amber_rounded, color: Colors.white, size: 55),
                        SizedBox(height: 12),
                        Text("HOLD FOR", style: TextStyle(color: Colors.white70, fontSize: 14, fontWeight: FontWeight.bold)),
                        Text("SOS", style: TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.w900)),
                      ],
                    ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionGrid() {
    return GridView.count(
      crossAxisCount: 2,
      crossAxisSpacing: 15,
      mainAxisSpacing: 15,
      childAspectRatio: 1.6,
      children: [
        _buildSmallAction(Icons.phone_callback, "Fake Call"),
        _buildSmallAction(Icons.record_voice_over, "Voice Record"),
        _buildSmallAction(Icons.map_outlined, "Safe Route"),
        _buildSmallAction(Icons.contact_phone_outlined, "Contacts"),
      ],
    );
  }

  Widget _buildSmallAction(IconData icon, String label) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1A1D23),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: Colors.white, size: 26),
          const SizedBox(height: 8),
          Text(label, style: const TextStyle(color: Colors.white70, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildLocationBar() {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 20),
      decoration: BoxDecoration(
        color: const Color(0xFF1A1D23),
        borderRadius: BorderRadius.circular(16),
      ),
      child: const Row(
        children: [
          Icon(Icons.gps_fixed, color: Colors.greenAccent, size: 16),
          SizedBox(width: 12),
          Text("Tracking: Active - VIT-AP", 
            style: TextStyle(color: Colors.white38, fontSize: 12, fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }
}