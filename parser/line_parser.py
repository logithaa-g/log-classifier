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
    # Pattern 1: with log level
    pattern1 = r"^(\d{4}-\d{2}-\d{2} \S+) (\S+) (\S+).*?(INFO|ERROR|WARN|DEBUG).*?:?\s(.*)$"

    match = re.match(pattern1, line)
    if match:
        return LineParsedEvent(
            timestamp=match.group(1),
            host=match.group(2),
            source=match.group(3),
            level=match.group(4),
            message=match.group(5)
        )

    # Pattern 2: no log level (fallback structured)
    pattern2 = r"^(\d{4}-\d{2}-\d{2} \S+) (\S+) (\S+): (.*)$"

    match = re.match(pattern2, line)
    if match:
        return LineParsedEvent(
            timestamp=match.group(1),
            host=match.group(2),
            source=match.group(3),
            level="UNKNOWN",  # no level present
            message=match.group(4)
        )

    # fallback (completely unknown)
    return LineParsedEvent(
        timestamp="UNKNOWN",
        host="UNKNOWN",
        source="UNKNOWN",
        level="UNKNOWN",
        message=line
    )