# src/check_order.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Check status of a Binance Futures order")
    parser.add_argument("symbol", help="Symbol, e.g., BTCUSDT")
    parser.add_argument("order_id", help="Order ID", type=int)
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    order_id = args.order_id

    try:
        client = BinanceFuturesClient()

        # CORRECT ENDPOINT
        resp = client._request(
            "GET",
            "/fapi/v1/order",
            params={"symbol": symbol, "orderId": order_id},
            signed=True
        )

        print("\nOrder Status:")
        print(resp)
        logger.info(f"Checked order: {resp}")

    except Exception as e:
        logger.error(f"Failed to check order: {e}")
        print("Error:", e)

if __name__ == "__main__":
    main()
