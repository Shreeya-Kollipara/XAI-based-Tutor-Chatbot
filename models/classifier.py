import re
from typing import Tuple, List

INTENT_RULES = {
    "explain": [
        r"\bexplain\b", r"\bwhat is\b", r"\bdefine\b",
        r"\bdescribe\b", r"\bhow does\b", r"\bwhat are\b"
    ],
    "quiz": [
        r"\bquiz\b", r"\btest me\b", r"\bask me\b",
        r"\bquestion\b", r"\bpractice\b"
    ],
    "hint": [
        r"\bhint\b", r"\bgive me a clue\b",
        r"\bhelp me\b", r"\bstuck\b"
    ],
    "compare": [
        r"\bcompare\b", r"\bdifference between\b",
        r"\bvs\b", r"\bversus\b"
    ],
    "solve": [
        r"\bsolve\b", r"\bcalculate\b",
        r"\bcompute\b", r"\bfind\b", r"\bprove\b"
    ],
    "summarize": [
        r"\bsummarize\b", r"\bsummary\b",
        r"\bbrief\b", r"\boverview\b"
    ],
}

def classify_intent(query: str) -> Tuple[str, float, List[str]]:
    """
    Returns:
    - primary intent
    - confidence score
    - all matched intents (for interpretability)
    """

    q = query.lower()
    matched_intents = []

    for intent, patterns in INTENT_RULES.items():
        for pattern in patterns:
            if re.search(pattern, q):
                matched_intents.append(intent)
                break  # avoid duplicate matches per intent

    # =========================
    # 🔹 NO MATCH
    # =========================
    if not matched_intents:
        return "general", 0.5, []

    # =========================
    # 🔹 MULTI-INTENT HANDLING
    # =========================
    primary_intent = matched_intents[0]

    # Confidence = number of matches / total intents
    confidence = min(1.0, len(matched_intents) / len(INTENT_RULES))

    return primary_intent, confidence, matched_intents