# src/advanced/grid_cli.py
from __future__ import annotations
import argparse
from typing import List
from ..client import BinanceFuturesClient
from ..validators import validate_symbol, validate_quantity
from ..logger import get_logger

logger = get_logger(__name__)

def generate_grid_prices(lower: float, upper: float, steps: int) -> List[float]:
    step_size = (upper - lower) / steps
    return [round(lower + i * step_size, 8) for i in range(steps + 1)]

def main():
    parser = argparse.ArgumentParser(description="Simple Grid CLI")
    parser.add_argument("symbol")
    parser.add_argument("lower", type=float)
    parser.add_argument("upper", type=float)
    parser.add_argument("levels", type=int)
    parser.add_argument("qty_per_order")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    lower = args.lower
    upper = args.upper
    levels = args.levels
    qty = validate_quantity(args.qty_per_order)

    client = BinanceFuturesClient()
    prices = generate_grid_prices(lower, upper, levels)
    placed = []
    for p in prices:
        try:
            buy = client.place_limit_order(symbol=symbol, side="BUY", price=p, quantity=qty)
            sell = client.place_limit_order(symbol=symbol, side="SELL", price=p, quantity=qty)
            placed.append((p, buy.get("orderId"), sell.get("orderId")))
            logger.info("Grid placed at %s: buy=%s sell=%s", p, buy, sell)
        except Exception as e:
            logger.error("Grid placement failed at %s: %s", p, e)

    print("Grid placement summary.")
    print(f"Symbol: {symbol}")
    print(f"Levels: {levels}")
    print("Placed orders:")
    for p, b, s in placed:
        print(f"Price: {p}, Buy ID: {b}, Sell ID: {s}")

if __name__ == "__main__":
    main()
