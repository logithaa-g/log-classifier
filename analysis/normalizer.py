import json
import re
from datetime import datetime

CATEGORY_MAP = {
    "Port Error": "link",
    "Switch Initialization": "system",
    "LACP": "lacp",
    "Mastership": "ha",
    "VIP Failure": "vip",
    "Switch Health": "health",
    "SwitchD Crash": "crash"
}

def parse_details(details):
    port = None
    subtype = None

    # Extract port
    port_match = re.search(r"(Ethernet\d+)", details)
    if port_match:
        port = port_match.group(1)

    details_lower = details.lower()

    # Priority-based subtype detection
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
    port, subtype = parse_details(e["details"])

    return {
        "timestamp": datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
        "category": CATEGORY_MAP.get(e["category"], "unknown"),
        "subtype": subtype,
        "port": port,
        "device": e["host"],
        "raw": e["details"]
    }


def load_and_normalize(path="report.json"):
    with open(path) as f:
        data = json.load(f)

    seen = set()
    normalized = []

    for e in data:
        key = (e["timestamp"], e["details"])

        if key not in seen:
            seen.add(key)
            normalized.append(normalize_event(e))

    return normalized