# Smart Door with Face Recognition

This is a full-stack IoT project that enables secure, real-time smart door access using face recognition powered by ESP32-CAM, Flask + OpenCV, Firebase, and a mobile app built with Flutter.

---

##  Tech Stack

| Component       | Tech Used                          |
|----------------|------------------------------------|
| Microcontroller | ESP32-CAM (AI-Thinker)             |
| Face Recognition | Flask + OpenCV + face_recognition |
| Mobile App      | Flutter (Android/iOS)              |
| Backend         | Firebase (Realtime DB, Storage)    |
| Notifications   | Firebase Cloud Messaging (FCM)     |

---

##  Folder Structure

```
Smart_Door_Face_Recognition/
├── esp32-cam/                # ESP32 firmware
├── opencv-backend/           # Flask + OpenCV backend
├── smart-door-app/           # Flutter mobile app
```

---

##  Features

- Live face recognition via OpenCV backend
- Automatic unlock via relay on ESP32-CAM
- Push alerts to owner's phone using FCM
- Firebase Realtime DB stores logs with snapshots
- Flutter mobile app shows access history
- Secure config using .env and .example files

---

##  Setup

### ESP32-CAM
1. Flash `esp32-cam/main.ino` using Arduino IDE.
2. Create `WiFiConfig.h` with your secrets (see `WiFiConfig.example.h`).

### Backend
```bash
cd opencv-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Create a local `firebase_key.json` and `.env` file.

### Flutter App
Coming soon — under `smart-door-app/`.

---

##  Firebase Setup

- Enable Realtime DB
- Enable Firebase Storage
- Add Firebase Admin SDK Key to backend
- Use these rules:
```json
{
  "rules": {
    "access_logs": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

---

