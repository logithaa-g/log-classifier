from .base import BaseClassifier

class SigAbortClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "sigabrt" in msg:
            return {
                "category": "SIGABRT Events",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None