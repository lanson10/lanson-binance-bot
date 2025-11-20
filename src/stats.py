# src/stats.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol

def main():
    parser = argparse.ArgumentParser(description="Get 24h stats for symbol")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    args = parser.parse_args()
    symbol = validate_symbol(args.symbol)

    client = BinanceFuturesClient()
    try:
        resp = client._request("GET", "/fapi/v1/ticker/24hr", params={"symbol": symbol}, signed=False)
        print(resp)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
