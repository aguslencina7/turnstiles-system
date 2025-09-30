import time
from core.debounce import Debouncer

def test_first_seen():
    d = Debouncer(500)
    assert d.is_debounced("ABC123") is False

def test_repeated_fast():
    d = Debouncer(500)
    d.is_debounced("ABC123")
    assert d.is_debounced("ABC123") is True

def test_after_window():
    d = Debouncer(200)
    d.is_debounced("XYZ789")
    time.sleep(0.3)
    assert d.is_debounced("XYZ789") is False
