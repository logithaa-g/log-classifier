from .base import BaseClassifier

class AdminNetClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "admin" in msg and ("network" in msg or "fail" in msg or "down" in msg):
            return {
                "category": "Admin Network Issue",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None