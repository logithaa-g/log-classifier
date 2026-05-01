from normalizer import load_and_normalize
from flap_detector import detect_flaps
from anomaly_detector import detect_anomalies
from correlator import correlate
from narrator import generate_narrative
import json
from datetime import datetime


def main():
    # Step 1: Load and normalize events
    events = load_and_normalize()
    events = sorted(events, key=lambda x: x["timestamp"])

    print("Total events:", len(events))

    # Step 2: Sample check
    print("\n--- Sample Normalized Events ---")
    for e in events[:5]:
        print(e)

    # Step 3: Flap detection
    flaps = detect_flaps(events)

    print("\n--- Flaps Detected ---")
    for f in flaps:
        print(f) if flaps else print("No flaps detected")

    # Step 4: Sample counter data
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

    # Step 5: Anomaly detection
    anomalies = detect_anomalies(counter_data)

    print("\n--- Anomalies Detected ---")
    for a in anomalies:
        print(a) if anomalies else print("No anomalies detected")

    # Step 6: Correlation
    correlations = correlate(events, anomalies)

    print("\n--- Correlations ---")
    for c in correlations:
        print(c) if correlations else print("No correlations detected")

    # Step 7: Narrative
    print("\n--- Incident Narrative ---")
    narrative = generate_narrative(correlations)
    print(narrative)

    # Step 8: Deduplicate (KEEP FIRST OCCURRENCE)
    unique_correlations = {}
    for c in correlations:
        if "type" in c and c["type"] not in unique_correlations:
            unique_correlations[c["type"]] = c

    clean_correlations = list(unique_correlations.values())

    # Step 9: Smart severity
    severities = [c.get("severity", "").lower() for c in clean_correlations]

    if "critical" in severities:
        overall_severity = "CRITICAL"
    elif "error" in severities:
        overall_severity = "ERROR"
    elif "warning" in severities:
        overall_severity = "WARNING"
    else:
        overall_severity = "INFO"

    # Step 10: Summary
    summary = {
        "total_events": len(events),
        "flaps": len(flaps),
        "anomalies": len(anomalies),
        "correlations": len(clean_correlations),
        "overall_severity": overall_severity
    }

    # Step 11: Incidents with confidence
    incidents = []
    for c in clean_correlations:
        incident = {
            "type": c.get("type"),
            "severity": c.get("severity"),
            "description": c.get("root_cause"),
            "confidence": 0.9
        }

        if "port" in c:
            incident["port"] = c["port"]

        if "time" in c:
            incident["time"] = c["time"]

        incidents.append(incident)

    # Step 12: Final JSON
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "summary": summary,
        "incidents": incidents,
        "flaps": flaps,
        "anomalies": anomalies,
        "narrative": narrative
    }

    with open("analysis_output.json", "w") as f:
        json.dump(output_data, f, indent=4, default=str)

    print("\n--- Summary ---")
    print(f"Events: {len(events)} | Flaps: {len(flaps)} | Anomalies: {len(anomalies)} | Correlations: {len(clean_correlations)}")

    print("\n✅ Analysis saved to analysis_output.json")


if __name__ == "__main__":
    main()