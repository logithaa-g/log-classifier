from .base import BaseClassifier

#Management network problem 
#check for “admin” and “network” or failure-related words like “down” or “fail”

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