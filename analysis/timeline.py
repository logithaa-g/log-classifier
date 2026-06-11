# ==========================================================
# Timeline Generator
# Purpose:
# Organizes events chronologically to help understand
# the sequence of actions leading to an incident.
# ==========================================================

import pandas as pd
import plotly.express as px


def generate_timeline(events):

    if not events:
        print("No events available for timeline.")
        return

    # Convert events into dataframe
    data = []

    for e in events:

        data.append({
            "timestamp": str(e.get("timestamp")),
            "category": e.get("category"),
            "subtype": e.get("subtype"),
            "device": e.get("device"),
            "port": e.get("port")
        })

    df = pd.DataFrame(data)

    # Create interactive timeline
    fig = px.scatter(
        df,
        x="timestamp",
        y="category",
        color="category",
        hover_data=["subtype", "device", "port"],
        title="Log Event Timeline"
    )

    # Save HTML
    fig.write_html("timeline.html")

    print("Timeline saved to timeline.html")