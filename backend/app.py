from flask import Flask, Response, jsonify
from flask_cors import CORS
from camera import VideoCamera
import threading
import time
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Initialize Camera
camera_stream = VideoCamera()

def speak_worker():
    last_spoken_emotion = None
    print("✅ Voice Module: ONLINE (System Voice Mode)")

    while True:
        current_emotion = camera_stream.last_emotion
        
        if current_emotion and current_emotion != "neutral":
            if current_emotion != last_spoken_emotion:
                
                # Professional, concise phrase
                phrase = f"You appear {current_emotion}."
                print(f"🗣️ Speaking: {phrase}")
                
                try:
                    # --- THE SWITCH: Use speak.py (Offline System Voice) ---
                    subprocess.run(
                        [sys.executable, "speak.py", phrase], 
                        shell=False
                    )
                except Exception as e:
                    print(f"❌ Subprocess Error: {e}")
                
                last_spoken_emotion = current_emotion
                time.sleep(4) # Wait a bit so it doesn't overlap
        
        time.sleep(1)

# Start Background Thread
t = threading.Thread(target=speak_worker)
t.daemon = True
t.start()

# --- ROUTES ---

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion')
def get_emotion():
    return jsonify({'emotion': camera_stream.last_emotion})

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)