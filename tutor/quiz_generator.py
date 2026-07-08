import re

def generate_quiz(query: str, context: str = "") -> list:
    """
    Generates simple fill-in-the-blank and MCQ quiz questions.
    For full generation, the LLM handles this via intent=quiz in routes.
    This is a rule-based fallback.
    """
    words = re.findall(r'\b[A-Za-z]{5,}\b', query + " " + context)
    unique_words = list(set([w.lower() for w in words if w.lower() not in
                              {"which", "where", "about", "their", "these", "those", "there", "under", "after"}]))[:5]
    
    questions = []
    
    if unique_words:
        q1 = {
            "type": "fill_blank",
            "question": f"_______ refers to the main concept discussed in this topic.",
            "answer": unique_words[0] if unique_words else "unknown",
            "hint": f"It starts with '{unique_words[0][0].upper()}'" if unique_words else ""
        }
        questions.append(q1)
    
    if len(unique_words) >= 2:
        q2 = {
            "type": "true_false",
            "question": f"The concept of '{unique_words[0]}' is related to '{unique_words[1]}'.",
            "answer": "True (in most contexts)",
            "hint": "Think about the definitions of both terms."
        }
        questions.append(q2)
    
    q3 = {
        "type": "open_ended",
        "question": f"Explain '{query}' in your own words.",
        "answer": "Open-ended — check your answer with the explanation above.",
        "hint": "Use the step-by-step explanation as a guide."
    }
    questions.append(q3)
    
    return questions