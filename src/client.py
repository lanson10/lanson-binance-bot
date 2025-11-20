# src/client.py
from __future__ import annotations
import os
import time
import hmac
import hashlib
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from .logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)


class BinanceFuturesClient:
    """
    Minimal Binance USDT-M Futures client with timestamp synchronization.
    """

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url or os.getenv("BINANCE_BASE_URL", "https://fapi.binance.com")
        if not self.api_key or not self.api_secret:
            logger.error("API key/secret not provided. Set BINANCE_API_KEY and BINANCE_API_SECRET.")
            raise ValueError("API key/secret missing")
        # time offset between server and local (ms)
        self.time_offset = 0
        try:
            self._sync_time()
        except Exception as e:
            # don't fail hard — keep offset 0 but log
            logger.warning("Failed to sync server time: %s — continuing with local time", e)

    def _sync_time(self) -> None:
        """
        Query Binance server time and compute offset (server_time - local_time).
        This avoids timestamp errors (-1021).
        """
        try:
            url = self.base_url + "/fapi/v1/time"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            server_time = int(data.get("serverTime", 0))
            local_time = int(time.time() * 1000)
            self.time_offset = server_time - local_time
            logger.info("Time synced. server_time=%s local_time=%s offset=%sms", server_time, local_time, self.time_offset)
        except Exception as e:
            logger.error("Error syncing time: %s", e)
            raise

    def _sign(self, params: Dict[str, Any]) -> str:
        query = urlencode(params, doseq=True)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        return signature

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, signed: bool = False) -> Dict[str, Any]:
        url = self.base_url.rstrip("/") + path
        params = params.copy() if params else {}
        headers = {"X-MBX-APIKEY": self.api_key}
        if signed:
            # correct timestamp using server offset
            ts = int(time.time() * 1000 + getattr(self, "time_offset", 0))
            params["timestamp"] = ts
            params["recvWindow"] = params.get("recvWindow", 5000)
            signature = self._sign(params)
            params["signature"] = signature

        method = method.upper()
        try:
            if method == "GET":
                resp = requests.get(url, params=params, headers=headers, timeout=15)
            elif method == "POST":
                resp = requests.post(url, params=params, headers=headers, timeout=15)
            elif method == "DELETE":
                resp = requests.delete(url, params=params, headers=headers, timeout=15)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # try parse json
            try:
                data = resp.json()
            except Exception:
                resp.raise_for_status()
                data = {}

            if resp.status_code >= 400:
                logger.error("HTTP %s error: %s", resp.status_code, data)
                raise RuntimeError(f"Binance API error: {data}")

            logger.info("Request %s %s params=%s response=%s", method, path, params, data)
            return data
        except requests.RequestException as e:
            logger.error("Network error: %s", e)
            raise

    # Public helpers
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None,
                    time_in_force: Optional[str] = None, reduce_only: bool = False, stop_price: Optional[float] = None) -> Dict[str, Any]:
        path = "/fapi/v1/order"
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": float(quantity),
        }
        if price is not None:
            params["price"] = float(price)
        if time_in_force:
            params["timeInForce"] = time_in_force
        if reduce_only:
            params["reduceOnly"] = "true"
        if stop_price is not None:
            params["stopPrice"] = float(stop_price)

        return self._request("POST", path, params=params, signed=True)

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        return self.place_order(symbol=symbol, side=side, order_type="MARKET", quantity=quantity)

    def place_limit_order(self, symbol: str, side: str, price: float, quantity: float, time_in_force: str = "GTC") -> Dict[str, Any]:
        return self.place_order(symbol=symbol, side=side, order_type="LIMIT", price=price, quantity=quantity, time_in_force=time_in_force)

    def get_symbol_price(self, symbol: str) -> Dict[str, Any]:
        path = "/fapi/v1/ticker/price"
        return self._request("GET", path, params={"symbol": symbol}, signed=False)
