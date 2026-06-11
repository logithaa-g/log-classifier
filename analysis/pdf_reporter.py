# ==========================================================
# PDF Report Generator
# Purpose:
# Creates professional PDF reports containing
# incident details, severity information,
# timelines, and analysis summaries.
# ==========================================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def generate_pdf(report):

    doc = SimpleDocTemplate(
        "report.pdf",
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==========================================
    # Title
    # ==========================================
    elements.append(
        Paragraph(
            "Log Pattern Classifier Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    # ==========================================
    # Summary
    # ==========================================
    summary = report["summary"]

    elements.append(
        Paragraph(
            f"""
            <b>Total Events:</b> {summary['total_events']}<br/>
            <b>Flaps:</b> {summary['flaps']}<br/>
            <b>Anomalies:</b> {summary['anomalies']}<br/>
            <b>Correlations:</b> {summary['correlations']}<br/>
            <b>Overall Severity:</b> {summary['overall_severity']}
            """,
            styles['BodyText']
        )
    )

    elements.append(Spacer(1, 20))

    # ==========================================
    # Incidents
    # ==========================================
    elements.append(
        Paragraph(
            "Detected Incidents",
            styles['Heading2']
        )
    )

    for incident in report["incidents"]:

        text = f"""
        <b>Type:</b> {incident.get('type')}<br/>
        <b>Severity:</b> {incident.get('severity')}<br/>
        <b>Description:</b> {incident.get('description')}<br/>
        """

        if "port" in incident:
            text += f"<b>Port:</b> {incident['port']}<br/>"

        if "time" in incident:
            text += f"<b>Time:</b> {incident['time']}<br/>"

        elements.append(
            Paragraph(text, styles['BodyText'])
        )

        elements.append(Spacer(1, 12))

    # ==========================================
    # Narrative
    # ==========================================
    elements.append(
        Paragraph(
            "Incident Narrative",
            styles['Heading2']
        )
    )

    narrative = report["narrative"].replace("\n", "<br/>")

    elements.append(
        Paragraph(
            narrative,
            styles['BodyText']
        )
    )

    # ==========================================
    # Build PDF
    # ==========================================
    doc.build(elements)

    print("PDF report saved to report.pdf")