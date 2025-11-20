import os
import sys
import subprocess

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def run(cmd: str):
    print(f"\n>>> Running: {cmd}\n")
    subprocess.call(cmd, shell=True)
    print("\n----------------------------------------\n")
    input("Press Enter to continue...")


def menu():
    clear()
    print("""
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
    """)

    choice = input("Enter your choice: ").strip()
    return choice


def main():
    while True:
        choice = menu()

        if choice == "1":
            # Market Order
            symbol = input("Symbol (example: BTCUSDT): ")
            side = input("Side (BUY/SELL): ").upper()
            qty = input("Quantity: ")
            run(f"python -m src.market_orders {symbol} {side} {qty}")

        elif choice == "2":
            # Limit Order
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            qty = input("Quantity: ")
            price = input("Limit Price: ")
            run(f"python -m src.limit_orders {symbol} {side} {qty} {price}")

        elif choice == "3":
            # Close Position
            symbol = input("Symbol: ")
            run(f"python -m src.close_position {symbol}")

        elif choice == "4":
            # Price
            symbol = input("Symbol: ")
            run(f"python -m src.price {symbol}")

        elif choice == "5":
            # Exchange Info
            symbol = input("Symbol: ")
            run(f"python -m src.exchange_info {symbol}")

        elif choice == "6":
            # OCO
            symbol = input("Symbol: ")
            side = input("Entry Side (BUY/SELL): ").upper()
            qty = input("Quantity: ")
            tp = input("Take-Profit price: ")
            stop_price = input("Stop price: ")
            stop_limit = input("Stop-limit price: ")
            run(f"python -m src.advanced.oco_cli {symbol} {side} {qty} {tp} {stop_price} {stop_limit}")

        elif choice == "7":
            # Stop-Limit
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            trigger = input("Trigger Price: ")
            limit_price = input("Limit Price: ")
            qty = input("Quantity: ")
            run(f"python -m src.advanced.stop_limit {symbol} {side} {trigger} {limit_price} --qty {qty}")

        elif choice == "8":
            # TWAP
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            total_qty = input("Total Quantity: ")
            slices = input("Number of slices: ")
            interval = input("Seconds between slices: ")
            run(f"python -m src.advanced.twap_cli {symbol} {side} {total_qty} {slices} {interval}")

        elif choice == "9":
            # Grid
            symbol = input("Symbol: ")
            lower = input("Lower Range: ")
            upper = input("Upper Range: ")
            levels = input("Number of levels: ")
            qty = input("Quantity per level: ")
            run(f"python -m src.advanced.grid_cli {symbol} {lower} {upper} {levels} {qty}")

        elif choice == "10":
            # Cancel Order
            symbol = input("Symbol: ")
            order_id = input("Order ID: ")
            run(f"python -m src.cancel_order {symbol} {order_id}")

        elif choice == "11":
            # Cancel ALL Orders
            symbol = input("Symbol: ")
            run(f"python -m src.cancel_all {symbol}")

        elif choice == "12":
            # Positions
            run("python -m src.positions")

        elif choice == "13":
            # Balance
            run("python -m src.balance")

        elif choice == "14":
            # Open orders
            symbol = input("Symbol: ")
            run(f"python -m src.open_orders {symbol}")

        elif choice == "0":
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Try again.")
            input("Press Enter...")


if __name__ == "__main__":
    main()
