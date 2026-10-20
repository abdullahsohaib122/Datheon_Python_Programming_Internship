
import csv
import os
# Sample current prices only — not live market prices
current_prices = {
    "AAPL": 220.00,
    "MSFT": 510.00,
    "GOOGL": 250.00,
    "AMZN": 230.00,
    "TSLA": 350.00
}

portfolio = {}

print("=" * 45)
print("       INVESTMENT PORTFOLIO TRACKER")
print("=" * 45)
print("Available sample tickers:", ", ".join(current_prices))

while True:
    ticker = input("\nEnter stock ticker (or 'done' to finish): ").strip().upper()

    if ticker == "DONE":
        break

    if ticker not in current_prices:
        print("Ticker not found. Please choose from the listed symbols.")
        continue

    try:
        buy_price = float(input("Enter your buying price per share: "))
        quantity = int(input("Enter number of shares: "))

        if buy_price <= 0 or quantity <= 0:
            print("Price and quantity must be greater than zero.")
            continue

    except ValueError:
        print("Invalid input. Enter a valid price and whole-number quantity.")
        continue

    if ticker in portfolio:
        old = portfolio[ticker]
        old_quantity = old["quantity"]
        new_quantity = old_quantity + quantity

        old["buy_price"] = (
            old["buy_price"] * old_quantity + buy_price * quantity
        ) / new_quantity
        old["quantity"] = new_quantity
    else:
        portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity
        }

if not portfolio:
    print("\nNo stocks were added. No summary was created.")
else:
    total_invested = 0
    total_market_value = 0
    summary_rows = []

    print("\n" + "=" * 75)
    print("PORTFOLIO SUMMARY")
    print("=" * 75)
    print(
        f"{'Ticker':<10}{'Shares':>8}{'Buy Price':>13}"
        f"{'Current':>12}{'Gain/Loss':>14}{'Return %':>12}"
    )
    print("-" * 75)

    for ticker, details in portfolio.items():
        buy_price = details["buy_price"]
        quantity = details["quantity"]
        current_price = current_prices[ticker]

        invested = buy_price * quantity
        market_value = current_price * quantity
        gain_loss = market_value - invested
        percentage = (gain_loss / invested) * 100

        total_invested += invested
        total_market_value += market_value

        print(
            f"{ticker:<10}{quantity:>8}{buy_price:>13.2f}"
            f"{current_price:>12.2f}{gain_loss:>14.2f}"
            f"{percentage:>11.2f}%"
        )

        summary_rows.append({
            "Ticker": ticker,
            "Quantity": quantity,
            "Buy Price": round(buy_price, 2),
            "Current Price (Sample)": round(current_price, 2),
            "Invested Amount": round(invested, 2),
            "Current Market Value": round(market_value, 2),
            "Gain/Loss": round(gain_loss, 2),
            "Return Percentage": round(percentage, 2)
        })

    total_gain_loss = total_market_value - total_invested
    overall_return = (total_gain_loss / total_invested) * 100

    print("-" * 75)
    print(f"Total invested:       ${total_invested:.2f}")
    print(f"Current market value: ${total_market_value:.2f}")
    print(f"Total gain/loss:      ${total_gain_loss:.2f}")
    print(f"Overall return:        {overall_return:.2f}%")

   
csv_filename = "portfolio_summary.csv"

file_exists = os.path.exists(csv_filename)
file_is_empty = not file_exists or os.path.getsize(csv_filename) == 0

with open(
    csv_filename,
    "a",
    newline="",
    encoding="utf-8"
) as csv_file:
    fieldnames = summary_rows[0].keys()

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if file_is_empty:
        writer.writeheader()

    writer.writerows(summary_rows)

print("\nNew records added to portfolio_summary.csv")

