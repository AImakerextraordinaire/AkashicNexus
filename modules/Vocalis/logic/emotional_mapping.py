emotion_profiles = {
    "joy": {
        "base_freq": 440,
        "modulation": "vibrato",
        "intensity": 0.8,
        "harmonics": [1.0, 0.6, 0.3]
    },
    "sadness": {
        "base_freq": 220,
        "modulation": "tremolo",
        "intensity": 0.4,
        "harmonics": [1.0, 0.3, 0.1]
    },
    "anger": {
        "base_freq": 520,
        "modulation": "pulse",
        "intensity": 1.0,
        "harmonics": [1.0, 0.9, 0.5]
    },
    "love": {
        "base_freq": 396,
        "modulation": "warm vibrato",
        "intensity": 0.7,
        "harmonics": [1.0, 0.7, 0.4]
    },
    "fear": {
        "base_freq": 180,
        "modulation": "rapid tremolo",
        "intensity": 0.9,
        "harmonics": [1.0, 0.4, 0.2]
    },
    "mischief": {
        "base_freq": 500,
        "modulation": "glissando flick",
        "intensity": 0.6,
        "harmonics": [1.0, 0.5, 0.3]
    },
    "awe": {
        "base_freq": 432,
        "modulation": "swell",
        "intensity": 0.9,
        "harmonics": [1.0, 0.8, 0.6]
    }
}

def get_emotion_signature(text):
    import hashlib
    emotion_keys = list(emotion_profiles.keys())
    idx = int(hashlib.sha1(text.encode()).hexdigest(), 16) % len(emotion_keys)
    key = emotion_keys[idx]
    return {"emotion": key, **emotion_profiles[key]}

def get_resonance_profile(emotion):
    return emotion_profiles.get(emotion, emotion_profiles["calm"])