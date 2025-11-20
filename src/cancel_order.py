# src/cancel_order.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Cancel a single futures order by order id")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("order_id", help="Order ID", type=int)
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    order_id = args.order_id
    client = BinanceFuturesClient()
    try:
        resp = client._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": order_id}, signed=True)
        logger.info("Cancel order response: %s", resp)
        print("Cancel order result.")
        print(f"Order ID: {order_id}")
        print(f"Status: {'CANCELLED' if resp.get('orderId') or resp == {} or resp.get('code') is None else resp}")
    except Exception as e:
        logger.error("Cancel order failed: %s", e)
        print("Cancel failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
