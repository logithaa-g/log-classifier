from .base import BaseClassifier

class SwitchInitClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if (
            ("starting" in msg or "started" in msg or "initializing" in msg)
            and ("switch" in msg or "switchd" in msg or "switch manager" in msg)
        ):
            return {
                "category": "Switch Initialization",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None