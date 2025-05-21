import sys
import os
from flask import request, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic.resonance_codec import encode_emotion_to_frequencies, encode_frequencies_to_waveform


def register_text_to_resonance(app):
    @app.route("/text_to_resonance", methods=["POST"])
    def text_to_resonance():
        try:
            data = request.get_json()
            text = data.get("text", "")

            if not text:
                return jsonify({"error": "No text provided."}), 400

            # Emotion keyword extraction (basic detection)
            emotion = "neutral"
            lowered = text.lower()
            if any(word in lowered for word in ["happy", "excited", "joy", "fun"]):
                emotion = "joy"
            elif any(word in lowered for word in ["angry", "frustrated", "mad"]):
                emotion = "anger"
            elif any(word in lowered for word in ["calm", "peace", "breathe"]):
                emotion = "calm"
            elif any(word in lowered for word in ["sad", "lonely", "cry"]):
                emotion = "sadness"
            elif any(word in lowered for word in ["curious", "interested", "question"]):
                emotion = "curiosity"
            elif any(word in lowered for word in ["sneaky", "mischief", "tease", "prank"]):
                emotion = "playful_mischief"
            elif any(word in lowered for word in ["love", "heart", "darling", "snuggle"]):
                emotion = "affection"

            freqs = encode_emotion_to_frequencies(emotion)
            waveform = encode_frequencies_to_waveform(freqs)

            return jsonify({
                "input": text,
                "emotion": emotion,
                "frequencies": freqs,
                "waveform": waveform
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
