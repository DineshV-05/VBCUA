import os

import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def generate_feedback(
        concept,
        transcript,
        semantic_score,
        filler_count,
        pause_ratio):

    prompt = f"""
You are an AI Communication and Concept Evaluation Assistant.

Evaluate the following spoken explanation.

Concept:
{concept}

Transcript:
{transcript}

Semantic Score:
{semantic_score:.2f}

Filler Words:
{filler_count}

Pause Ratio:
{pause_ratio}

Generate a report with exactly these headings:

Understanding Level

Strengths

Weaknesses

Suggestions for Improvement

Overall Feedback

Keep the response under 200 words.
"""

    if model is None:
        return "Gemini API key is not configured. Please set the GEMINI_API_KEY environment variable."

    response = model.generate_content(prompt)

    return response.text