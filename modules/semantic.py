from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(reference_text, user_text):

    model = load_model()

    emb1 = model.encode(reference_text)

    emb2 = model.encode(user_text)

    score = cosine_similarity([emb1], [emb2])[0][0] * 100
    return float(score)