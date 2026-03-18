from parser.line_parser import parse_line

def test_valid_log_line():
    line = "2026-03-05 18:16:00.895374 host1 source INFO message here"
    event = parse_line(line)

    assert event.timestamp == "2026-03-05 18:16:00.895374"
    assert event.level == "INFO"


def test_invalid_log_line():
    line = "random garbage log"
    event = parse_line(line)

    assert event.timestamp == "UNKNOWN"


def test_error_level():
    line = "2026-03-05 18:16:00 host1 source ERROR something failed"
    event = parse_line(line)

    assert event.level == "ERROR"


def test_warning_level():
    line = "2026-03-05 18:16:00 host1 source WARN warning message"
    event = parse_line(line)

    assert event.level == "WARN"


def test_message_extraction():
    line = "2026-03-05 18:16:00 host1 source INFO hello world"
    event = parse_line(line)

    assert "hello world" in event.message