import streamlit as st


def metric_cards():

    # Before analysis
    if "semantic_score" not in st.session_state:

        semantic = 0
        fluency = 0
        confidence = 0
        overall = 0

    else:

        semantic = round(float(st.session_state["semantic_score"]), 1)

        audio = st.session_state.get("audio_metrics", {})

        filler = st.session_state.get("filler_count", 0)

        pause = audio.get("pause_ratio", 0)

        rms = audio.get("rms", 0)

        # Fluency
        fluency = 100
        fluency -= min(pause, 40)
        fluency -= filler * 3
        fluency = max(0, min(100, fluency))

        # Confidence
        confidence = 100
        confidence -= filler * 4
        confidence -= pause * 0.5

        if rms < 0.01:
            confidence -= 10

        confidence = max(0, min(100, confidence))

        # Overall
        overall = round(
            semantic * 0.60 +
            fluency * 0.25 +
            confidence * 0.15,
            1
        )

    cards = [
        ("🧠", "Semantic Score", semantic),
        ("🎙", "Speech Fluency", round(fluency, 1)),
        ("😊", "Confidence", round(confidence, 1)),
        ("🏆", "Overall Score", round(overall, 1)),
    ]

    cols = st.columns(4)

    for col, (icon, title, value) in zip(cols, cards):

        with col:

            st.metric(
                label=f"{icon} {title}",
                value=f"{value}%"
            )