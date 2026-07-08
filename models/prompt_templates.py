def tutor_prompt(query, context):
    return f"""
You are a tutor.

Context:
{context}

Question:
{query}

Give:
1. Answer
2. Step-by-step reasoning
3. Simple explanation
4. One hint
"""