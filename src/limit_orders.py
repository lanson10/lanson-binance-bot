# src/limit_orders.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol, validate_side, validate_quantity, validate_price
from .logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Place a limit order")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity")
    parser.add_argument("price", help="Price")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    qty = validate_quantity(args.quantity)
    price = validate_price(args.price)

    client = BinanceFuturesClient()
    try:
        resp = client.place_limit_order(symbol=symbol, side=side, price=price, quantity=qty)
        logger.info("Limit order response: %s", resp)

        # Clean output (Style C)
        print("Limit order placed.")
        print(f"Side: {side}")
        print(f"Qty: {qty}")
        print(f"Price: {price}")
        print(f"Status: {resp.get('status')}")
        print(f"Order ID: {resp.get('orderId')}")
    except Exception as e:
        logger.error("Limit order failed: %s", e)
        print("Limit order failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
