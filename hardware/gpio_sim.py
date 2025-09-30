# For simulation, check main.py for GpioSim configuration
import time

class GpioSim:
    def __init__(self, confirm_after_s: float = 1.0):
        self.confirm_after_s = confirm_after_s
    
    def enable_cw(self, pulse_ms = 300):
        print(f"[SIM GPIO] enable CW {pulse_ms}ms")
        time.sleep(pulse_ms/1000)
    
    def enable_ccw(self, pulse_ms = 300):
        print(f"[SIM GPIO] enable CCW {pulse_ms}ms")
        time.sleep(pulse_ms/1000)

    def wait_confirmation(self, timeout_s = 5.0) -> bool:
        time.sleep(min(self.confirm_after_s, timeout_s))
        return self.confirm_after_s <= timeout_s
    

