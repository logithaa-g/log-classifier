from .base import BaseClassifier

class MastershipClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "master" in msg and ("change" in msg or "election" in msg):
            return {
                "category": "Mastership Change",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None