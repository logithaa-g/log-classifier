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

    parser = argparse.ArgumentParser(description="Log Pattern Classifier")

    parser.add_argument(
        "--input",
        required=True,
        help="Input log file pattern (*.log or *.zst)"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON report"
    )

    parser.add_argument(
        "--filter-category",
        help="Filter by category"
    )

    parser.add_argument(
        "--severity",
        help="Filter by severity"
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
    # Optional category filtering
    # ==========================================
    if args.filter_category:

        results = [
            r for r in results
            if r.get("category") == args.filter_category
        ]

    # ==========================================
    # Optional severity filtering
    # ==========================================
    if args.severity:

        results = [
            r for r in results
            if r.get("severity", "").lower() == args.severity.lower()
        ]

    # ==========================================
    # Write final output
    # ==========================================
    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)

    # ==========================================
    # Console summary
    # ==========================================
    print("\n===================================")
    print("Log Classification Complete")
    print("===================================")

    print(f"Files processed: {len(files)}")
    print(f"Total classified events: {len(results)}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()