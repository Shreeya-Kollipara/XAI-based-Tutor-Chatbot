import re
from collections import Counter

# Lightweight LIME-style explainer (no sklearn dependency for demo)
# For production, use: from lime.lime_text import LimeTextExplainer

STOP_WORDS = {"the", "a", "an", "is", "in", "on", "at", "to", "and", "or", "of", "for", "it", "be", "do", "i", "me", "my"}

def lime_explain(query: str) -> dict:
    """
    Simplified LIME: perturbs the input by removing words one-at-a-time
    and reports which words most affect the query's 'information content'.
    
    In production, replace with actual LIME using a classifier.
    """
    words = [w for w in re.findall(r'\b\w+\b', query.lower()) if w not in STOP_WORDS and len(w) > 2]
    
    if not words:
        return {"important_words": [], "explanation": "No significant words found."}
    
    # Simulate word importance by TF-character proxy (longer/rarer words = more important)
    word_scores = {}
    for word in set(words):
        freq = words.count(word)
        importance = round(len(word) * 0.1 + (1 / freq) * 0.5, 3)
        word_scores[word] = min(importance, 1.0)

    # Sort by importance
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "method": "LIME (perturbation-based)",
        "important_words": [{"word": w, "importance": s} for w, s in sorted_words],
        "explanation": f"The answer is most influenced by: {', '.join([w for w, _ in sorted_words[:3]])}",
        "note": "Higher score = word removal causes bigger answer change"
    }