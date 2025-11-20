# src/exchange_info.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Get exchange info for a symbol")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    args = parser.parse_args()
    symbol = validate_symbol(args.symbol)

    client = BinanceFuturesClient()
    try:
        resp = client._request("GET", "/fapi/v1/exchangeInfo", params={}, signed=False)
        symbols = resp.get("symbols", [])
        info = next((s for s in symbols if s.get("symbol") == symbol), None)
        logger.info("Exchange info: %s", info or resp)
        if info:
            # Print key filters cleanly
            print("Exchange info summary.")
            print(f"Symbol: {symbol}")
            for f in info.get("filters", []):
                print(f"{f.get('filterType')}: {f}")
        else:
            print("Symbol info not found.")
    except Exception as e:
        logger.error("Exchange info failed: %s", e)
        print("Exchange info failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
