import subprocess
import os
import json


def test_pipeline():

    subprocess.run([
        "python",
        "-m",
        "log_classifier",
        "--input",
        "sample.log",
        "--output",
        "test_report.json"
    ])

    assert os.path.exists("test_report.json")

    with open("test_report.json", "r") as f:
        data = json.load(f)

    assert len(data) > 0


def test_category_filter():

    subprocess.run([
        "python",
        "-m",
        "log_classifier",
        "--input",
        "sample.log",
        "--categories",
        "link_flap",
        "--output",
        "category_report.json"
    ])

    with open("category_report.json", "r") as f:
        data = json.load(f)

    assert len(data) > 0

    for event in data:
        assert event["category"] == "Link Flap"


def test_severity_filter():

    subprocess.run([
        "python",
        "-m",
        "log_classifier",
        "--input",
        "sample.log",
        "--severity",
        "critical",
        "--output",
        "severity_report.json"
    ])

    with open("severity_report.json", "r") as f:
        data = json.load(f)

    assert len(data) > 0

    for event in data:
        assert event["severity"] == "critical"