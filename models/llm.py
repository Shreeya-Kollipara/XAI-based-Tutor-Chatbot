import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.config import GROQ_API_KEY, LLM_MODEL
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)


def call_llm(query: str, context: str = "", intent: str = "explain") -> str:
    """
    Calls Groq LLM API with structured tutoring prompts.
    Falls back gracefully if API fails.
    """

    # =========================
    # 🔹 PROMPT ENGINEERING
    # =========================
    if intent == "quiz":
        prompt = f"""You are an educational tutor. Generate 3 multiple choice quiz questions.

Context: {context}
Topic: {query}

Format:
Q: ...
A) ...
B) ...
C) ...
D) ...
Answer: ...
"""

    elif intent == "explain":
        prompt = f"""You are a friendly tutor.

Explain the concept step-by-step in simple language.

Context:
{context}

Question: {query}

Provide:
1. One-line definition
2. Step-by-step explanation (3-5 steps)
3. Real-world analogy

Keep it clear and concise.
"""

    else:
        prompt = f"""You are a helpful tutor.

Context:
{context}

Question: {query}

Answer clearly and concisely.
"""

    # =========================
    # 🔹 API CALL
    # =========================
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an intelligent tutoring assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )

        return response.choices[0].message.content

    # =========================
    # 🔹 FALLBACKS
    # =========================
    except Exception as e:
        return (
            f"[LLM API Error] {str(e)}\n\n"
            f"Fallback answer:\n"
            f"This question relates to '{query}'.\n"
            f"Retrieved context: {context[:200] if context else 'None'}..."
        )