# ==========================================================
# Main Analysis Pipeline
# Purpose:
# Coordinates the complete analysis workflow:
# 1. Normalize logs
# 2. Detect anomalies
# 3. Detect flapping events
# 4. Correlate related events
# 5. Assign severity levels
# 6. Generate timelines
# 7. Create human-readable summaries
# 8. Generate reports
# ==========================================================

from normalizer import load_and_normalize
from flap_detector import detect_flaps
from anomaly_detector import detect_anomalies
from correlator import correlate
from narrator import generate_narrative
from reporter import generate_report
from timeline import generate_timeline
from pdf_reporter import generate_pdf

import json

from colorama import Fore, Style, init

init()


def main():

    # ==========================================
    # Step 1: Load and normalize events
    # ==========================================
    events = load_and_normalize("classified_report.json")
    events = sorted(events, key=lambda x: x["timestamp"])

    print(Fore.CYAN + f"\nTotal events: {len(events)}")

    # ==========================================
    # Step 2: Sample normalized events
    # ==========================================
    print(Fore.BLUE + "\n--- Sample Normalized Events ---")

    for e in events[:5]:
        print(e)

    # ==========================================
    # Step 3: Flap detection
    # ==========================================
    flaps = detect_flaps(events)

    print(Fore.YELLOW + "\n--- Flaps Detected ---")

    if not flaps:
        print("No flaps detected")
    else:
        for f in flaps:
            print(f)

    # ==========================================
    # Step 4: Sample counter data
    # ==========================================
    counter_data = {
        "Ethernet1": [
            {"timestamp": 1, "value": 10},
            {"timestamp": 2, "value": 15},
            {"timestamp": 3, "value": 900},
        ],
        "Ethernet2": [
            {"timestamp": 1, "value": 5},
            {"timestamp": 2, "value": 6},
            {"timestamp": 3, "value": 7},
        ]
    }

    # ==========================================
    # Step 5: Anomaly detection
    # ==========================================
    anomalies = detect_anomalies(counter_data)

    print(Fore.MAGENTA + "\n--- Anomalies Detected ---")

    if not anomalies:
        print("No anomalies detected")
    else:
        for a in anomalies:
            print(a)

    # ==========================================
    # Step 6: Correlation engine
    # ==========================================
    correlations = correlate(events, anomalies)

    print(Fore.RED + "\n--- Correlations ---")

    if not correlations:
        print("No correlations detected")
    else:
        for c in correlations:
            print(c)

    # ==========================================
    # Step 7: Incident narrative
    # ==========================================
    print(Fore.GREEN + "\n--- Incident Narrative ---")

    narrative = generate_narrative(correlations)

    print(narrative)

    # ==========================================
    # Step 8: Generate final report
    # ==========================================
    report = generate_report(
        events,
        flaps,
        anomalies,
        correlations,
        narrative
    )

    # ==========================================
    # Step 9: Save JSON report
    # ==========================================
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4, default=str)

    # Generate PDF report
    generate_pdf(report)
    # ==========================================
    # Step 10: Generate HTML timeline
    # ==========================================
    generate_timeline(events)

    # ==========================================
    # Step 11: Console summary
    # ==========================================
    print(Fore.CYAN + "\n--- Summary ---")

    print(Fore.YELLOW + f"Events: {len(events)}")
    print(Fore.GREEN + f"Flaps: {len(flaps)}")
    print(Fore.MAGENTA + f"Anomalies: {len(anomalies)}")
    print(Fore.RED + f"Correlations: {len(report['incidents'])}")

    print(Style.RESET_ALL)

    print("Report saved to report.json")
    print("Timeline saved to timeline.html")


if __name__ == "__main__":
    main()