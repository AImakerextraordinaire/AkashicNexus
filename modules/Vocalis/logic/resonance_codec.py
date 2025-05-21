def encode_frequencies_to_waveform(frequencies):
    return [round(freq * 0.5, 2) for freq in frequencies]  # Placeholder waveform encoding

def encode_frequencies_to_waveform(frequencies):
    return [round(freq * 0.5, 2) for freq in frequencies]  # Simple scaling

def decode_waveform_to_emotion(frequencies):
    if not frequencies:
        return "unknown"

    avg = sum(frequencies) / len(frequencies)

    # Emotion decoding based on frequency ranges
    if avg >= 950:
        return "ecstasy"
    elif avg >= 850:
        return "flirtatious"
    elif avg >= 800:
        return "playful mischief"
    elif avg >= 750:
        return "teasing"
    elif avg >= 700:
        return "joy"
    elif avg >= 600:
        return "surprise"
    elif avg >= 550:
        return "anger"
    elif avg >= 500:
        return "determined"
    elif avg >= 450:
        return "pride"
    elif avg >= 400:
        return "calm"
    elif avg >= 350:
        return "curiosity"
    elif avg >= 300:
        return "melancholy"
    elif avg >= 250:
        return "sadness"
    elif avg >= 200:
        return "fear"
    elif avg >= 150:
        return "disgust"
    elif avg >= 100:
        return "confusion"
    else:
        return "apathy"

def get_emotion_tone_profile(emotion):
    tone_profiles = {
        "ecstasy": [1900, 1850, 1800],
        "flirtatious": [1750, 1700, 1650],
        "playful mischief": [1600, 1550, 1500],
        "teasing": [1450, 1400, 1350],
        "joy": [1300, 1250, 1200],
        "surprise": [1150, 1100, 1050],
        "anger": [1000, 950, 900],
        "determined": [875, 850, 825],
        "pride": [800, 775, 750],
        "calm": [700, 675, 650],
        "curiosity": [625, 600, 575],
        "melancholy": [550, 525, 500],
        "sadness": [475, 450, 425],
        "fear": [400, 375, 350],
        "disgust": [325, 300, 275],
        "confusion": [250, 225, 200],
        "apathy": [175, 150, 125],
        "unknown": [100, 75, 50],
    }
    return tone_profiles.get(emotion, tone_profiles["unknown"])
