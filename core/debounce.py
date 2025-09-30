import time
from typing import Dict

class Debouncer:
    """
    Avoids processing twice the same credential in a short interval
    """

    def __init__(self, window_ms: int = 800):
        self.window = window_ms / 1000.0
        self.last_seen: Dict[str, float] = {}
    
    def is_debounced(self, credential: str) -> bool:
        """
        Returns True if the credential was seen too soon
        """
        now = time.monotonic()
        last = self.last_seen.get(credential)

        if last and (now - last) < self.window:
            return True 
        
        self.last_seen[credential] = now
        return False