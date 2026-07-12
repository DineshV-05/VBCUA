import streamlit as st

# Components
from components.hero import hero
from components.cards import metric_cards
from components.uploader import uploader
from components.footer import footer
from components.gauge import create_gauge

# Modules
from modules.audio_utils import save_uploaded_file
from modules.reference_loader import load_reference
from modules.concept_checker import check_missing_concepts
from modules.filler_detection import detect_fillers
from modules.pdf_report import generate_pdf
from modules.whisper_model import is_whisper_available
from modules.semantic import is_sentence_transformers_available
from modules.gemini_feedback import is_gemini_available


def home():

    # -------------------------------------------------
    # Hero Section
    # -------------------------------------------------

    hero()

    st.markdown("---")
    st.markdown(
        "#### Deployment status: Render-friendly mode — optional AI features are detected dynamically."
    )
    st.write("")

    # -------------------------------------------------
    # Live Dashboard Cards
    # -------------------------------------------------

    # -------------------------------------------------
    # Live Dashboard Cards
    # -------------------------------------------------

    if "semantic_score" in st.session_state:

        semantic = float(st.session_state["semantic_score"])

        metrics = st.session_state["audio_metrics"]

        filler_count = st.session_state["filler_count"]

        fluency = max(0, 100 - metrics["pause_ratio"] - filler_count * 2)

        confidence = max(0, 100 - metrics["pause_ratio"] / 2)

        overall = round((semantic + fluency + confidence) / 3, 2)

        metric_cards()

    else:

        metric_cards()

    st.write("")


    # -------------------------------------------------
    # Upload Section
    # -------------------------------------------------

    concept, audio = uploader()

    if audio:

        st.success("✅ Audio Uploaded Successfully")

        st.audio(audio)

    st.write("")

    whisper_ready = is_whisper_available()
    semantic_ready = is_sentence_transformers_available()
    gemini_ready = is_gemini_available()

    if not whisper_ready:
        st.warning(
            "Whisper transcription is unavailable in this deployment. "
            "The analysis button is disabled until the optional dependency is installed."
        )

    if not semantic_ready:
        st.info(
            "Semantic similarity is using a lightweight fallback instead of SentenceTransformers. "
            "Results may be less precise."
        )

    if not gemini_ready:
        st.info(
            "Gemini feedback is unavailable because the Gemini API dependency or key is missing. "
            "Feedback will show a placeholder message."
        )

    button_disabled = not whisper_ready
    if st.button(
        "🚀 Analyze Explanation",
        use_container_width=True,
        disabled=button_disabled
    ):

        if audio is None:

            st.warning("⚠ Please upload an audio file.")

        else:

            with st.spinner("🤖 AI is analyzing your explanation..."):

                try:
                    from modules.audio_analysis import analyze_audio
                    from modules.gemini_feedback import generate_feedback
                    from modules.semantic import semantic_similarity
                    from modules.whisper_model import transcribe_audio
                    from modules.waveform import plot_waveform

                    # ------------------------------------
                    # Save Audio
                    # ------------------------------------

                    audio_path = save_uploaded_file(audio)

                    st.session_state["audio_path"] = audio_path

                    # ------------------------------------
                    # Whisper
                    # ------------------------------------

                    transcript = transcribe_audio(audio_path)

                    st.session_state["transcript"] = transcript

                    st.session_state["concept"] = concept

                    # ------------------------------------
                    # Reference Concept
                    # ------------------------------------

                    reference = load_reference(concept)

                    # ------------------------------------
                    # Semantic Similarity
                    # ------------------------------------

                    semantic_score = semantic_similarity(
                        reference,
                        transcript
                    )

                    st.session_state["semantic_score"] = float(semantic_score)

                    # ------------------------------------
                    # Audio Analysis
                    # ------------------------------------

                    audio_metrics = analyze_audio(audio_path)

                    st.session_state["audio_metrics"] = audio_metrics

                    # ------------------------------------
                    # Filler Detection
                    # ------------------------------------

                    filler_count, filler_words = detect_fillers(transcript)

                    st.session_state["filler_count"] = filler_count
                    st.session_state["filler_words"] = filler_words

                    feedback = generate_feedback(

                        concept,

                        transcript,

                        semantic_score,

                        filler_count,

                        audio_metrics["pause_ratio"]

                    )

                    pause = audio_metrics["pause_ratio"]
                    rms = audio_metrics["rms"]

                    # Fluency
                    fluency = 100
                    fluency -= min(pause, 40)
                    fluency -= filler_count * 3
                    fluency = max(0, min(100, fluency))

                    # Confidence
                    confidence = 100
                    confidence -= filler_count * 4
                    confidence -= pause * 0.5

                    if rms < 0.01:
                        confidence -= 10

                    confidence = max(0, min(100, confidence))

                    overall = (
                        semantic_score * 0.60 +
                        fluency * 0.25 +
                        confidence * 0.15
                    )

                    overall = round(overall, 2)

                    

                    st.session_state["ai_feedback"] = feedback

                    found, missing = check_missing_concepts(
                        concept,
                        transcript
                    )

                    st.session_state["found_concepts"] = found
                    st.session_state["missing_concepts"] = missing

                    st.success("✅ AI Analysis Completed!")

                    st.rerun()

                except Exception as e:

                    st.error("❌ ERROR OCCURRED")

                    st.exception(e)

    st.write("")

    # -------------------------------------------------
    # Tabs
    # -------------------------------------------------

    tab0 ,tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Dashboard",
            "📄 Transcript",
            "📈 Audio Analysis",
            "🤖 AI Feedback",
            "📥 PDF Report"
        ]
    )

    # ==========================================================
    # Transcript
    # ==========================================================
    with tab0:

        if "semantic_score" in st.session_state:

            semantic = float(st.session_state["semantic_score"])

            metrics = st.session_state["audio_metrics"]

            filler = st.session_state.get("filler_count", 0)

            pause = metrics["pause_ratio"]

            rms = metrics["rms"]

            fluency = 100

            fluency -= min(pause, 40)

            fluency -= filler * 3

            fluency = max(0, min(100, fluency))

            confidence = 100

            confidence -= filler * 4

            confidence -= pause * 0.5

            if rms < 0.01:
                confidence -= 10

            confidence = max(0, min(100, confidence))

            overall = (
                semantic * 0.60 +
                fluency * 0.25 +
                confidence * 0.15
            )

            overall = round(overall, 2)

            c1, c2 = st.columns(2)

            with c1:

                st.plotly_chart(
                    create_gauge(
                        "Semantic Score",
                        semantic
                    ),
                    use_container_width=True
                )

            with c2:

                st.plotly_chart(
                    create_gauge(
                        "Speech Fluency",
                        fluency
                    ),
                    use_container_width=True
                )

            c3, c4 = st.columns(2)

            with c3:

                st.plotly_chart(
                    create_gauge(
                        "Confidence",
                        confidence
                    ),
                    use_container_width=True
               )

            with c4:

                st.plotly_chart(

                    create_gauge(

                        "Overall Score",

                        overall

                    ),

                    use_container_width=True

                )

