import time
from core.state_machine import TurnstileStateMachine
from core.debounce import Debouncer
from api.rest_api import ApiClient
from hardware.gpio_sim import GpioSim
from hardware.reader_sim import CredentialReader

def test_reader_debounce_intergation(capsys):
    cfg = {"GATE_ID": "turnstile_01", "CONFIRM_TIMEOUT_SEC": 1}
    api = ApiClient(simulated= True)
    gpio = GpioSim(confirm_after_s= 0.1)

    sm = TurnstileStateMachine(api= api, gpio= gpio, cfg= cfg)

    # Replace the internal debouncer with a bigger one (1s)
    sm.debouncer = Debouncer(window_ms= 1000)

    # Simulated reader in manual mode with repeated credentials
    reader = CredentialReader(mode= "manual", sequense=["ABCD1234", "ABCD1234", "WXYZ9876"], loop_sequence= False)

    results = []
    while True:
        raw = reader.read_once()
        if raw is None:
            break
    res = sm.process_credential(raw)
    results.append(res)
    time.sleep(0.2) #Simulates time between reads

    assert results[0] in ("OK", "DENIED")
    assert results[1] == "IGNORED"
    assert results[2] in ("OK", "DENIED")