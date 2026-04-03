from .base import BaseClassifier
#Core switch process crashed
#detect “switchd” with words like “crash”, “failed”, or “terminated
class SwitchDCrashClassifier(BaseClassifier):

    def match(self, event):
        msg = event.message.lower()

        if "switchd" in msg and ("crash" in msg or "failed" in msg or "terminated" in msg):
            return {
                "category": "SwitchD Crash",
                "timestamp": event.timestamp,
                "host": event.host,
                "details": event.message
            }
        return None