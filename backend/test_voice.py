import pyttsx3

print("--- STARTING VOICE TEST ---")

try:
    # Initialize the engine
    engine = pyttsx3.init()
    
    # Force it to speak loud and clear
    engine.setProperty('volume', 1.0) 
    
    # Say something
    print("Speaking now...")
    engine.say("Testing. Testing. One two three.")
    
    # Block until done
    engine.runAndWait()
    
    print("--- VOICE TEST COMPLETE ---")

except Exception as e:
    print(f"ERROR: {e}")