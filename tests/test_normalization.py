import pytest
from core.normalization import normalize_credential

def test_upper_and_filter():
    assert normalize_credential("0x0a:1f") == "0A1F"

def test_invalid():
    with pytest.raises(ValueError):
        normalize_credential("###")
