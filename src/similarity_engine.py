"""Text similarity engine supporting TF-IDF cosine similarity and optional SBERT."""

from typing import Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.text_preprocessor import clean_text_for_similarity

# Global cache for SBERT model
_sbert_model = None
_sbert_available = None


def is_sbert_available() -> bool:
    """Check if sentence-transformers is installed in the current environment."""
    global _sbert_available
    if _sbert_available is None:
        try:
            import sentence_transformers  # noqa: F401
            _sbert_available = True
        except ImportError:
            _sbert_available = False
    return _sbert_available


def get_sbert_model():
    """Load SBERT model locally on CPU if available."""
    global _sbert_model
    if _sbert_model is None and is_sbert_available():
        try:
            from sentence_transformers import SentenceTransformer
            # Lightweight, high-speed model
            _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _sbert_model = None
    return _sbert_model


def compute_tfidf_similarity(jd_text: str, resume_text: str) -> float:
    """Calculate Cosine Similarity between Job Description and Resume using TF-IDF.
    
    Returns a score from 0.0 to 100.0.
    """
    if not jd_text or not resume_text:
        return 0.0

    clean_jd = clean_text_for_similarity(jd_text)
    clean_resume = clean_text_for_similarity(resume_text)

    if not clean_jd or not clean_resume:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        tfidf_matrix = vectorizer.fit_transform([clean_jd, clean_resume])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(sim_matrix[0][0]) * 100.0
        return round(max(0.0, min(100.0, score)), 2)
    except Exception:
        return 0.0


def compute_sbert_similarity(jd_text: str, resume_text: str) -> Tuple[float, bool]:
    """Calculate semantic similarity using SBERT embeddings if available.
    
    Returns (score, success_flag). If SBERT is not available, falls back to TF-IDF.
    """
    model = get_sbert_model()
    if model is None:
        # Fallback to TF-IDF
        return compute_tfidf_similarity(jd_text, resume_text), False

    try:
        # Truncate to reasonable token limits
        jd_input = jd_text[:3000]
        resume_input = resume_text[:3000]

        embeddings = model.encode([jd_input, resume_input], convert_to_numpy=True)
        vec_jd = embeddings[0].reshape(1, -1)
        vec_res = embeddings[1].reshape(1, -1)

        sim = float(cosine_similarity(vec_jd, vec_res)[0][0]) * 100.0
        return round(max(0.0, min(100.0, sim)), 2), True
    except Exception:
        return compute_tfidf_similarity(jd_text, resume_text), False


def compute_similarity(jd_text: str, resume_text: str, method: str = "TF-IDF") -> Dict[str, Any]:
    """Unified entry point to calculate similarity based on configured method.
    
    Methods: 'TF-IDF', 'SBERT', 'Hybrid'
    """
    method = method.upper()
    tfidf_score = compute_tfidf_similarity(jd_text, resume_text)

    if method == "SBERT":
        sbert_score, used_sbert = compute_sbert_similarity(jd_text, resume_text)
        if used_sbert:
            return {
                "score": sbert_score,
                "method_used": "SBERT (Sentence-BERT)",
                "tfidf_score": tfidf_score,
                "sbert_score": sbert_score
            }
        else:
            return {
                "score": tfidf_score,
                "method_used": "TF-IDF (SBERT unavailable, fallen back)",
                "tfidf_score": tfidf_score,
                "sbert_score": None
            }
    elif method == "HYBRID":
        sbert_score, used_sbert = compute_sbert_similarity(jd_text, resume_text)
        if used_sbert:
            hybrid_score = round(0.5 * tfidf_score + 0.5 * sbert_score, 2)
            return {
                "score": hybrid_score,
                "method_used": "Hybrid (50% TF-IDF + 50% SBERT)",
                "tfidf_score": tfidf_score,
                "sbert_score": sbert_score
            }
        else:
            return {
                "score": tfidf_score,
                "method_used": "TF-IDF (Hybrid fallback)",
                "tfidf_score": tfidf_score,
                "sbert_score": None
            }
    else:
        # Default TF-IDF
        return {
            "score": tfidf_score,
            "method_used": "TF-IDF + Cosine Similarity",
            "tfidf_score": tfidf_score,
            "sbert_score": None
        }
