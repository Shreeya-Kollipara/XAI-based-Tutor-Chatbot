def compute_confidence(retrieval_score: float, answer: str) -> dict:
    """
    Computes a multi-factor confidence score.
    Factors: retrieval score, answer length, keyword presence.
    """
    # Factor 1: Retrieval similarity
    retrieval_factor = min(retrieval_score * 1.2, 1.0)
    
    # Factor 2: Answer length (longer = more informative, up to a point)
    word_count = len(answer.split())
    length_factor = min(word_count / 100, 1.0) if word_count > 0 else 0.0
    
    # Factor 3: No uncertainty phrases
    uncertainty_phrases = ["i don't know", "i'm not sure", "unclear", "cannot", "error", "ollama not running"]
    uncertainty_factor = 0.0
    for phrase in uncertainty_phrases:
        if phrase.lower() in answer.lower():
            uncertainty_factor = -0.3
            break
    
    # Weighted combination
    raw_score = (retrieval_factor * 0.6) + (length_factor * 0.3) + (uncertainty_factor)
    final_score = max(0.0, min(1.0, raw_score))
    final_score = round(final_score, 3)
    
    # Label
    if final_score >= 0.75:
        label = "High"
        color = "green"
    elif final_score >= 0.45:
        label = "Moderate"
        color = "orange"
    else:
        label = "Low"
        color = "red"
    
    return {
        "score": final_score,
        "label": label,
        "color": color,
        "breakdown": {
            "retrieval_factor": round(retrieval_factor, 3),
            "length_factor": round(length_factor, 3),
            "uncertainty_penalty": uncertainty_factor
        },
        "explanation": f"Confidence is {label.lower()} ({final_score}) based on retrieval quality and answer completeness."
    }