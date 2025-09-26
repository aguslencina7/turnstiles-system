from core.normalization import normalize_credential
import pytest

def test_basic_normalization():
    assert normalize_credential("0x0a:1f") == "0A1F" or "0X0A1F"

def test_remove_separators():
    assert normalize_credential("12-34-56") == "123456"

def test_uppercase():
    assert normalize_credential("aBcDeF") == "ABCDEF"
 
def test_invalid_raises():
    with pytest.raises(ValueError):
        normalize_credential("###@@")