from .base import BaseClassifier
#Switch changes state (like unknown → retry → healthy) 
#check for keywords like “status change” or “health” in the message. 

class SwitchHealthClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "switch" in msg and ("status change" in msg or "health" in msg):
            return {
                "category": "Switch Health Transition",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None