# ==================================================
# Overall Assessment
# ==================================================

            st.markdown("---")

            if overall >= 85:

                st.success("""
                ## 🌟 Overall Assessment

                Excellent conceptual understanding.

                Your explanation is technically strong and well structured.
                """)

            elif overall >= 70:

                st.warning("""
            ## 👍 Overall Assessment

            Good understanding.

            Try including more technical terms and practical examples.
            """)

            else:

                st.error("""
            ## 📘 Overall Assessment

             Basic understanding.

            Review the concept and explain the important keywords in more detail.
            """)

           
    with tab1:

        if "transcript" in st.session_state:

            st.subheader("📝 Transcript")

            st.write(st.session_state["transcript"])

        else:

            st.info("Transcript will appear here.")

    # ==========================================================
    # Audio Analysis
    # ==========================================================

    with tab2:

        if "audio_metrics" in st.session_state:

            metrics = st.session_state["audio_metrics"]

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "🎤 Duration",
                    f"{metrics['duration']} sec"
                )

            with c2:

                st.metric(
                    "🔊 RMS Energy",
                    metrics["rms"]
                )

            with c3:

                st.metric(
                    "⏸ Pause Ratio",
                    f"{metrics['pause_ratio']}%"
                )

            st.write("---")

            st.subheader("📈 Audio Waveform")

            figure = plot_waveform(
                st.session_state["audio_path"]
            )

            st.pyplot(figure)

        else:

            st.info("Analyze an audio file first.")

    # ==========================================================
    # AI Feedback
    # ==========================================================

    with tab3:

        if "semantic_score" in st.session_state:

            score = float(st.session_state["semantic_score"])

            st.metric(
                "🧠 Semantic Similarity",
                f"{score:.2f}%"
            )

            st.progress(score / 100)

            st.write("")

            

            st.subheader("🤖 AI Generated Feedback")

            

            if "ai_feedback" in st.session_state:
                st.write(st.session_state["ai_feedback"])
            else:
                st.warning("AI feedback is not available.")

            # ==========================================
            # Concepts Identified
              # ==========================================

            st.write("---")

            st.subheader("✅ Concepts Identified")

            found = st.session_state.get("found_concepts", [])

            if found:

                for concept in found:

                    st.success(f"✔ {concept}")

            else:

                st.warning("No expected concepts were identified.")

