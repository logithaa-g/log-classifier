from collections import defaultdict

def detect_flaps(events, threshold=30):
    events = sorted(events, key=lambda x: x["timestamp"])

    port_map = defaultdict(list)
    flaps = []

    for e in events:
        if e["port"]:
            port_map[e["port"]].append(e)

    for port, evs in port_map.items():
        for i in range(len(evs)-1):
            if evs[i]["subtype"] == "DOWN" and evs[i+1]["subtype"] == "UP":
                delta = (evs[i+1]["timestamp"] - evs[i]["timestamp"]).seconds
                if delta <= threshold:
                    flaps.append({
                        "port": port,
                        "duration": delta
                    })

    return flaps