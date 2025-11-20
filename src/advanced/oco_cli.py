# src/advanced/oco_cli.py
from __future__ import annotations
import argparse
import time
from ..client import BinanceFuturesClient
from ..validators import validate_symbol, validate_side, validate_quantity, validate_price
from ..logger import get_logger

logger = get_logger(__name__)

class OCOExecutorCLI:
    def __init__(self, client: BinanceFuturesClient, poll_interval: float = 2.0, timeout: int = 3600):
        self.client = client
        self.poll_interval = poll_interval
        self.timeout = timeout

    def run(self, symbol: str, side: str, quantity: float, tp_price: float, stop_price: float, stop_limit_price: float):
        exit_side = "SELL" if side == "BUY" else "BUY"

        logger.info("Placing TP order for OCO")
        tp_resp = self.client.place_limit_order(symbol=symbol, side=exit_side, price=tp_price, quantity=quantity)
        tp_id = tp_resp.get("orderId")
        logger.info("TP resp: %s", tp_resp)

        logger.info("Placing stop-limit for OCO")
        stop_resp = None
        try:
            stop_resp = self.client.place_order(symbol=symbol, side=exit_side, order_type="STOP", quantity=quantity,
                                               price=stop_limit_price, stop_price=stop_price, time_in_force="GTC")
        except Exception as e:
            logger.error("Stop placement failed: %s", e)
            raise

        stop_id = stop_resp.get("orderId")
        logger.info("Stop resp: %s", stop_resp)

        start = time.time()
        filled = None
        while time.time() - start < self.timeout:
            tp_status = self.client._request("GET", "/fapi/v1/order", params={"symbol": symbol, "orderId": tp_id}, signed=True)
            stop_status = self.client._request("GET", "/fapi/v1/order", params={"symbol": symbol, "orderId": stop_id}, signed=True)

            tp_executed = float(tp_status.get("executedQty", 0))
            stop_executed = float(stop_status.get("executedQty", 0))

            if tp_executed > 0:
                filled = ("TP", tp_status)
                try:
                    self.client._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": stop_id}, signed=True)
                except Exception as e:
                    logger.error("Failed cancel stop: %s", e)
                break

            if stop_executed > 0:
                filled = ("STOP", stop_status)
                try:
                    self.client._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": tp_id}, signed=True)
                except Exception as e:
                    logger.error("Failed cancel tp: %s", e)
                break

            time.sleep(self.poll_interval)

        # Clean output
        print("OCO result.")
        print(f"TP price: {tp_price}, TP order id: {tp_id}")
        print(f"Stop trigger: {stop_price}, Stop-limit price: {stop_limit_price}, Stop order id: {stop_id}")
        print(f"Result: {filled[0] if filled else 'NO_FILL'}")
        if filled:
            print(f"Filled Order ID: {filled[1].get('orderId')}")
        return {"tp": tp_resp, "stop": stop_resp, "result": filled}

def main():
    parser = argparse.ArgumentParser(description="OCO CLI")
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("qty")
    parser.add_argument("tp_price")
    parser.add_argument("stop_price")
    parser.add_argument("stop_limit_price")
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    side = validate_side(args.side)
    qty = validate_quantity(args.qty)
    tp_price = validate_price(args.tp_price)
    stop_price = validate_price(args.stop_price)
    stop_limit_price = validate_price(args.stop_limit_price)

    client = BinanceFuturesClient()
    oco = OCOExecutorCLI(client)
    try:
        oco.run(symbol, side, qty, tp_price, stop_price, stop_limit_price)
    except Exception as e:
        logger.error("OCO failed: %s", e)
        print("OCO failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
