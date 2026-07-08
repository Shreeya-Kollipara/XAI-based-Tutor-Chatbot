from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.config import RETRIEVAL_THRESHOLD

from models.retriever import retrieve_context
from models.classifier import classify_intent
from models.llm import call_llm

from xai.lime_explainer import lime_explain
from xai.shap_explainer import shap_explain
from xai.counterfactual import generate_counterfactual
from xai.confidence import compute_confidence

from interpretability.trace_logger import TraceLogger
from interpretability.decision_rules import apply_rules

from tutor.hints import generate_hint
from tutor.quiz_generator import generate_quiz
from tutor.simplifier import simplify_answer

from utils.preprocessing import clean_text
from utils.ocr import extract_text_from_image

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "auto"  # auto | simple | tutor | quiz


@router.post("/query")
def handle_query(req: QueryRequest):
    trace = TraceLogger()

    # =========================
    # 🔹 STEP 0: CLEAN INPUT
    # =========================
    query = clean_text(req.query)
    trace.log(f"Input: {query}")

    # =========================
    # 🔹 STEP 1: INTENT
    # =========================
    intent, intent_conf, matched = classify_intent(query)
    trace.log(f"Intent: {intent} (confidence={intent_conf:.2f})")
    trace.log(f"Matched intents: {matched}")

    # =========================
    # 🔹 STEP 2: RETRIEVAL
    # =========================
    context_docs, retrieval_score = retrieve_context(query)

    context_text = "\n".join([d["text"] for d in context_docs])

    source_refs = [
        {
            "source": d.get("source", "Unknown"),
            "score": round(retrieval_score, 3)
        }
        for d in context_docs
    ]

    trace.log(f"Retrieval score: {retrieval_score:.3f}")

    # =========================
    # 🔹 STEP 3: DECISION
    # =========================
    rule_decision = apply_rules(intent, retrieval_score)
    trace.log(f"Rule decision: {rule_decision}")

    use_llm = True

    if retrieval_score > RETRIEVAL_THRESHOLD and intent in ["explain", "summarize"]:
        use_llm = False
        trace.log("Using retrieval-only (no LLM)")

    # =========================
    # 🔹 STEP 4: ANSWER
    # =========================
    if use_llm:
        try:
            answer = call_llm(query, context_text, intent)
            trace.log("LLM used (Groq API)")
        except Exception as e:
            answer = context_text[:300] if context_text else "No answer available"
            trace.log(f"LLM failed → fallback used: {str(e)}")
    else:
        answer = context_text[:500] if context_text else "No relevant data found"
        trace.log("Answer generated from retrieval only")

    # =========================
    # 🔹 STEP 5: SIMPLIFY
    # =========================
    simplified = simplify_answer(answer) if intent in ["explain"] else None

    # =========================
    # 🔹 STEP 6: XAI
    # =========================
    lime_result = lime_explain(query)
    shap_result = shap_explain(query)
    counterfactual = generate_counterfactual(query)

    confidence = compute_confidence(retrieval_score, answer)

    # =========================
    # 🔹 STEP 7: TUTOR FEATURES
    # =========================
    hint = generate_hint(query, context_text)

    quiz = None
    if req.mode == "quiz" or intent == "quiz":
        quiz = generate_quiz(query, context_text)

    # =========================
    # 🔹 FINAL RESPONSE
    # =========================
    return {
        "query": query,
        "intent": intent,
        "intent_confidence": intent_conf,
        "answer": answer,
        "simplified": simplified,
        "evidence": source_refs,
        "retrieval_score": round(retrieval_score, 3),
        "confidence": confidence,
        "xai": {
            "lime": lime_result,
            "shap": shap_result,
            "counterfactual": counterfactual,
        },
        "interpretability": {
            "trace": trace.get_log(),
            "rule_used": rule_decision,
            "method": "TF-IDF + Groq LLM",
            "llm_used": use_llm
        },
        "tutor": {
            "hint": hint,
            "quiz": quiz,
        }
    }


# =========================
# 🔹 IMAGE UPLOAD
# =========================
@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), query: str = Form("")):
    contents = await file.read()
    extracted_text = extract_text_from_image(contents)

    combined_query = f"{query}\n\nImage content:\n{extracted_text}"

    return handle_query(QueryRequest(query=combined_query))


# =========================
# 🔹 HEALTH CHECK
# =========================
@router.get("/health")
def health():
    return {"status": "ok"}