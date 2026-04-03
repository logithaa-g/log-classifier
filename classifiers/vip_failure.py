from .base import BaseClassifier

class VIPFailureClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "vip" in msg and ("fail" in msg or "error" in msg):
            return {
                "category": "VIP Creation Failure",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None