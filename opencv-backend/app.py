from flask import Flask, request, jsonify
import cv2
import numpy as np
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

app = Flask(__name__)

# Load Firebase credentials (local-only)
# DO NOT PUSH actual credentials
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://YOUR_PROJECT.firebaseio.com",
    "storageBucket": "YOUR_PROJECT.appspot.com"
})

known_encodings = np.load("known_faces/encodings.npy", allow_pickle=True)
known_names = ["John", "Alice", "Bob"]

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(img)

    if len(encodings) == 0:
        return jsonify({"recognized": False, "name": "unknown", "confidence": 0})

    face_encoding = encodings[0]
    results = face_recognition.compare_faces(known_encodings, face_encoding)
    name = "unknown"
    confidence = 0

    if True in results:
        match_index = results.index(True)
        name = known_names[match_index]
        confidence = 95  # Simulated confidence

    # Save image to Firebase Storage
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"face_{timestamp}.jpg"
    cv2.imwrite(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    bucket = storage.bucket()
    blob = bucket.blob(f"faces/{filename}")
    blob.upload_from_filename(filename)
    image_url = blob.public_url

    # Log to Realtime DB
    ref = db.reference("access_logs").push()
    ref.set({
        "name": name,
        "status": "recognized" if name != "unknown" else "denied",
        "timestamp": timestamp,
        "image_url": image_url
    })

    return jsonify({
        "recognized": name != "unknown",
        "name": name,
        "confidence": confidence,
        "image_url": image_url
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)