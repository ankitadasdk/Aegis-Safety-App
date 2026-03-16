import 'package:flutter/material.dart';
import 'screens/home_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Women Safety',
      theme: ThemeData(primarySwatch: Colors.pink),
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}