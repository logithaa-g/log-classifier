import argparse
import json
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
    parser.add_argument("--input", required=True, help="Input log file (.zst or .log)")
    parser.add_argument("--output", required=True, help="Output JSON file")

    args = parser.parse_args()

    # initialize all classifiers
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

    results = []

    # single-pass processing
    for line in read_log_lines(args.input):
        event = parse_line(line)

        for classifier in classifiers:
            result = classifier.match(event)
            if result:
                results.append(result)

    # write output
    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Report saved to {args.output}")
    print(f"Total classified events: {len(results)}")


if __name__ == "__main__":
    main()