import time
import pytest
from core.debounce import Debouncer

def test_first_seen_is_not_debounced():
    d = Debouncer(window_ms=500)
    assert d.is_debounced("ABC123") is False  # primera vez: se procesa

def test_second_seen_is_debounced():
    d = Debouncer(window_ms=500)
    d.is_debounced("ABC123")
    assert d.is_debounced("ABC123") is True  # segunda vez, demasiado rápido

def test_after_window_is_not_debounced():
    d = Debouncer(window_ms=200)
    d.is_debounced("XYZ789")
    time.sleep(0.3)  # esperar más que la ventana
    assert d.is_debounced("XYZ789") is False  # ya puede procesarse de nuevo

def test_different_credentials_independent():
    d = Debouncer(window_ms=500)
    assert d.is_debounced("AAA111") is False
    assert d.is_debounced("BBB222") is False  # distinta credencial, no rebota
    assert d.is_debounced("AAA111") is True   # misma credencial, rebote
