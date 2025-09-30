from core.normalization import normalize_credential
from utils.loggers import logger
from core.debounce import Debouncer

class TurnstileStateMachine:
    def __init__(self, api, gpio, cfg: dict):
        self.api = api
        self.gpio = gpio
        self.cfg = cfg
        self.state = "IDLE"
        self.debouncer = Debouncer(window_ms = 800)

    def process_credential(self, raw: str, direction = "CW"):
        logger.info(f"Actual state: {self.state} raw = {raw!r}")

        try: 
            cred = normalize_credential(raw)
            logger.info(f"Credential normalized: {cred}.")
        except ValueError as e:
            logger.error(f"Error normalizing credential: {e}.")
            return "DENIED"
        
        if self.debouncer.is_debounced(cred):
            logger.warning(f"Credential {cred} ignored for bounce.")
            return "IGNORED"
        
        # Auth
        self.state = "AUTH"
        token = self.api.get_token()
        resp = self.api.validate_credential(cred, self.cfg["GATE_ID"], token)
        
        if not resp.get("authorized"):
            logger.warning("Access denied")
            return "DENIED"
        
        # Enable
        self.state = "ENABLE"
        if direction == "CW":
            self.gpio.enable_cw(pulse_ms = 300)
        else:
            self.gpio.enable_ccw(pulse_ms = 300)

        # Wait confirm
        self.state = "WAIT_CONFIRM"
        ok = self.gpio.wait_confirmation(timeout_s = self.cfg.get("CONFIRM_TIMEOUT_SEC", 5))

        # Log
        self.state = "LOG"
        logger.info(f"confirm = {ok} user = {resp.get('user_id')}")

        # Reset
        self.state = "IDLE"
        if ok:
            return "OK"
        else:
            return "TIMEOUT"
    