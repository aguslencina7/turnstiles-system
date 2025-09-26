from dotenv import load_dotenv
import os

class ConfigError(Exception):
    pass

def _require(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise ConfigError(f"Missing required environment variable: {name}")
    return v

def load_config():
    load_dotenv()  # Carga .env si existe

    cfg = {
        # OAuth2 / API
        "TENANT_ID": _require("TENANT_ID"),
        "CLIENT_ID": _require("CLIENT_ID"),
        "CLIENT_SECRET": _require("CLIENT_SECRET"),
        "TOKEN_URL": _require("TOKEN_URL"),
        "API_URL": _require("API_URL"),

        # Identidad y políticas
        "GATE_ID": os.getenv("GATE_ID", "turnstile_01"),
        "MODE_POLICY": os.getenv("MODE_POLICY", "online_preferred"),

        # Tiempos (con defaults razonables)
        "API_TIMEOUT_SEC": float(os.getenv("API_TIMEOUT_SEC", "3")),
        "CACHE_TTL_HOURS": int(os.getenv("CACHE_TTL_HOURS", "48")),
        "DEBOUNCE_MS": int(os.getenv("DEBOUNCE_MS", "800")),
        "CONFIRM_TIMEOUT_SEC": float(os.getenv("CONFIRM_TIMEOUT_SEC", "5")),

        # GPIO (placeholders)
        "PIN_OUT_CW": int(os.getenv("PIN_OUT_CW", "17")),
        "PIN_OUT_CCW": int(os.getenv("PIN_OUT_CCW", "27")),
        "PIN_IN_CONFIRM": int(os.getenv("PIN_IN_CONFIRM", "22")),
    }

    # Derivados simples / validaciones
    if cfg["MODE_POLICY"] not in {"online_required", "online_preferred", "offline_allowed"}:
        raise ConfigError("MODE_POLICY must be one of: online_required|online_preferred|offline_allowed")

    return cfg
