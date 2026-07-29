from .base import BaseClassifier

class TimeoutsClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if (
            "request timeout" in msg
            or "rpc timeout" in msg
            or "health check timeout" in msg
            or "timeout" in msg
        ):
            return {
                "category": "Timeout",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None