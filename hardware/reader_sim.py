from __future__ import annotations
import time
from typing import Optional, Iterable

try:
    from evdev import InputDevice, list_devices, categorize, ecodes # type: ignore
    HAVE_EVDEV = True
except Exception:
    HAVE_EVDEV = False
    class DummyEcodes:
        def __getattr__(self, _): return 0
    ecodes = DummyEcodes()


# Keys Map
KEYMAP = {
    # upper row numeric keys
    getattr(ecodes, "KEY_0", 0): "0",
    getattr(ecodes, "KEY_1", 0): "1",
    getattr(ecodes, "KEY_2", 0): "2",
    getattr(ecodes, "KEY_3", 0): "3",
    getattr(ecodes, "KEY_4", 0): "4",
    getattr(ecodes, "KEY_5", 0): "5",
    getattr(ecodes, "KEY_6", 0): "6",
    getattr(ecodes, "KEY_7", 0): "7",
    getattr(ecodes, "KEY_8", 0): "8",
    getattr(ecodes, "KEY_9", 0): "9",

    # numeric keyboard
    getattr(ecodes, "KEY_KP0", 0): "0",
    getattr(ecodes, "KEY_KP1", 0): "1",
    getattr(ecodes, "KEY_KP2", 0): "2",
    getattr(ecodes, "KEY_KP3", 0): "3",
    getattr(ecodes, "KEY_KP4", 0): "4",
    getattr(ecodes, "KEY_KP5", 0): "5",
    getattr(ecodes, "KEY_KP6", 0): "6",
    getattr(ecodes, "KEY_KP7", 0): "7",
    getattr(ecodes, "KEY_KP8", 0): "8",
    getattr(ecodes, "KEY_KP9", 0): "9",

    # A-F keys for hex
    getattr(ecodes, "KEY_A", 0): "A",
    getattr(ecodes, "KEY_B", 0): "B",
    getattr(ecodes, "KEY_C", 0): "C",
    getattr(ecodes, "KEY_D", 0): "D",
    getattr(ecodes, "KEY_E", 0): "E",
    getattr(ecodes, "KEY_F", 0): "F",

    # common spacers
    getattr(ecodes, "KEY_MINUS", 0): "-",
    getattr(ecodes, "KEY_SLASH", 0): "/",
    getattr(ecodes, "KEY_EQUAL", 0): "=",
    getattr(ecodes, "KEY_DOT", 0): ".",
    getattr(ecodes, "KEY_COMMA", 0): ",",
    getattr(ecodes, "KEY_SEMICOLON", 0): ";",
    getattr(ecodes, "KEY_SPACE", 0): " ",
}

ENTER_KEYS = {
    getattr(ecodes, "KEY_ENTER", 0),
    getattr(ecodes, "KEY_KPENTER", 0),
    # Uncomment the nextline if the reader uses TAB like an ender
    # getattr(ecodes, "KEY_TAB", 0),
}

SHIFT_KEYS = {
    getattr(ecodes, "KEY_LEFTSHIFT", 0),
    getattr(ecodes, "KEY_RIGHTSHIFT", 0),
}

class CredentialReaderSim:
    """
    Lector de credenciales USB que emula teclado (HID).
    Lee directamente /dev/input/eventX, hace 'grab' para que no escriba en la consola,
    y devuelve una credencial cruda (string) cuando detecta ENTER.
    """
    def __init__(
        self,
        device_path: Optional[str] = None,
        name_hints: Iterable[str] = ("keyboard", "reader", "barcode"),
        grab: bool = True,
        read_timeout_s: float = 3.0,
        accept_separators: bool = True,
    ):
        self.read_timeout_s = read_timeout_s
        self.accept_separators = accept_separators
        self.grab = grab

        if not HAVE_EDVED:
            #Fallback: reading from stdin (only for local development)
            self.dev = None
            return
        
        self.device_path or self._auto_find_device(name_hints)
        self.dev = InputDevice(self.device_path)

        if grab:
            # Exclusive grab: avoids key inputs going to the terminal / GUI
            self.dev.grab()

    def _auto_find_device(self, hints: Iterable[str]) -> str:
        hints = tuple(h.lower() for h in hints)
        for path in list_devices(): # type: ignore
            d = InputDevice(path)
            name = (d.name or "").lower()
            if any(h in name for h in hints):
                return path
        
        # If cannot find by name, take the first with keyboard capacity
        for path in list_devices(): # type: ignore
            d = InputDevice(path)
            try:
                caps = d.capabilities(verbose = True)
            except Exception:
                continue
            if "EV_KEY" in str(caps):
                return path
        raise RuntimeError("Cannot find an input device.")
    
    def close(self):
        if HAVE_EDVED and self.dev is not None:
            try:
                if self.grab:
                    self.dev.ungrab()
                self.dev.close()
            except Exception:
                pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.close()

    def read_credential(self) -> Optional[str]:
        """
        Bloquea hasta recibir ENTER (o timeout). Devuelve la cadena sin \r\n.
        Si no hay evdev (desarrollo en PC), lee de stdin.
        """
        if not HAVE_EDVED:
            # Simple fallback for PC development
            try:
                raw = input(">> (stdin reader) ")
            except KeyboardInterrupt:
                return None
        
        buf: list[str] = []
        shift_pressed = False
        start = time.time()

        for event in self.dev.read_loop():
            #Manual timeout (read_loop is infinite)
            if self.read_timeout_s and (time.time() - start) > self.read_timeout_s:
                return None

            if event.type != getattr(ecodes, "EV_KEY", 0):
                continue

            # 0=UP, 1=DOWN, 2=HOLD
            if event.value not in (0, 1):
                continue 

            code = event.code

            # Manejo de SHIFT (por si tu lector lo usa; muchos no lo necesitan)
            if code in SHIFT_KEYS:
                shift_pressed = (event.value == 1)
                continue

            # ENTER: finaliza lectura
            if code in ENTER_KEYS and event.value == 1:
                raw = "".join(buf).strip()
                return raw if raw else None

            # Solo tomamos key-down
            if event.value != 1:
                continue

            # Mapeo
            ch = KEYMAP.get(code)
            if ch is None:
                # Descartamos teclas que no estén en el map
                continue

            # Si no queremos separadores, filtrarlos aquí
            if not self.accept_separators and ch in "-/=. ,;":
                continue

            # Si SHIFT estuviera activo y tu lector lo usara para letras, aquí podrías
            # aplicar transformaciones. Para HEX usamos mayúsculas ya en KEYMAP.
            buf.append(ch)