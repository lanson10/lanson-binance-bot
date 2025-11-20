# src/open_orders.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="View all open orders for a Futures symbol")
    parser.add_argument("symbol", help="Symbol, e.g., BTCUSDT")
    args = parser.parse_args()
    symbol = validate_symbol(args.symbol)

    client = BinanceFuturesClient()
    try:
        response = client._request("GET", "/fapi/v1/openOrders", params={"symbol": symbol}, signed=True)
        logger.info("Open orders: %s", response)
        print("Open orders summary.")
        if response:
            for o in response:
                print(f"Order ID: {o.get('orderId')}, Side: {o.get('side')}, Qty: {o.get('origQty')}, Price: {o.get('price')}, Status: {o.get('status')}")
        else:
            print("No open orders for", symbol)
    except Exception as e:
        logger.error("Failed to fetch open orders: %s", e)
        print("Fetch open orders failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
