from PIL import Image
import io
import base64

def image_to_sonic_signature(image_base64):
    try:
        image_bytes = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize((10, 10))
        pixels = list(img.getdata())

        tone_map = []
        for r, g, b in pixels:
            frequency = 200 + int((r + g + b) / 3)  # Simple average to frequency
            tone_map.append(frequency)

        return tone_map  # List of frequency values
    except Exception as e:
        return {"error": str(e)}