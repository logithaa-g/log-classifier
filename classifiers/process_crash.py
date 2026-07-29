from .base import BaseClassifier

class ProcessCrashClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if (
            "crash" in msg
            or "failed" in msg
            or "restart" in msg
            or "restarted" in msg
        ):
            return {
                "category": "Process Crash",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None