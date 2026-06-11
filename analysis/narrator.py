# ==========================================================
# Incident Narrator
# Purpose:
# Converts technical log analysis results into
# human-readable explanations and summaries.
# ==========================================================

def generate_narrative(correlations):
    if not correlations:
        return "No major incidents detected."

    narrative = []
    seen_types = set()  # remove duplicates

    narrative.append("=== Incident Summary ===\n")

    count = 1

    for c in correlations:
        ctype = c["type"]

        # Skip duplicate incident types
        if ctype in seen_types:
            continue

        seen_types.add(ctype)

        if ctype == "multi_port_failure":
            narrative.append(
                f"{count}. Multiple ports went down simultaneously. "
                f"This indicates a possible switch reset or fabric issue."
            )

        elif ctype == "link_instability":
            narrative.append(
                f"{count}. A port error was followed by link failure and system restart. "
                f"This suggests link instability."
            )

        elif ctype == "congestion_failure":
            narrative.append(
                f"{count}. High packet loss detected on {c.get('port')} leading to link failure. "
                f"This indicates congestion-related issues."
            )

        count += 1

    narrative.append("\nOverall Severity: CRITICAL")

    return "\n".join(narrative)