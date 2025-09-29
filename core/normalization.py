import re

def normalize_credential(raw): #Function for normalize the code coming from the card reader
    """
    Normalizes a raw credential to a consistent format:
    -Deletes spaces and separators. 
    -Converts to uppercase
    -Validates that only has hexadecimal characters or numbers
    """
    if not raw:
        raise ValueError("Empty credential")
    
    clean = re.sub(r"[^A-Fa-f0-9]", "", raw)
    del_spaces = re.sub(r" ", "", clean)
    del_char = re.sub(r"-", "", del_spaces)


    if not clean:
        raise ValueError(f"Invalid credential: {raw}")
    
    return del_char.upper()

#def format_detector(raw)

#def normalize_hex(raw):

#def normalize_decimal(raw):

#def normalize_ascii_tag():
