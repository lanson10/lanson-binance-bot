# src/advanced/oco.py
from __future__ import annotations
import time
from typing import Dict, Any
from ..client import BinanceFuturesClient
from ..validators import validate_symbol, validate_side, validate_quantity, validate_price
from ..logger import get_logger

logger = get_logger(__name__)

class OCOExecutor:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def run(self, symbol: str, side: str, quantity: float, tp_price: float, stop_price: float, stop_limit_price: float, poll_interval: float = 2.0) -> Dict[str, Any]:
        """
        Place a take-profit limit order and a stop-limit stop-loss. Poll for fills.
        tp_price: price for limit take-profit
        stop_price: trigger price for stop
        stop_limit_price: limit price for stop-limit (can equal stop_price or slightly worse)
        """
        logger.info("Placing OCO style pair")
        # Place take-profit limit
        tp_side = "SELL" if side == "BUY" else "BUY"
        tp = self.client.place_limit_order(symbol=symbol, side=tp_side, price=tp_price, quantity=quantity)
        logger.info(f"TP order response: {tp}")

        # Place stop-limit: use STOP type with stopPrice and price
        stop = self.client.place_order(symbol=symbol, side=tp_side, order_type="STOP", quantity=quantity, price=stop_limit_price, stop_price=stop_price, time_in_force="GTC")
        logger.info(f"Stop-limit order response: {stop}")

        tp_id = tp.get("orderId")
        stop_id = stop.get("orderId")

        # Poll to see which executes
        path_status = "/fapi/v2/order"  # fetch order by symbol & orderId (we will reuse client._request directly)
        start = time.time()
        timeout = 3600  # 1 hour max by default
        filled = None
        while time.time() - start < timeout:
            try:
                tp_status = self.client._request("GET", "/fapi/v2/order", params={"symbol": symbol, "orderId": tp_id}, signed=False)
                stop_status = self.client._request("GET", "/fapi/v2/order", params={"symbol": symbol, "orderId": stop_id}, signed=False)
            except Exception as e:
                logger.error("Error querying order status: %s", e)
                time.sleep(poll_interval)
                continue

            if float(tp_status.get("executedQty", 0)) > 0:
                filled = ("tp", tp_status)
                logger.info("TP filled, cancelling stop order")
                try:
                    self.client._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": stop_id}, signed=True)
                except Exception as e:
                    logger.error("Failed to cancel stop order: %s", e)
                break

            if float(stop_status.get("executedQty", 0)) > 0:
                filled = ("stop", stop_status)
                logger.info("Stop filled, cancelling tp order")
                try:
                    self.client._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": tp_id}, signed=True)
                except Exception as e:
                    logger.error("Failed to cancel TP order: %s", e)
                break

            time.sleep(poll_interval)

        return {"filled": filled}
