# ==========================================================
# Log Normalizer
# Purpose:
# Converts logs from different formats into a standard
# structure for consistent analysis and processing.
# ==========================================================

import json
import re
from datetime import datetime





def parse_details(details):

    port = None
    subtype = None

    # ==========================================
    # Extract port
    # ==========================================
    port_match = re.search(r"(Ethernet\d+)", details)

    if port_match:
        port = port_match.group(1)

    details_lower = details.lower()

    # ==========================================
    # Subtype detection
    # ==========================================
    if "crash" in details_lower:
        subtype = "CRASH"

    elif "starting" in details_lower or "started" in details_lower:
        subtype = "START"

    elif "error" in details_lower:
        subtype = "ERROR"

    elif "down" in details_lower:
        subtype = "DOWN"

    elif "up" in details_lower:
        subtype = "UP"

    return port, subtype


def normalize_event(e):

    # ==========================================
    # Parse port + subtype
    # ==========================================
    port, subtype = parse_details(e["details"])

    # ==========================================
    # Safe timestamp parsing
    # ==========================================
    try:
        timestamp = datetime.strptime(
            e["timestamp"],
            "%Y-%m-%d %H:%M:%S.%f"
        )

    except:
        # Skip invalid timestamps
        return None

    # ==========================================
    # Normalized event
    # ==========================================
    return {
        "timestamp": timestamp,
        "category": e["category"],
        "subtype": subtype,
        "port": port,
        "device": e["host"],
        "raw": e["details"]
    }


def load_and_normalize(path="report.json"):

    # ==========================================
    # Load JSON report
    # ==========================================
    with open(path) as f:
        data = json.load(f)

    seen = set()
    normalized = []

    # ==========================================
    # Normalize events
    # ==========================================
    for e in data:

        key = (
            e["timestamp"],
            e["details"]
        )

        # Remove duplicates
        if key not in seen:

            seen.add(key)

            event = normalize_event(e)

            # Skip invalid events
            if event:
                normalized.append(event)

    return normalized