# ==========================================
# Missing Concepts
# ==========================================

            st.write("---")

            st.subheader("❌ Missing Concepts")

            missing = st.session_state.get("missing_concepts", [])

            if missing:

                for concept in missing:

                    st.error(f"✖ {concept}")

            else:

                st.success("🎉 Great! No important concepts are missing.")

            st.write("---")

            st.subheader("💬 Filler Word Analysis")

            filler_count = st.session_state.get(
                "filler_count",
                0
            )

            filler_words = st.session_state.get(
                "filler_words",
                {}
            )

            st.metric(
                "Total Fillers",
                filler_count
            )

            if filler_words:

                st.json(filler_words)

            else:

                st.success("🎉 No filler words detected!")

        else:

            st.info("AI feedback will appear after analysis.")

    # ==========================================================
    # PDF Report
    # ==========================================================

    with tab4:
            if "semantic_score" in st.session_state:

                semantic = float(st.session_state["semantic_score"])

                metrics = st.session_state["audio_metrics"]

                filler_count = st.session_state.get("filler_count", 0)

                pause = metrics["pause_ratio"]

                rms = metrics["rms"]

                # Fluency Score
                fluency = 100
                fluency -= min(pause, 40)
                fluency -= filler_count * 3
                fluency = max(0, min(100, fluency))

                # Confidence Score
                confidence = 100
                confidence -= filler_count * 4
                confidence -= pause * 0.5

                if rms < 0.01:
                    confidence -= 10

                confidence = max(0, min(100, confidence))

        # Overall Score
                overall = (
                    semantic * 0.60 +
                    fluency * 0.25 +
                    confidence * 0.15
               )

                overall = round(overall, 2)

                if st.button("📄 Generate PDF Report"):

                    pdf_path = generate_pdf(

                        concept=st.session_state["concept"],

                        transcript=st.session_state["transcript"],

                        semantic_score=semantic,

                        duration=metrics["duration"],

                        pause_ratio=metrics["pause_ratio"],

                        filler_count=filler_count,

                        

            

                        overall_score=overall,

                    

                        feedback=st.session_state["ai_feedback"]

                    )

                    st.success("✅ PDF Generated Successfully!")

                    with open(pdf_path, "rb") as pdf:

                        st.download_button(

                            "⬇ Download PDF",

                            pdf,

                            file_name="Voice_Report.pdf",

                            mime="application/pdf",

                            use_container_width=True

                        )

            else:

                st.info("Analyze an audio file first.")
       

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    footer()