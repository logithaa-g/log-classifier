import re
from dataclasses import dataclass

@dataclass
class LineParsedEvent:
    timestamp: str
    host: str
    source: str
    level: str
    message: str


def parse_line(line: str):
    # Stripping trailing/leading whitespaces for safety
    line = line.strip()

    # Replaced both old patterns with the new unified layout pattern
    pattern1 = (
        r"^(\d{4}-\d{2}-\d{2} \S+)\s+"
        r"(\S+)\s+"
        r"(\S+)\s+-\s+"
        r"(INFO|ERROR|WARN|DEBUG)\s+-\s+"
        r"(.*)$"
    )

    match = re.match(pattern1, line)
    if match:
        print("MATCHED:", line)
        return LineParsedEvent(
            timestamp=match.group(1),
            host=match.group(2),
            source=match.group(3),
            level=match.group(4),
            message=match.group(5)
        )

    # Fallback (completely unparseable line)
    print("FAILED:", line)
    return LineParsedEvent(
        timestamp="UNKNOWN",
        host="UNKNOWN",
        source="UNKNOWN",
        level="UNKNOWN",
        message=line
    )
