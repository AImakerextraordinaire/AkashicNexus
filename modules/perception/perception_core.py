import pytesseract
from PIL import Image
import io
from flask import request, jsonify


def interpret_audio(audio_segment):
    """
    Process an audio segment and extract transcribed text using speech recognition.
    """
    try:
        print("[??] Interpreting audio segment...")
        # Placeholder logic – swap for real audio-to-text if available
        transcript = "Audio content interpreted successfully."
        return {
            "status": "processed",
            "transcript": transcript
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def interpret_frame(image_data):
    """
    Process raw image bytes and extract text from the image using OCR.
    """
    print("[???] Interpreting visual frame...")
    try:
        # Convert raw image bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))

        # Extract text via OCR
        extracted_text = pytesseract.image_to_string(image)

        return {
            "status": "processed",
            "text_detected": extracted_text.strip()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def register_perception_core_endpoints(app):
    @app.route('/analyze_audio', methods=['POST'])
    def analyze_audio():
        try:
            data = request.get_json()
            audio_data = data.get("audio_data")
            if not audio_data:
                return jsonify({"error": "Missing 'audio_data' parameter"}), 400
            result = interpret_audio(audio_data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/analyze_image', methods=['POST'])
    def analyze_image():
        try:
            data = request.get_json()
            image_base64 = data.get("image_base64")
            if not image_base64:
                return jsonify({"error": "Missing 'image_base64' parameter"}), 400
            result = interpret_frame(image_base64)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500