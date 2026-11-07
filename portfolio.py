
import csv
import os
from datetime import datetime

import yfinance as yf

CSV_FILE = "portfolio_summary.csv"

# Store portfolio positions in a dictionary
portfolio = {}


def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("Please enter a value greater than zero.")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a valid number.")


# Fetch the latest available market price
def get_current_price(symbol):
    stock = yf.Ticker(symbol)

    try:
        price = stock.fast_info.get("last_price")
    except Exception:
        price = None

    if price is None:
        history = stock.history(period="5d")

        if history.empty:
            raise ValueError("No market data found for " + symbol)

        price = history["Close"].dropna().iloc[-1]

    if price is None or float(price) <= 0:
        raise ValueError("Unable to retrieve a valid price.")

    return float(price)


# Take portfolio input
def add_stocks():
    print("\n===== ENTER YOUR STOCK DETAILS =====")

    while True:
        symbol = input("\nEnter stock ticker (e.g. AAPL): ").strip().upper()

        if not symbol:
            print("Ticker cannot be empty.")
            continue

        if symbol in portfolio:
            print("This stock has already been entered.")
            continue

        buy_price = get_positive_number("Enter purchase price: ")
        quantity = get_positive_number("Enter number of shares: ")

        portfolio[symbol] = {
            "buy_price": buy_price,
            "quantity": quantity
        }

        print("Stock added successfully!")

        choice = input("Add another stock? (y/n): ").strip().lower()

        if choice != "y":
            break


# Calculate portfolio performance
def calculate_portfolio():
    results = []
    total_invested = 0
    total_value = 0

    print("\n========== PORTFOLIO REPORT ==========")

    for symbol, details in portfolio.items():

        buy_price = details["buy_price"]
        quantity = details["quantity"]

        try:
            current_price = get_current_price(symbol)
        except Exception as error:
            print(f"\nCould not retrieve {symbol}: {error}")
            print("Skipping this stock.")
            continue

        invested = buy_price * quantity
        market_value = current_price * quantity
        profit_loss = market_value - invested

        percentage = (profit_loss / invested) * 100

        total_invested += invested
        total_value += market_value

        results.append({
            "record_type": "HOLDING",
            "ticker": symbol,
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price,
            "invested_value": invested,
            "market_value": market_value,
            "profit_loss": profit_loss,
            "return_percent": percentage
        })

        print(f"\nStock: {symbol}")
        print(f"Purchase Price: ${buy_price:.2f}")
        print(f"Current Price:  ${current_price:.2f}")
        print(f"Quantity:       {quantity:g}")
        print(f"Invested:       ${invested:.2f}")
        print(f"Current Value:  ${market_value:.2f}")
        print(f"Profit/Loss:    ${profit_loss:.2f}")
        print(f"Return:         {percentage:.2f}%")

    if not results:
        print("\nNo stock prices could be retrieved.")
        return

    total_profit = total_value - total_invested
    total_percentage = (total_profit / total_invested) * 100

    print("\n========== TOTAL PORTFOLIO ==========")
    print(f"Total Investment: ${total_invested:.2f}")
    print(f"Current Value:    ${total_value:.2f}")
    print(f"Total Profit/Loss:${total_profit:.2f}")
    print(f"Overall Return:   {total_percentage:.2f}%")

    # Add portfolio summary
    results.append({
        "record_type": "PORTFOLIO_TOTAL",
        "ticker": "ALL",
        "buy_price": "",
        "quantity": "",
        "current_price": "",
        "invested_value": total_invested,
        "market_value": total_value,
        "profit_loss": total_profit,
        "return_percent": total_percentage
    })

    save_to_csv(results)


# Save results into CSV
def save_to_csv(results):
    fields = [
        "timestamp",
        "record_type",
        "ticker",
        "buy_price",
        "quantity",
        "current_price",
        "invested_value",
        "market_value",
        "profit_loss",
        "return_percent"
    ]

    file_exists = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        for result in results:
            result["timestamp"] = timestamp
            writer.writerow(result)

    print(f"\nPerformance successfully saved to {CSV_FILE}")


# Main program
def main():
    print("====================================")
    print("     INVESTMENT PORTFOLIO TRACKER")
    print("====================================")

    add_stocks()
    calculate_portfolio()

    print("\n===== THANK YOU FOR USING THE TRACKER =====")


if __name__ == "__main__":
    main()
