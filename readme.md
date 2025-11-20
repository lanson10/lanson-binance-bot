# Lanson Binance Futures Bot

A complete Binance Futures automated trading bot supporting market orders, limit orders, stop-limit, OCO, TWAP execution, grid strategy, position management, and more.
All API calls log to bot.log for debugging and validation.

Setup
1. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt

2. Create .env file

BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# Optional Testnet endpoint
BINANCE_BASE_URL=https://testnet.binancefuture.com

3. Basic Examples
python -m src.market_orders BTCUSDT BUY 0.001
python -m src.limit_orders BTCUSDT SELL 0.001 65000

Running the Full Bot (Menu-Based CLI)

To run the complete menu-based interface with all features:

python bot.py


This opens the interactive menu:

========================================
        BINANCE FUTURES BOT MENU
========================================
1) Market Order
2) Limit Order
3) Close Position (Market)
4) View Price
5) Exchange Info
6) OCO (TP + SL)
7) Stop-Limit Trigger
8) TWAP Orders
9) Grid Strategy
10) Cancel Single Order
11) Cancel ALL Orders
12) View Positions
13) View Balance
14) View Open Orders
0) Exit
========================================


Choose any option and follow the prompts.

All Supported Commands (Direct Terminal)
1. Market Order
python -m src.market_orders <symbol> <BUY/SELL> <quantity>


Example:

python -m src.market_orders BTCUSDT BUY 0.002

2. Limit Order
python -m src.limit_orders <symbol> <BUY/SELL> <quantity> <price>

3. Close Position (Market)
python -m src.close_position <symbol>

4. Check Current Price
python -m src.price <symbol>

5. Exchange Info (filters, step sizes, limits)
python -m src.exchange_info <symbol>

6. View Open Orders
python -m src.open_orders <symbol>

7. View Positions
python -m src.positions

8. View Balance
python -m src.balance

9. Cancel a Single Order
python -m src.cancel_order <symbol> <orderId>

10. Cancel ALL Orders
python -m src.cancel_all <symbol>

Advanced Features
A) Stop-Limit Trigger Watcher

Places a limit order when price reaches trigger.

python -m src.advanced.stop_limit <symbol> <BUY/SELL> <trigger_price> <limit_price> --qty <quantity>


Example:

python -m src.advanced.stop_limit BTCUSDT BUY 95000 94800 --qty 0.002

B) OCO (Take Profit + Stop Loss)
python -m src.advanced.oco_cli <symbol> <BUY/SELL> <qty> <tp_price> <stop_price> <stop_limit_price>


Example:

python -m src.advanced.oco_cli BTCUSDT BUY 0.002 95000 92000 91800

C) TWAP (Time Weighted Average Price)

Splits orders evenly across time.

python -m src.advanced.twap_cli <symbol> <BUY/SELL> <total_qty> <parts> <delay_seconds>


Example:

python -m src.advanced.twap_cli BTCUSDT BUY 0.02 5 60

D) Grid Trading Bot

Automatically buys low and sells high in a range.

python -m src.advanced.grid_cli <symbol> <lower_price> <upper_price> <grid_count> <quantity>


Example:

python -m src.advanced.grid_cli BTCUSDT 88000 94000 6 0.0005

Logging

Every API call is logged to:

bot.log


Logs include:

Timestamp

Endpoint

Parameters

Responses

Errors

These logs are required for assignment verification.

Notes

The bot uses Binance Futures REST API endpoints such as:

/fapi/v1/order

/fapi/v1/ticker/price

/fapi/v2/positionRisk

For safety, always test using Binance Futures Testnet.

Ensure system time is synced to avoid -1021 timestamp errors.


Author

Lanson
Binance Futures Automated Trading Bot Assignment
MCA Student
