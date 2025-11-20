# src/positions.py
from __future__ import annotations
from .client import BinanceFuturesClient
from .logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        client = BinanceFuturesClient()
        data = client._request("GET", "/fapi/v2/positionRisk", params={}, signed=True)
        non_zero = [p for p in data if float(p.get("positionAmt", 0)) != 0.0]
        logger.info("Positions fetched: %s", non_zero)
        print("Open positions summary.")
        if non_zero:
            for p in non_zero:
                print(f"Symbol: {p.get('symbol')}, Amt: {p.get('positionAmt')}, Entry: {p.get('entryPrice')}, UnPnL: {p.get('unRealizedProfit')}")
        else:
            print("No open positions.")
    except Exception as e:
        logger.error("Failed to fetch positions: %s", e)
        print("Positions fetch failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
