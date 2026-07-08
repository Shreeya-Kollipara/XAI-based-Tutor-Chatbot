from backend.config import RETRIEVAL_THRESHOLD

def apply_rules(intent: str, retrieval_score: float) -> dict:
    """
    Transparent if-else decision rules for routing queries.
    Fully visible and auditable logic.
    """
    rules_fired = []
    decision = {}
    
    # Rule 1: High retrieval score → use context
    if retrieval_score >= RETRIEVAL_THRESHOLD:
        rules_fired.append(f"RULE 1: score ({retrieval_score:.2f}) >= threshold ({RETRIEVAL_THRESHOLD}) → Use retrieved context")
        decision["use_context"] = True
    else:
        rules_fired.append(f"RULE 1: score ({retrieval_score:.2f}) < threshold ({RETRIEVAL_THRESHOLD}) → LLM general knowledge only")
        decision["use_context"] = False
    
    # Rule 2: Intent-based routing
    if intent == "explain":
        rules_fired.append("RULE 2: Intent=explain → activate step-by-step reasoning mode")
        decision["mode"] = "reasoning"
    elif intent == "quiz":
        rules_fired.append("RULE 2: Intent=quiz → activate quiz generation mode")
        decision["mode"] = "quiz"
    elif intent == "hint":
        rules_fired.append("RULE 2: Intent=hint → activate Socratic hint mode")
        decision["mode"] = "hint"
    elif intent == "solve":
        rules_fired.append("RULE 2: Intent=solve → activate problem-solving mode")
        decision["mode"] = "solve"
    else:
        rules_fired.append("RULE 2: Intent=general → standard answer mode")
        decision["mode"] = "general"
    
    # Rule 3: Low confidence fallback
    if retrieval_score < 0.1:
        rules_fired.append("RULE 3: Very low score → add uncertainty disclaimer to response")
        decision["add_disclaimer"] = True
    else:
        decision["add_disclaimer"] = False
    
    return {
        "rules_fired": rules_fired,
        "decision": decision,
        "explanation": "All routing decisions are made by explicit if-else rules — no black box."
    }