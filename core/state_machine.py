from core.normalization import normalize_credential
from utils.loggers import logger

class TurnstileStateMachine:
    def __init__(self):
        self.state = "IDLE"

    def process_credential(self, raw = str):
        logger.info(f"Actual state: {self.state}")

        try: 
            cred = normalize_credential(raw)
            logger.info(f"Credential normalized: {cred}.")
        except ValueError as e:
            logger.error(f"Error normalizing credential: {e}.")
            return "DENIED"
        
        authorized = True

        if authorized:
            self.state = "ENABLED"
            logger.info(f"Access authorized -> Unlocking turnstile (simulated).")
            # GPIO.enable()
            self.state = "WAIT_CONFIRM"
        else:
            self.state = "DENIED"
            logger.warning("Access denied.")
        
        # User cross the turnstile
        self.state = "LOG"
        logger.info("Access confirmed (simulated).")
        self.state = "IDLE"

        return "OK"
    
# self.state = "AUTH" when the request is received (by API or local cache)