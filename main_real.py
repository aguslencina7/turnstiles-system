from core.config import load_config
from core.builders import build_reader, build_gpio
from utils.loggers import logger
from core.state_machine import TurnstileStateMachine
from api.rest_api import ApiClient

def main():
    cfg = load_config()
    reader = build_reader(cfg)   # keyboard
    gpio   = build_gpio(cfg)     # real
    api    = ApiClient(simulated=False)  # ← cuando implementes API real

    sm = TurnstileStateMachine(api=api, gpio=gpio, cfg=cfg)
    logger.info(f"[PI] Backends: reader={cfg['READER_BACKEND']} gpio={cfg['GPIO_BACKEND']}")

    # Loop lectura continua (keyboard)
    with reader:  # KeyboardCardReader soporta contexto; ReaderSim también funciona sin with
        while True:
            raw = reader.read_credential()
            if raw is None:
                continue
            sm.process_credential(raw, direction="CW")

if __name__ == "__main__":
    main()
