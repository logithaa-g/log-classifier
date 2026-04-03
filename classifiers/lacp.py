from .base import BaseClassifier

class LACPClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "lacp" in msg or "aggregation" in msg or "bond" in msg:
            if "fail" in msg or "error" in msg or "down" in msg:
                return {
                    "category": "LACP Failure",
                    "timestamp": event.timestamp,
                    "host": event.host,
                    "details": event.message
                }
        return None