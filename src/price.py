# src/price.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Get latest price for a symbol")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    args = parser.parse_args()
    symbol = validate_symbol(args.symbol)

    client = BinanceFuturesClient()
    try:
        resp = client.get_symbol_price(symbol)
        logger.info("Price fetched: %s", resp)
        print("Price summary.")
        print(f"Symbol: {symbol}, Price: {resp.get('price')}")
    except Exception as e:
        logger.error("Price failed: %s", e)
        print("Price fetch failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
