import re

COMPLEX_TO_SIMPLE = {
    "photosynthesis": "how plants make food",
    "osmosis": "water movement through membranes",
    "mitosis": "cell division",
    "algorithm": "step-by-step instructions",
    "hypothesis": "educated guess",
    "kinetic energy": "energy of motion",
    "velocity": "speed with direction",
    "catalyst": "something that speeds up a reaction",
}

def simplify_answer(answer: str) -> str:
    """
    Simplifies complex terminology in the answer for beginner learners.
    """
    simplified = answer
    for term, simple in COMPLEX_TO_SIMPLE.items():
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        simplified = pattern.sub(f"{term} ({simple})", simplified, count=1)
    
    # Trim to key sentences if too long
    sentences = re.split(r'(?<=[.!?])\s+', simplified)
    if len(sentences) > 6:
        simplified = ' '.join(sentences[:6]) + "\n\n[Simplified view — ask for full details]"
    
    return simplified