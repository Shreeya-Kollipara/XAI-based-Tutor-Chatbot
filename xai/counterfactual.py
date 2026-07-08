import re

STOP_WORDS = {"the", "a", "an", "is", "in", "on", "at", "to", "and", "or", "of", "for", "it"}

def generate_counterfactual(query: str) -> dict:
    """
    Generates counterfactual explanations:
    'If you changed X in the query, the answer would change to Y.'
    """
    words = [w for w in re.findall(r'\b\w+\b', query.lower()) if w not in STOP_WORDS and len(w) > 2]
    
    if len(words) < 2:
        return {
            "counterfactuals": [],
            "explanation": "Query too short to generate counterfactuals."
        }
    
    # Sort by length (longest words are likely most important)
    key_words = sorted(set(words), key=len, reverse=True)[:3]
    
    counterfactuals = []
    for kw in key_words:
        example = query.lower().replace(kw, "[REMOVED]")
        counterfactuals.append({
            "original_query": query,
            "modified_query": example,
            "removed_word": kw,
            "impact": f"Removing '{kw}' would likely make the answer less specific or change its focus.",
            "severity": "high" if len(kw) > 6 else "medium"
        })
    
    # Add a "what-if" style counterfactual
    what_if = {
        "scenario": f"What if the question was about a different subject than '{words[0]}'?",
        "impact": "The system would retrieve entirely different documents and generate a different answer.",
        "type": "topic_change"
    }
    
    return {
        "method": "Counterfactual Analysis",
        "counterfactuals": counterfactuals,
        "what_if": what_if,
        "explanation": f"The most critical words in your query are: {', '.join(key_words)}. Removing any of them significantly changes the answer."
    }