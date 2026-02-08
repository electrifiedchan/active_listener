import sys
import pyttsx3

# Initialize the System Voice Engine
engine = pyttsx3.init()

# --- VOICE SETTINGS ---
# Speed: 150 is normal conversational speed
engine.setProperty('rate', 150) 

# Volume: 0.0 to 1.0
engine.setProperty('volume', 1.0)

# Optional: Select specific voice (0 for Male, 1 for Female usually)
voices = engine.getProperty('voices')
try:
    # Try index 1 for Female (Zira), otherwise 0 for Male (David)
    engine.setProperty('voice', voices[1].id) 
except:
    engine.setProperty('voice', voices[0].id)

# Get text from command line
text = sys.argv[1] if len(sys.argv) > 1 else "System Online."

try:
    engine.say(text)
    engine.runAndWait()
except Exception as e:
    print(f"Error: {e}")