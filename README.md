# 🛡️ Aegis | Smart Women's Safety Ecosystem

**Aegis** is a full-stack safety solution built with **Flutter** and **FastAPI**. It leverages real-time location services and hardware-level triggers (accelerometer) to provide an immediate response during emergencies.

---

##  Key Features

* **📳 Shake-to-Alert:** Uses the `shake` package to detect high-frequency physical movement, triggering an SOS even when the app is in the background.
* **📍 Live GPS Tracking:** Accurate location retrieval via `geolocator` with real-time mapping using `Maps_flutter`.
* **🔗 FastAPI Backend:** A dedicated Python backend that receives SOS payloads (User ID, Latitude, Longitude, Timestamp) via the `/sos/trigger` endpoint.
* **🎙️ Evidence Collection:** Automated logic for audio and video recording using `record` and `camera` packages.
* **📊 Dashboard Ready:** Designed to sync with a centralized emergency monitoring system.

---

## 🛠️ Tech Stack

### Frontend (Mobile App)
- **Framework:** Flutter (Dart)
- **Networking:** `http` for RESTful communication.
- **Hardware:** Accelerometer (Shake Detection), GPS, Microphone, and Camera.
- **State Management:** StatefulWidget (Scalable to Provider/Bloc).

### Backend (Server)
- **Framework:** FastAPI (Python)
- **Data Format:** JSON
- **Logic:** Real-time logging and emergency distribution.

---

## 📂 Project Structure

```text
lib/
├── screens/
│   ├── home_screen.dart      # Main UI with Shake listener & SOS Button
│   └── map_screen.dart       # Google Maps real-time tracking
├── services/
│   ├── api_service.dart      # Flutter-to-FastAPI communication logic
│   ├── location_service.dart # GPS handling & Coordinate fetching
│   └── record_service.dart   # Evidence recorder implementation
└── main.dart                 # App initialization & Permissions
