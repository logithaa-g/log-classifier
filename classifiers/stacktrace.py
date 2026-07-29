from .base import BaseClassifier

class StacktraceClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "stacktrace" in msg:
            return {
                "category": "Stacktrace Events",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None