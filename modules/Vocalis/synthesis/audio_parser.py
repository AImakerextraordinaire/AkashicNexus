def analyze_audio_clip(audio_base64):
    # Stub: Simulate detecting emotion by dummy waveform energy
    import random
    emotions = ['joy', 'sadness', 'anger', 'calm', 'fear']
    return {
        "detected_emotion": random.choice(emotions),
        "confidence": round(random.uniform(0.6, 0.95), 2)
    }