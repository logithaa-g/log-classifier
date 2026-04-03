from .base import BaseClassifier

class PortErrorClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "port" in msg and ("error" in msg or "down" in msg or "fault" in msg):
            return {
                "category": "Port Error",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None