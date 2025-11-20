# src/close_position.py
from __future__ import annotations
import argparse
from .client import BinanceFuturesClient
from .validators import validate_symbol
from .logger import get_logger

logger = get_logger(__name__)

def get_position_info(client: BinanceFuturesClient, symbol: str):
    data = client._request("GET", "/fapi/v2/positionRisk", params={"symbol": symbol}, signed=True)
    return data[0] if isinstance(data, list) and data else None

def main():
    parser = argparse.ArgumentParser(description="Close open futures position (market, reduce-only)")
    parser.add_argument("symbol", help="Symbol, e.g., BTCUSDT")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    client = BinanceFuturesClient()
    try:
        position = get_position_info(client, symbol)
        if not position:
            print("No position found.")
            return

        position_amt = float(position.get("positionAmt", 0))
        if position_amt == 0:
            print("No open position.")
            return

        side = "SELL" if position_amt > 0 else "BUY"
        qty = abs(position_amt)

        logger.info("Attempting to close position: %s %s qty=%s", symbol, side, qty)
        resp = client.place_order(symbol=symbol, side=side, order_type="MARKET", quantity=qty, reduce_only=True)
        logger.info("Close position response: %s", resp)

        # Re-check position
        updated = get_position_info(client, symbol)
        new_amt = float(updated.get("positionAmt", 0)) if updated else 0.0

        print("Position close result.")
        print(f"Side: {side}")
        print(f"Qty: {qty}")
        print(f"Result: {'SUCCESS' if new_amt == 0 else 'PARTIAL' if new_amt != 0 else 'UNKNOWN'}")
        print(f"Final position size: {new_amt}")
        if new_amt == 0:
            print("Note: Position successfully closed.")
    except Exception as e:
        logger.error("Failed to close position: %s", e)
        print("Close position failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
