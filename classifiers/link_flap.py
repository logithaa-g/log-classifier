from .base import BaseClassifier

class LinkFlapClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "port" in msg and ("down" in msg or "up" in msg):
            return {
                "category": "Link Flap",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None