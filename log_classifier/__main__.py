# ==========================================================
# Main Analysis Pipeline
# Purpose:
# Coordinates the complete analysis workflow:
# 1. Normalize logs
# 2. Detect anomalies
# 3. Detect flapping events
# 4. Correlate related events
# 5. Assign severity levels
# 6. Generate timelines
# 7. Create human-readable summaries
# 8. Generate reports
# ==========================================================


import argparse
import json
import glob

from parser.decompressor import read_log_lines
from parser.line_parser import parse_line

# import all classifiers
from classifiers.switchd_crash import SwitchDCrashClassifier
from classifiers.vip_failure import VIPFailureClassifier
from classifiers.port_errors import PortErrorClassifier
from classifiers.switch_init import SwitchInitClassifier
from classifiers.switch_health import SwitchHealthClassifier
from classifiers.lacp import LACPClassifier
from classifiers.mastership import MastershipClassifier
from classifiers.admin_net import AdminNetClassifier
from classifiers.link_flap import LinkFlapClassifier


def main():

    parser = argparse.ArgumentParser(
        description="Log Pattern Classifier"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input log file pattern (*.log or *.zst)"
    )

    parser.add_argument(
        "--output",
        default="report.json",
        help="Output report file"
    )

    parser.add_argument(
        "--categories",
        "--filter-category",
        dest="categories",
        help="Filter categories (comma separated)"
    )

    parser.add_argument(
        "--severity",
        help="Filter severity levels (comma separated)"
    )

    parser.add_argument(
        "--format",
        default="json",
        help="Output format: json,text"
    )

    args = parser.parse_args()

    # ==========================================
    # Initialize classifiers
    # ==========================================
    classifiers = [
        SwitchDCrashClassifier(),
        VIPFailureClassifier(),
        PortErrorClassifier(),
        SwitchInitClassifier(),
        SwitchHealthClassifier(),
        LACPClassifier(),
        MastershipClassifier(),
        AdminNetClassifier(),
        LinkFlapClassifier()
    ]

    # ==========================================
    # Multi-file support
    # ==========================================
    files = glob.glob(args.input)

    if not files:
        print("No matching input files found.")
        return

    results = []

    # ==========================================
    # Process all files
    # ==========================================
    for file in files:

        print(f"\nProcessing: {file}")

        for line in read_log_lines(file):

            event = parse_line(line)

            for classifier in classifiers:

                result = classifier.match(event)

                if result:

                    # ==========================================
                    # Default severity assignment
                    # ==========================================
                    if "severity" not in result:

                        if result["category"] in [
                            "SwitchD Crash",
                            "VIP Failure"
                        ]:
                            result["severity"] = "critical"

                        elif result["category"] in [
                            "Port Error",
                            "LACP"
                        ]:
                            result["severity"] = "error"

                        elif result["category"] in [
                            "Mastership",
                            "Switch Health"
                        ]:
                            result["severity"] = "warning"

                        else:
                            result["severity"] = "info"

                    results.append(result)

    # ==========================================
    # Category filtering
    # ==========================================
    if args.categories:

        selected_categories = [
            c.strip().lower().replace("_", " ")
            for c in args.categories.split(",")
        ]

        results = [
            r for r in results
            if r.get("category", "").lower()
            in selected_categories
        ]
    # ==========================================
    # Severity filtering
    # ==========================================
    if args.severity:

        selected_severity = [
            s.strip().lower()
            for s in args.severity.split(",")
        ]

        results = [
            r for r in results
            if r.get("severity", "").lower()
            in selected_severity
        ]

    # ==========================================
    # JSON Output
    # ==========================================
    if "json" in args.format.lower():

        with open(args.output, "w") as f:
            json.dump(results, f, indent=4)

    # ==========================================
    # Text Output
    # ==========================================
    if "text" in args.format.lower():

        print("\n========== Classified Events ==========")

        for result in results:
            print(
                f"[{result.get('severity', 'unknown').upper()}] "
                f"{result.get('category')} -> "
                f"{result}"
            )

    # ==========================================
    # Console summary
    # ==========================================
    print("\n===================================")
    print("LOG CLASSIFICATION SUMMARY")
    print("===================================")

    print(f"Files Processed      : {len(files)}")
    print(f"Total Events         : {len(results)}")

    critical = len([
        r for r in results
        if r.get("severity") == "critical"
    ])

    error = len([
        r for r in results
        if r.get("severity") == "error"
    ])

    warning = len([
        r for r in results
        if r.get("severity") == "warning"
    ])

    info = len([
        r for r in results
        if r.get("severity") == "info"
    ])

    print(f"Critical Events      : {critical}")
    print(f"Error Events         : {error}")
    print(f"Warning Events       : {warning}")
    print(f"Info Events          : {info}")

    print(f"\nReport Saved To      : {args.output}")


if __name__ == "__main__":
    main()