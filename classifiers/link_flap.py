from .base import BaseClassifier
#A port goes down and comes back up → unstable link
#check if the log message contains the word “port” and either “down” or “up”. 
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