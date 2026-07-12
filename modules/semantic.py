import re

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def is_sentence_transformers_available():
    try:
        import sentence_transformers  # noqa: F401
        return True
    except Exception:
        return False


@st.cache_resource
def load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return None


def _fallback_similarity(reference_text, user_text):
    tokenizer = lambda text: re.findall(r"\w+", text.lower())
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, lowercase=False, ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([reference_text, user_text])
    return float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)


def semantic_similarity(reference_text, user_text):
    model = load_model()

    if model is None:
        return _fallback_similarity(reference_text, user_text)

    emb1 = model.encode(reference_text)
    emb2 = model.encode(user_text)

    score = cosine_similarity([emb1], [emb2])[0][0] * 100
    return float(score)