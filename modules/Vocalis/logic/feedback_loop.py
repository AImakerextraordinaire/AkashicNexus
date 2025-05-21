feedback_registry = {}

def adjust_model(emotion, rating):
    if emotion not in feedback_registry:
        feedback_registry[emotion] = []
    feedback_registry[emotion].append(rating)
    return {"message": f"Feedback for '{emotion}' recorded.", "avg_rating": round(sum(feedback_registry[emotion]) / len(feedback_registry[emotion]), 2)}