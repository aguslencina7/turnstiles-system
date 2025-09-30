from core.config import load_config
from utils.loggers import logger
from api.rest_api import ApiClient
from hardware.gpio_controller_pc import GpioSim
from hardware.reader_pc import ReaderSim
from core.state_machine import TurnstileStateMachine

def main():
    cfg = load_config()
    cfg["READER_BACKEND"] = "sim"
    cfg["GPIO_BACKEND"]   = "sim"

    api  = ApiClient(simulated=True)
    gpio = GpioSim(confirm_after_s=1.0)
    sm   = TurnstileStateMachine(api=api, gpio=gpio, cfg=cfg)
    reader = ReaderSim(mode="manual", sequence=None)

    logger.info("Sim listo. Ctrl+C para salir.")
    while True:
        raw = reader.read_once()
        if raw is None:
            continue
        res = sm.process_credential(raw, direction="CW")
        print("RAW:", raw, "→", res)

if __name__ == "__main__":
    main()
