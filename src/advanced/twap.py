# src/advanced/twap.py
from __future__ import annotations
import time
from typing import Dict, Any
from ..client import BinanceFuturesClient
from ..logger import get_logger

logger = get_logger(__name__)

class TWAPExecutor:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def run(self, symbol: str, side: str, total_quantity: float, slices: int, duration_seconds: int) -> Dict[str, Any]:
        if slices <= 0:
            raise ValueError("slices must be > 0")
        slice_qty = float(total_quantity) / slices
        interval = duration_seconds / slices
        results = []
        logger.info(f"Running TWAP: {slices} slices every {interval:.2f}s of {slice_qty} each.")
        for i in range(slices):
            try:
                r = self.client.place_market_order(symbol=symbol, side=side, quantity=slice_qty)
                results.append(r)
                logger.info(f"TWAP slice {i+1}/{slices} placed")
            except Exception as e:
                logger.error(f"Failed to place TWAP slice {i+1}: {e}")
                results.append({"error": str(e)})
            time.sleep(interval)
        return {"results": results}
