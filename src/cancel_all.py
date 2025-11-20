# src/cancel_all.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Cancel ALL open Futures orders for a symbol")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    client = BinanceFuturesClient()
    try:
        resp = client._request("DELETE", "/fapi/v1/allOpenOrders", params={"symbol": symbol}, signed=True)
        logger.info("Cancel all response: %s", resp)
        print("Cancel all result.")
        print(f"Symbol: {symbol}")
        print(f"Result: {resp.get('msg') if isinstance(resp, dict) else resp}")
    except Exception as e:
        logger.error("Cancel all failed: %s", e)
        print("Cancel all failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
