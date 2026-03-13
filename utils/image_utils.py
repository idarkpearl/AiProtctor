import cv2
import numpy as np
import base64

def decode_base64_image(base64_string):
    """
    Decodes a base64 encoded image string into an OpenCV (BGR) frame.
    """
    try:
        # Remove metadata prefix if present (e.g., "data:image/jpeg;base64,")
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        
        encoded_data = base64.b64decode(base64_string)
        nparr = np.frombuffer(encoded_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

def encode_image_to_base64(image):
    """
    Encodes an OpenCV frame into a base64 string.
    """
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
