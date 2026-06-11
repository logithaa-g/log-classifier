# ==========================================================
# Event Correlator
# Purpose:
# Groups related log events together to identify the
# root cause of an incident and reduce alert noise.
# ==========================================================

from datetime import timedelta

def correlate(events, anomalies, window_seconds=60):
    correlations = []
    used_times = set()  # prevents duplicate detections

    # Ensure events are sorted
    events = sorted(events, key=lambda x: x["timestamp"])

    # =====================================================
    # RULE 1 & RULE 2 → Event-based Correlations
    # =====================================================
    for i in range(len(events)):
        base = events[i]

        # Skip if already used in correlation
        if base["timestamp"] in used_times:
            continue

        # Build time window
        window_events = []
        for j in range(i + 1, len(events)):
            delta = (events[j]["timestamp"] - base["timestamp"]).total_seconds()

            if delta > window_seconds:
                break

            window_events.append(events[j])

        # ---------------------------
        # RULE 1: ERROR → DOWN → START
        # ---------------------------
        if base["subtype"] == "ERROR":
            has_down = any(e["subtype"] == "DOWN" for e in window_events)
            has_start = any(e["subtype"] == "START" for e in window_events)

            if has_down and has_start:
                correlations.append({
                    "type": "link_instability",
                    "root_cause": "Port error leading to restart",
                    "time": str(base["timestamp"]),
                    "severity": "critical"
                })
                used_times.add(base["timestamp"])
                continue

        # ---------------------------
        # RULE 2: MULTIPLE PORTS DOWN
        # ---------------------------
        if base["subtype"] == "DOWN":
            down_events = [
                e for e in window_events if e["subtype"] == "DOWN"
            ]

            if len(down_events) >= 3:
                correlations.append({
                    "type": "multi_port_failure",
                    "root_cause": "Possible switch reset or fabric issue",
                    "time": str(base["timestamp"]),
                    "severity": "critical"
                })
                used_times.add(base["timestamp"])

    # =====================================================
    # RULE 3 → Anomaly-based Correlation
    # =====================================================
    for anomaly in anomalies:
        for e in events:
            if (
                e["port"] == anomaly["port"] and
                e["subtype"] == "DOWN"
            ):
                correlations.append({
                    "type": "congestion_failure",
                    "root_cause": "High packet loss leading to link failure",
                    "port": anomaly["port"],
                    "severity": "critical"
                })
                break  # avoid duplicate per anomaly

    return correlations