# src/market_orders.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol, validate_side, validate_quantity
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Place a market order")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    qty = validate_quantity(args.quantity)

    client = BinanceFuturesClient()
    try:
        resp = client.place_market_order(symbol=symbol, side=side, quantity=qty)
        # Log full response
        logger.info("Market order response: %s", resp)

        # Clean terminal output (Style C)
        print("Order executed.")
        print(f"Side: {side}")
        print(f"Qty: {qty}")
        print(f"Status: {resp.get('status')}")
        print(f"Order ID: {resp.get('orderId')}")
        print(f"Executed Qty: {resp.get('executedQty')}")
    except Exception as e:
        logger.error("Market order failed: %s", e)
        print("Order failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
