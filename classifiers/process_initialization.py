from .base import BaseClassifier

class ProcessInitializationClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if (
            "starting" in msg
            or "started" in msg
            or "initializing" in msg
            or "initialized" in msg
            or "initialization" in msg
        ):
            return {
                "category": "Process Initialization",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }

        return None