import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.config import DOCUMENTS_PATH, TFIDF_TOP_K

# Load documents
def load_documents():
    try:
        with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback sample documents for demo
        return [
            {"id": 1, "text": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce oxygen and energy in the form of glucose.", "source": "Biology Textbook, Ch. 3", "topic": "biology"},
            {"id": 2, "text": "Newton's three laws of motion describe the relationship between a body and the forces acting upon it, and its motion in response to those forces.", "source": "Physics Textbook, Ch. 5", "topic": "physics"},
            {"id": 3, "text": "The water cycle describes how water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface.", "source": "Earth Science, Ch. 2", "topic": "science"},
            {"id": 4, "text": "Mitosis is the process by which a eukaryotic cell separates the chromosomes in its cell nucleus into two identical sets in two nuclei.", "source": "Cell Biology, Ch. 4", "topic": "biology"},
            {"id": 5, "text": "The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse equals the sum of squares of the other two sides.", "source": "Mathematics, Ch. 7", "topic": "math"},
            {"id": 6, "text": "Gravity is a fundamental force that attracts two objects with mass toward each other. On Earth, gravity gives weight to objects and causes them to fall.", "source": "Physics Textbook, Ch. 3", "topic": "physics"},
            {"id": 7, "text": "DNA (deoxyribonucleic acid) is the molecule that carries genetic information in all living organisms. It consists of two strands forming a double helix.", "source": "Genetics, Ch. 1", "topic": "biology"},
            {"id": 8, "text": "Electricity is the flow of electric charge through a conductor. Voltage drives the current, and resistance opposes it, described by Ohm's Law: V = IR.", "source": "Physics Textbook, Ch. 8", "topic": "physics"},
        ]

_docs = load_documents()
_texts = [d["text"] for d in _docs]

_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
_tfidf_matrix = _vectorizer.fit_transform(_texts)


def retrieve_context(query: str, top_k: int = TFIDF_TOP_K):
    """
    Returns top-k relevant documents and the best similarity score.
    Fully interpretable: TF-IDF cosine similarity.
    """
    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _tfidf_matrix).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]
    top_docs = [_docs[i] for i in top_indices]
    top_score = float(scores[top_indices[0]]) if len(top_indices) > 0 else 0.0
    return top_docs, top_score


def get_feature_weights(query: str):
    """Returns the TF-IDF feature weights for the query — for interpretability panel."""
    query_vec = _vectorizer.transform([query])
    feature_names = _vectorizer.get_feature_names_out()
    weights = query_vec.toarray().flatten()
    word_weights = {feature_names[i]: round(float(weights[i]), 4)
                    for i in np.argsort(weights)[::-1][:10] if weights[i] > 0}
    return word_weights