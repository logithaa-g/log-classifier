import argparse
import json
from parser.decompressor import read_log_lines
from parser.line_parser import parse_line


def main():
    parser = argparse.ArgumentParser(description="Log Classifier")
    parser.add_argument("--input", required=True, help="Input log file (.zst or .log)")
    parser.add_argument("--output", required=True, help="Output JSON file")

    args = parser.parse_args()

    parsed_events = []

    # read + parse
    for line in read_log_lines(args.input):
        event = parse_line(line)

        parsed_events.append({
            "timestamp": event.timestamp,
            "host": event.host,
            "source": event.source,
            "level": event.level,
            "message": event.message
        })

    # write output file
    with open(args.output, "w") as f:
        json.dump(parsed_events, f, indent=4)

    print(f"✅ Report saved to {args.output}")
    print(f"Total logs processed: {len(parsed_events)}")  # ✅ moved here


if __name__ == "__main__":
    main()