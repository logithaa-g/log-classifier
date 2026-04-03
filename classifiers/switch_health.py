from .base import BaseClassifier

class SwitchHealthClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "switch" in msg and ("status change" in msg or "health" in msg):
            return {
                "category": "Switch Health Transition",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None