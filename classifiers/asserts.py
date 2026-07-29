from .base import BaseClassifier

class AssertsClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if (
            "assert failed" in msg
            or "assertionerror" in msg
            or "assertion" in msg
            or "assert" in msg
        ):
            return {
                "category": "Assert Failure",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None