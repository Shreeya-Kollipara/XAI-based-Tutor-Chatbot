import re

def generate_hint(query: str, context: str = "") -> str:
    """
    Generates a Socratic-style hint without giving the full answer.
    """
    words = re.findall(r'\b\w+\b', query.lower())
    key_words = [w for w in words if len(w) > 4][:3]
    
    hints = []
    
    if key_words:
        hints.append(f"💡 Think about what you already know about: {', '.join(key_words)}")
    
    if context:
        first_sentence = context.split('.')[0] if '.' in context else context[:80]
        hints.append(f"📖 Here's a starting point: {first_sentence}...")
    
    hints.append("🤔 Try breaking the question into smaller parts — what does each part mean?")
    
    return " | ".join(hints) if hints else "Think step-by-step. What do you already know about this topic?"