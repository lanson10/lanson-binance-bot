# src/validators.py
from __future__ import annotations
from typing import Tuple
import re

VALID_SIDES = {"BUY", "SELL"}

def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValueError("Invalid symbol format. Example: BTCUSDT")
    return symbol.upper()

def validate_side(side: str) -> str:
    s = side.upper()
    if s not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL")
    return s

def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except Exception:
        raise ValueError("Quantity must be a number")
    if q <= 0:
        raise ValueError("Quantity must be > 0")
    return q

def validate_price(price: str) -> float:
    try:
        p = float(price)
    except Exception:
        raise ValueError("Price must be a number")
    if p <= 0:
        raise ValueError("Price must be > 0")
    return p
