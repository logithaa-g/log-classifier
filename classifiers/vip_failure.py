from .base import BaseClassifier
#Virtual IP crea on failed 
#check for “vip” and either “fail” or “error”.
class VIPFailureClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "vip" in msg and ("fail" in msg or "error" in msg):
            return {
                "category": "VIP Creation Failure",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None