import sys
import requests
import pygame
import os

# --- CONFIGURATION ---
API_KEY = "130abcf4ffd3887e3b29726bc4ebd544839f4d2c1b4e2d53b032beb4ab3b5557"
VOICE_ID = "ErXwobaYiN019PkySvjV"  # Antoni (System Voice - Free)

# Get text from command line
text = sys.argv[1] if len(sys.argv) > 1 else "System Check. Neural Link Established."

def generate_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": text,
        # --- THE FIX: UPGRADE TO V2 ---
        "model_id": "eleven_multilingual_v2", 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            
            # Play Audio
            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.quit()
            os.remove("output.mp3") 
            print("✅ Voice Output Complete.")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    generate_voice(text)