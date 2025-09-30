# hardware/gpio_real.py
try:
    import RPi.GPIO as GPIO #type: ignore
    HAVE_RPI_GPIO = True
except Exception:
    HAVE_RPI_GPIO = False

import time

class GpioReal:
    """
    Mapear pines reales según tu cableado.
    CW/CCW como salidas a relé/opto → J11
    CONFIRM como entrada desde J10
    """
    PIN_OUT_CW  = 17
    PIN_OUT_CCW = 27
    PIN_IN_CONFIRM = 22

    def __init__(self):
        if not HAVE_RPI_GPIO:
            raise RuntimeError("RPi.GPIO no disponible")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_OUT_CW, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_OUT_CCW, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_IN_CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ajusta NA/NC

    def enable_cw(self, pulse_ms=300):
        GPIO.output(self.PIN_OUT_CW, GPIO.HIGH)
        time.sleep(pulse_ms/1000)
        GPIO.output(self.PIN_OUT_CW, GPIO.LOW)

    def enable_ccw(self, pulse_ms=300):
        GPIO.output(self.PIN_OUT_CCW, GPIO.HIGH)
        time.sleep(pulse_ms/1000)
        GPIO.output(self.PIN_OUT_CCW, GPIO.LOW)

    def wait_confirmation(self, timeout_s=5.0) -> bool:
        # simple polling; puedes mejorarlo con eventos
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if GPIO.input(self.PIN_IN_CONFIRM) == GPIO.LOW:  # depende de NA/NC
                return True
            time.sleep(0.01)
        return False

    def __del__(self):
        try:
            GPIO.cleanup()
        except Exception:
            pass
