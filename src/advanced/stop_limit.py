# src/advanced/stop_limit.py
from __future__ import annotations
import argparse
import time
from ..client import BinanceFuturesClient
from ..validators import validate_symbol, validate_side, validate_quantity, validate_price
from ..logger import get_logger

logger = get_logger(__name__)

class StopLimitTrigger:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def wait_and_place(self, symbol: str, side: str, quantity: float,
                       trigger_price: float, limit_price: float,
                       check_interval: float = 2.0):

        logger.info("Watching price for stop-limit: %s %s qty=%s trigger=%s limit=%s",
                    symbol, side, quantity, trigger_price, limit_price)
        print("Watching price...")
        while True:
            price_info = self.client.get_symbol_price(symbol)
            current = float(price_info["price"])
            print(f"Current: {current}")
            # BUY trigger: price goes down to trigger
            if side == "BUY" and current <= trigger_price:
                resp = self.client.place_limit_order(symbol, "BUY", limit_price, quantity)
                logger.info("Stop-limit placed: %s", resp)
                return {"action": "placed", "type": "LIMIT", "price": limit_price, "order": resp}
            # SELL trigger: price goes up to trigger
            if side == "SELL" and current >= trigger_price:
                resp = self.client.place_limit_order(symbol, "SELL", limit_price, quantity)
                logger.info("Stop-limit placed: %s", resp)
                return {"action": "placed", "type": "LIMIT", "price": limit_price, "order": resp}
            time.sleep(check_interval)

def main():
    parser = argparse.ArgumentParser(description="Stop-Limit trigger for Binance Futures")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("trigger_price", help="Trigger price")
    parser.add_argument("limit_price", help="Limit price for order")
    parser.add_argument("--qty", help="Order quantity", default="0.002")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    trigger_price = validate_price(args.trigger_price)
    limit_price = validate_price(args.limit_price)
    qty = validate_quantity(args.qty)

    client = BinanceFuturesClient()
    sl = StopLimitTrigger(client)
    try:
        result = sl.wait_and_place(symbol, side, qty, trigger_price, limit_price)
        # Clean output
        print("Stop-limit result.")
        print(f"Action: {result.get('action')}")
        print(f"Type: {result.get('type')}")
        print(f"Price: {result.get('price')}")
        print(f"Order ID: {result.get('order', {}).get('orderId')}")
    except Exception as e:
        logger.error("Stop-limit error: %s", e)
        print("Stop-limit failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
