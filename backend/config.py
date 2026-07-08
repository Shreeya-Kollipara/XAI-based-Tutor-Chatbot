import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================
# 🔹 LLM API CONFIG (Groq)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

# =========================
# 🔹 RETRIEVAL SETTINGS
# =========================
TFIDF_TOP_K = int(os.getenv("TFIDF_TOP_K", 3))
RETRIEVAL_THRESHOLD = float(os.getenv("RETRIEVAL_THRESHOLD", 0.3))

# =========================
# 🔹 DATA PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCUMENTS_PATH = os.path.join(BASE_DIR, "..", "data", "documents.json")

# =========================
# 🔹 CONFIDENCE THRESHOLDS
# =========================
HIGH_CONFIDENCE = float(os.getenv("HIGH_CONFIDENCE", 0.75))
MID_CONFIDENCE = float(os.getenv("MID_CONFIDENCE", 0.5))

# =========================
# 🔹 SYSTEM FLAGS
# =========================
USE_LLM = os.getenv("USE_LLM", "true").lower() == "true"
ENABLE_XAI = os.getenv("ENABLE_XAI", "true").lower() == "true"
ENABLE_COUNTERFACTUAL = os.getenv("ENABLE_COUNTERFACTUAL", "true").lower() == "true"
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"