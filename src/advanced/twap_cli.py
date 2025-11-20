# src/advanced/twap_cli.py
from __future__ import annotations
import argparse
from ..client import BinanceFuturesClient
from ..advanced.twap import TWAPExecutor
from ..validators import validate_symbol, validate_side, validate_quantity
from ..logger import get_logger

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="TWAP CLI")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("total_qty")
    parser.add_argument("slices", type=int)
    parser.add_argument("duration", type=int)
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    total_qty = validate_quantity(args.total_qty)
    slices = args.slices
    duration = args.duration

    client = BinanceFuturesClient()
    twap = TWAPExecutor(client)
    try:
        summary = twap.run(symbol=symbol, side=side, total_quantity=total_qty, slices=slices, duration_seconds=duration)
        logger.info("TWAP summary: %s", summary)
        print("TWAP summary.")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Total Qty: {total_qty}")
        print(f"Slices: {slices}")
        print(f"Executed slices: {len(summary.get('slices', []))}")
    except Exception as e:
        logger.error("TWAP failed: %s", e)
        print("TWAP failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
