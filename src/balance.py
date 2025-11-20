# src/balance.py
from __future__ import annotations
from .client import BinanceFuturesClient
from .logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        client = BinanceFuturesClient()
        data = client._request("GET", "/fapi/v2/balance", params={}, signed=True)
        usdt = next((d for d in data if d.get("asset") == "USDT"), None)
        logger.info("Balance fetched: %s", usdt or data)
        print("Futures wallet summary.")
        if usdt:
            print(f"Asset: USDT, Balance: {usdt.get('balance')}, Available: {usdt.get('withdrawAvailable')}")
        else:
            print("Balance data:", data)
    except Exception as e:
        logger.error("Balance fetch failed: %s", e)
        print("Balance fetch failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
