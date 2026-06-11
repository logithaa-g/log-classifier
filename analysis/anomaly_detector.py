# ==========================================================
# Anomaly Detector
# Purpose:
# Identifies unusual or unexpected patterns in network logs.
# Compares event frequency and behavior against expected
# thresholds to detect potential incidents or attacks.
# ==========================================================

def detect_anomalies(counter_data, threshold=500):
    anomalies = []

    for port, samples in counter_data.items():
        for i in range(1, len(samples)):
            prev = samples[i-1]["value"]
            curr = samples[i]["value"]
            delta = curr - prev

            if delta > threshold:
                anomalies.append({
                    "port": port,
                    "previous": prev,
                    "current": curr,
                    "delta": delta,
                    "severity": "error"
                })

    return anomalies