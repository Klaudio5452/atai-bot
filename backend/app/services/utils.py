"""
Small utilities used by services.
"""
import re

def parse_airports_from_text(text: str):
    """
    Naive airport code extraction (3-letter IATA codes).
    Example: 'TIR-FCO' -> ['TIR','FCO']
    """
    if not text:
        return []
    codes = re.findall(r"\b[A-Z]{3}\b", text)
    return codes
