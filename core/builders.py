# core/builders.py
import os, platform
from utils.loggers import logger

def on_raspberry() -> bool:
    return platform.system()=="Linux" and os.path.exists("/proc/device-tree/model")

def build_reader(cfg):
    if cfg["READER_BACKEND"] == "keyboard":
        #from hardware.reader_real import #Falta codigo de reader real
        if not HAVE_EVDEV and not cfg["ALLOW_PC_FALLBACK"]:
            raise RuntimeError("READER_BACKEND=keyboard sin evdev y ALLOW_PC_FALLBACK=false")
        return KeyboardCardReader()
    elif cfg["READER_BACKEND"] == "sim":
        from hardware.reader_sim import CredentialReaderSim
        return CredentialReaderSim(mode="manual")
    else:
        raise ValueError("READER_BACKEND inválido")

def build_gpio(cfg):
    if cfg["GPIO_BACKEND"] == "real":
        from hardware.gpio_real import GpioReal, HAVE_RPI_GPIO
        if not HAVE_RPI_GPIO and not cfg["ALLOW_PC_FALLBACK"]:
            raise RuntimeError("GPIO_BACKEND=real sin RPi.GPIO y ALLOW_PC_FALLBACK=false")
        return GpioReal()
    elif cfg["GPIO_BACKEND"] == "sim":
        from hardware.gpio_sim import GpioSim
        return GpioSim(confirm_after_s=1.0)
    else:
        raise ValueError("GPIO_BACKEND inválido")
