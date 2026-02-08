try:
    from fer.fer import FER
    import cv2
    
    print("--------------------------------------------------")
    print("✅ SUCCESS: FER Library imported!")
    
    # Initialize the detector to make sure weights load correctly
    detector = FER(mtcnn=True) 
    print("✅ SUCCESS: FER Detector initialized with MTCNN!")
    print("--------------------------------------------------")

except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
except Exception as e:
    print(f"❌ OTHER ERROR: {e}")