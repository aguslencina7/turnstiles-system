from dotenv import load_dotenv
import os

class ConfigError(Exception):
    pass

def _require(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise ConfigError(f"Missing required environment variable: {name}")
    return v

def load_config() -> dict:
    load_dotenv()  # carga .env si está presente
    
    cfg = {

        "READER_BACKEND": os.getenv("READER_BACKEND", "sim"),
        "GPIO_BACKEND": os.getenv("GPIO_BACKEND", "sim"),
        "ALLOW_PC_FALLBACK": os.getenv("ALLOW_PC_FALLBACK", "true").lower()=="true",
        "GATE_ID": os.getenv("GATE_ID", "turnstile_01"),
        "CONFIRM_TIMEOUT_SEC": float(os.getenv("CONFIRM_TIMEOUT_SEC", "5")),

        # API (opcionales en dev sim)
        "TENANT_ID": os.getenv("TENANT_ID"),
        "CLIENT_ID": os.getenv("CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
        "TOKEN_URL": os.getenv("TOKEN_URL"),
        "API_URL": os.getenv("API_URL"),
    }
    return cfg
