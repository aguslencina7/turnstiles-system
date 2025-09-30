from core.config import load_config
from core.builders import build_reader, build_gpio
from utils.loggers import logger
from core.state_machine import TurnstileStateMachine
from api.rest_api import ApiClient

def main():
    cfg = load_config()
    # Forzamos sim en PC si querés:
    cfg["READER_BACKEND"] = "sim"
    cfg["GPIO_BACKEND"] = "sim"
    cfg["ALLOW_PC_FALLBACK"] = True

    reader = build_reader(cfg)
    gpio   = build_gpio(cfg)
    api    = ApiClient(simulated=True)

    sm = TurnstileStateMachine(api=api, gpio=gpio, cfg=cfg)
    logger.info(f"[PC] Backends: reader={cfg['READER_BACKEND']} gpio={cfg['GPIO_BACKEND']}")

    print("PC Simulación: presiona Enter para generar o usa ReaderSim secuencia.")
    while True:
        raw = reader.read_once() if hasattr(reader, "read_once") else input(">> ")
        if raw is None: break
        print("RAW:", raw, "| RES:", sm.process_credential(raw, direction="CW"))

if __name__ == "__main__":
    main()
