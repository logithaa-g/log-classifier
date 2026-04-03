from parser.line_parser import parse_line

from classifiers.switchd_crash import SwitchDCrashClassifier
from classifiers.vip_failure import VIPFailureClassifier
from classifiers.port_errors import PortErrorClassifier
from classifiers.switch_init import SwitchInitClassifier
from classifiers.switch_health import SwitchHealthClassifier
from classifiers.lacp import LACPClassifier
from classifiers.mastership import MastershipClassifier
from classifiers.admin_net import AdminNetClassifier
from classifiers.link_flap import LinkFlapClassifier


def test_switchd_crash():
    line = "2026-03-05 host1 switchd ERROR switchd crashed unexpectedly"
    event = parse_line(line)
    result = SwitchDCrashClassifier().match(event)

    assert result is not None
    assert result["category"] == "SwitchD Crash"


def test_vip_failure():
    line = "2026-03-05 host1 network ERROR vip creation failed"
    event = parse_line(line)
    result = VIPFailureClassifier().match(event)

    assert result is not None
    assert result["category"] == "VIP Creation Failure"


def test_port_error():
    line = "2026-03-05 host1 port ERROR port 3 down"
    event = parse_line(line)
    result = PortErrorClassifier().match(event)

    assert result is not None
    assert result["category"] == "Port Error"


def test_switch_init():
    line = "2026-03-05 host1 switch INFO switchd started successfully"
    event = parse_line(line)
    result = SwitchInitClassifier().match(event)

    assert result is not None
    assert result["category"] == "Switch Initialization"


def test_switch_health():
    line = "2026-03-05 host1 switch INFO switch status change: unknown -> retry"
    event = parse_line(line)
    result = SwitchHealthClassifier().match(event)

    assert result is not None
    assert result["category"] == "Switch Health Transition"


def test_lacp():
    line = "2026-03-05 host1 lacp ERROR LACP aggregation failed"
    event = parse_line(line)
    result = LACPClassifier().match(event)

    assert result is not None
    assert result["category"] == "LACP Failure"


def test_mastership():
    line = "2026-03-05 host1 cluster INFO master changed to node2"
    event = parse_line(line)
    result = MastershipClassifier().match(event)

    assert result is not None
    assert result["category"] == "Mastership Change"


def test_admin_net():
    line = "2026-03-05 host1 admin ERROR admin network down"
    event = parse_line(line)
    result = AdminNetClassifier().match(event)

    assert result is not None
    assert result["category"] == "Admin Network Issue"


def test_link_flap():
    line = "2026-03-05 host1 port INFO port 1 down"
    event = parse_line(line)
    result = LinkFlapClassifier().match(event)

    assert result is not None
    assert result["category"] == "Link Flap"