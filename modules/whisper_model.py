import streamlit as st

try:
    import whisper
except Exception:  # pragma: no cover - optional dependency
    whisper = None


def is_whisper_available():
    return whisper is not None


@st.cache_resource
def load_whisper_model():
    if whisper is None:
        return None
    return whisper.load_model("base")


def transcribe_audio(audio_path):
    model = load_whisper_model()

    if model is None:
        raise RuntimeError(
            "Whisper support is not available in this deployment. "
            "Please install the optional speech model dependencies to enable transcription."
        )

    result = model.transcribe(audio_path)

    return result["text"]