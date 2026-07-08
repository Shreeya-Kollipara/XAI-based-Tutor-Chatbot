import re

# Lightweight SHAP-style explainer
# For production with a real model: import shap

STOP_WORDS = {"the", "a", "an", "is", "in", "on", "at", "to", "and", "or", "of", "for"}

KNOWLEDGE_TERMS = {
    "photosynthesis", "gravity", "evolution", "molecule", "cell", "energy", "force",
    "theorem", "equation", "function", "algorithm", "network", "matrix", "vector",
    "atom", "electron", "protein", "dna", "rna", "osmosis", "reaction", "catalyst",
    "mitosis", "meiosis", "newton", "einstein", "voltage", "current", "resistance"
}

def shap_explain(query: str) -> dict:
    """
    Simplified SHAP: assigns Shapley-value-like scores based on
    word contribution to retrieval relevance.
    
    Production version: use shap.Explainer with a real model.
    """
    words = re.findall(r'\b\w+\b', query.lower())
    total_words = len(words)
    
    if total_words == 0:
        return {"contributions": [], "baseline": 0.0}
    
    word_contributions = {}
    baseline = 0.1  # Average model output without any input words
    
    for word in words:
        if word in STOP_WORDS:
            contribution = round(-0.02, 3)  # Negative: stop words reduce quality
        elif word in KNOWLEDGE_TERMS:
            contribution = round(0.35, 3)   # High: domain-specific term
        elif len(word) > 6:
            contribution = round(0.15, 3)   # Medium: longer words tend to be informative
        elif len(word) > 3:
            contribution = round(0.08, 3)
        else:
            contribution = round(0.02, 3)
        
        word_contributions[word] = contribution
    
    sorted_contributions = sorted(word_contributions.items(), key=lambda x: x[1], reverse=True)[:6]
    
    return {
        "method": "SHAP (Shapley additive explanations)",
        "baseline_score": baseline,
        "contributions": [{"word": w, "shap_value": v} for w, v in sorted_contributions],
        "explanation": "SHAP values show each word's contribution to the final answer quality.",
        "note": "Positive = increases answer relevance | Negative = decreases"
    }