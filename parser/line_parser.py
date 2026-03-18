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
    # flexible regex (works for your sample)
    pattern = r"^(\d{4}-\d{2}-\d{2} \S+) (\S+) (\S+).*?(INFO|ERROR|WARN|DEBUG).*?:?\s(.*)$"

    match = re.match(pattern, line)

    if match:
        return LineParsedEvent(
            timestamp=match.group(1),
            host=match.group(2),
            source=match.group(3),
            level=match.group(4),
            message=match.group(5)
        )

    # fallback if parsing fails
    return LineParsedEvent(
        timestamp="UNKNOWN",
        host="UNKNOWN",
        source="UNKNOWN",
        level="UNKNOWN",
        message=line
    )