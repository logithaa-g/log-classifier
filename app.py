from collections import Counter
import json
import os
import subprocess
import tempfile
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded_files = request.files.getlist("logfile")
    pasted_logs = request.form.get("logtext")

    # ==========================================
    # Validation
    # ==========================================
    if (not uploaded_files or uploaded_files[0].filename == "") and not pasted_logs:
        return "Please upload a file or paste logs."

    temp_dir = tempfile.gettempdir()
    all_results = []

    # ==========================================
    # Multiple uploaded files
    # ==========================================
    if uploaded_files and uploaded_files[0].filename != "":
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            uploaded_file.save(file_path)

            output_path = os.path.join(
                temp_dir, f"{uploaded_file.filename}_report.json"
            )

            subprocess.run(
                [
                    "python",
                    "-m",
                    "log_classifier",
                    "--input",
                    file_path,
                    "--output",
                    output_path,
                ]
            )

            if os.path.exists(output_path):
                with open(output_path, "r", encoding="utf-8") as f:
                    file_results = json.load(f)
                all_results.extend(file_results)

    # ==========================================
    # Pasted logs
    # ==========================================
    elif pasted_logs:
        input_path = os.path.join(temp_dir, "pasted_logs.log")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(pasted_logs)

        output_path = os.path.join(temp_dir, "pasted_report.json")

        subprocess.run(
            [
                "python",
                "-m",
                "log_classifier",
                "--input",
                input_path,
                "--output",
                output_path,
            ]
        )

        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                all_results = json.load(f)

    results = all_results

    # ==========================================
    # Dashboard stats
    # ==========================================
    total_events = len(results)

    severity_counts = Counter(
        event.get("severity", "info") for event in results
    )
    category_counts = Counter(
        event.get("category", "Unknown") for event in results
    )

    critical_count = severity_counts.get("critical", 0)
    error_count = severity_counts.get("error", 0)
    warning_count = severity_counts.get("warning", 0)
    info_count = severity_counts.get("info", 0)

    # ==========================================
    # Smart Summary
    # ==========================================
    flaps = len(
        [
            r
            for r in results
            if "flap" in r.get("category", "").lower()
        ]
    )
    anomalies = len(
        [
            r
            for r in results
            if r.get("severity") in ["critical", "error"]
        ]
    )

    correlations = 0
    incidents = []
    narratives = []

    # ==========================================
    # Incident Detection
    # ==========================================
    for event in results:
        category = event.get("category", "").lower()
        details = event.get("details", "")
        timestamp = event.get("timestamp", "")

        if "switchd crash" in category:
            correlations += 1
            incidents.append(
                {
                    "type": "switchd_failure",
                    "severity": "critical",
                    "description": "Possible switch reset or daemon crash.",
                    "time": timestamp,
                }
            )
            narratives.append(
                "Switch daemon crashed unexpectedly. This may indicate switch instability or software failure."
            )

        elif "link flap" in category:
            correlations += 1
            incidents.append(
                {
                    "type": "link_instability",
                    "severity": "critical",
                    "description": "Port instability detected.",
                    "time": timestamp,
                }
            )
            narratives.append(
                "Repeated link state changes suggest network instability or hardware issues."
            )

        elif "port error" in category:
            correlations += 1
            incidents.append(
                {
                    "type": "congestion_failure",
                    "severity": "critical",
                    "description": "Port error leading to failure.",
                    "time": timestamp,
                    "port": details,
                }
            )
            narratives.append(
                "Port errors detected leading to congestion or packet loss."
            )

    # ==========================================
    # Overall Severity
    # ==========================================
    if critical_count > 0:
        overall_severity = "CRITICAL"
    elif error_count > 0:
        overall_severity = "ERROR"
    elif warning_count > 0:
        overall_severity = "WARNING"
    else:
        overall_severity = "INFO"

    # ==========================================
    # Timeline Data Compilation
    # ==========================================
    timeline_labels = []
    timeline_values = []
    severity_map = {"info": 1, "warning": 2, "error": 3, "critical": 4}

    for event in results:
        timestamp = event.get("timestamp", "Unknown")
        severity = event.get("severity", "info").lower()

        timeline_labels.append(timestamp)
        timeline_values.append(severity_map.get(severity, 1))

    # ==========================================
    # OUTPUT FILTERING
    # Only filter if checkboxes were actually submitted from the form.
    # Without this guard, selected_outputs is always [] and wipes everything.
    # ==========================================
    selected_outputs = request.form.getlist("outputs")

    if selected_outputs:
        if "timeline" not in selected_outputs:
            timeline_labels = []
            timeline_values = []

        if "incident" not in selected_outputs:
            incidents = []
            narratives = []

        if "severity" not in selected_outputs:
            critical_count = 0
            error_count = 0
            warning_count = 0
            info_count = 0

    print("TIMELINE LABELS:", timeline_labels)
    print("TIMELINE VALUES:", timeline_values)

    return render_template(
        "result.html",
        results=results,
        total_events=total_events,
        critical_count=critical_count,
        error_count=error_count,
        warning_count=warning_count,
        info_count=info_count,
        category_counts=category_counts,
        flaps=flaps,
        anomalies=anomalies,
        correlations=correlations,
        overall_severity=overall_severity,
        incidents=incidents,
        narratives=narratives,
        timeline_labels=timeline_labels,
        timeline_values=timeline_values,
    )


if __name__ == "__main__":
    app.run(debug=True)