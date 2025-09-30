from core.state_machine import TurnstileStateMachine
from api.rest_api import ApiClient
from hardware.gpio_controller_pc import GpioSim
from hardware.reader_pc import ReaderSim

def test_flow_with_debounce():
    cfg = {"GATE_ID": "turnstile_01", "CONFIRM_TIMEOUT_SEC": 1}
    api = ApiClient(simulated=True)
    gpio = GpioSim(confirm_after_s=0.1)
    sm = TurnstileStateMachine(api=api, gpio=gpio, cfg=cfg)

    reader = ReaderSim(mode="manual", sequence=["ABCD1234", "ABCD1234", "FEDCBA98"], loop_sequence=False)
    results = []
    while True:
        raw = reader.read_once()
        if raw is None:
            break
        results.append(sm.process_credential(raw, direction="CW"))

    # 1° procesa, 2° ignorado por rebote, 3° procesa
    assert results[0] in ("OK", "DENIED")
    assert results[1] == "IGNORED"
    assert results[2] in ("OK", "DENIED")
