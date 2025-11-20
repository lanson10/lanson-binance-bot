# Lanson Binance Futures Bot

## Setup
1. Create virtualenv and install deps:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Create a `.env` file or export environment variables:
   BINANCE_API_KEY=your_api_key
   BINANCE_API_SECRET=your_api_secret
   # Optional: testnet base url
   BINANCE_BASE_URL=https://testnet.binancefuture.com

3. Examples:
   python src/market_orders.py BTCUSDT BUY 0.001
   python src/limit_orders.py BTCUSDT SELL 0.001 65000

Advanced examples:
   # TWAP (import and call programmatically or create a wrapper CLI)
   # OCO and stop-limit are provided as modules for integration.

## Notes
- This client talks to Binance REST futures endpoints: /fapi/v1/order, /fapi/v1/ticker/price
- Use testnet when testing to avoid real funds.
