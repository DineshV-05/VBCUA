from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(
    concept,
    transcript,
    semantic_score,
    duration,
    pause_ratio,
    filler_count,
    overall_score,
    feedback
):

    os.makedirs("reports", exist_ok=True)

    pdf_path = os.path.join(
        "reports",
        "analysis_report.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>Voice-Based Concept Understanding Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"<b>Concept:</b> {concept}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Transcript:</b> {transcript}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Semantic Score:</b> {semantic_score:.2f}%", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Duration:</b> {duration} sec", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Pause Ratio:</b> {pause_ratio}%", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Filler Words:</b> {filler_count}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Overall Score:</b> {overall_score:.2f}%", styles["Normal"])
    )

    story.append(
        Paragraph("<b>AI Feedback</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(feedback.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(story)

    return pdf_path