def generate_report(events, flaps, anomalies, correlations, narrative):

    # Deduplicate correlations by type (keep first occurrence)
    unique_correlations = {}

    for c in correlations:
        if "type" in c and c["type"] not in unique_correlations:
            unique_correlations[c["type"]] = c

    clean_correlations = list(unique_correlations.values())

    # Smart severity calculation
    severities = [c.get("severity", "").lower() for c in clean_correlations]

    if "critical" in severities:
        overall_severity = "CRITICAL"
    elif "error" in severities:
        overall_severity = "ERROR"
    elif "warning" in severities:
        overall_severity = "WARNING"
    else:
        overall_severity = "INFO"

    # Summary block
    summary = {
        "total_events": len(events),
        "flaps": len(flaps),
        "anomalies": len(anomalies),
        "correlations": len(clean_correlations),
        "overall_severity": overall_severity
    }

    # Incident list
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

    # Final report
    report = {
        "summary": summary,
        "incidents": incidents,
        "flaps": flaps,
        "anomalies": anomalies,
        "narrative": narrative
    }

    return report