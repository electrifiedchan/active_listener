import cv2
import numpy as np
from collections import deque

# --- SAFETY IMPORT BLOCK ---
try:
    from fer import FER
    print("✅ Using Standard FER Import")
except ImportError:
    try:
        from fer.fer import FER
        print("✅ Using Fixed FER Import")
    except ImportError:
        print("❌ CRITICAL ERROR: Could not import FER. Check installation.")

class VideoCamera(object):
    def __init__(self):
        # 1. THE CAMERA FIX: We add cv2.CAP_DSHOW to stop the "Camera Busy" error
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # 2. THE EMOTION DETECTOR
        # mtcnn=True is slower but better. If laggy, set to False.
        self.detector = FER(mtcnn=True)
        
        # 3. THE MISSING ATTRIBUTE (This fixes your AttributeError)
        self.last_emotion = "neutral"
        
        # 4. STABILIZER (Keeps the mood from flickering)
        self.emotion_history = deque(maxlen=5)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None

        # FER requires RGB colors (OpenCV uses BGR by default)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        try:
            # Detect Emotions
            result = self.detector.detect_emotions(rgb_image)

            if result:
                # Find the biggest face
                face = max(result, key=lambda x: x['box'][2] * x['box'][3])
                box = face['box']
                emotions = face['emotions']
                
                # Get the strongest emotion
                top_emotion, score = max(emotions.items(), key=lambda item: item[1])
                
                # --- UPDATE THE MEMORY ---
                self.emotion_history.append(top_emotion)
                stable_emotion = max(set(self.emotion_history), key=self.emotion_history.count)
                
                # SAVE IT TO THE CLASS SO APP.PY CAN READ IT
                self.last_emotion = stable_emotion

                # Draw UI
                x, y, w, h = box
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Label
                text = f"{stable_emotion.upper()}: {int(score*100)}%"
                cv2.putText(image, text, (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
        except Exception as e:
            # If detection fails, just keep the last emotion
            pass

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()