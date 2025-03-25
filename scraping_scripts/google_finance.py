import requests as r
from bs4 import BeautifulSoup
from dataclasses import dataclass
from tabulate import tabulate


# ---------------------------
# Data Classes
# ---------------------------

@dataclass
class Stock:
    """
    Represents a stock with its ticker, exchange, price, and currency.
    Automatically fetches price data upon initialization.
    """
    ticker: str
    exchange: str
    price: float = 0
    currency: str = "USD"
    usd_price: float = 0

    def __post_init__(self):
        """
        Automatically fetches the stock price and currency data upon object creation.
        """
        price_info = get_price_information(self.ticker, self.exchange)

        # If the fetched ticker matches, update stock details
        if price_info["ticker"] == self.ticker:
            self.price = price_info["price"]
            self.currency = price_info["currency"]
            self.usd_price = price_info["usd_price"]


@dataclass
class Position:
    """
    Represents a stock position in a portfolio.
    Holds a reference to a Stock object and the quantity owned.
    """
    stock: Stock
    quantity: int


@dataclass
class Portfolio:
    """
    Represents an investment portfolio holding multiple stock positions.
    """
    positions: list[Position]

    def get_total_value(self):
        """
        Calculates the total value of the portfolio in USD.
        """
        total_value = 0

        # Iterate through all positions and calculate total portfolio value
        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price

        return total_value


# ---------------------------
# Helper Functions
# ---------------------------

def get_fx_to_usd(currency):
    """
    Fetches the foreign exchange rate from Google Finance to convert to USD.

    Args:
        currency (str): The currency code (e.g., "CAD", "EUR").

    Returns:
        float: Exchange rate to USD.
    """
    fx_url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, "html.parser")

    fx_rate = soup.find("div", {"data-last-price": True})
    fx = float(fx_rate["data-last-price"])
    return fx


def get_price_information(ticker, exchange):
    """
    Fetches stock price and currency data from Google Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "MSFT").
        exchange (str): The exchange where the stock is listed (e.g., "NASDAQ").

    Returns:
        dict: Stock information containing price, currency, and USD-equivalent price.
    """
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    # Extract stock price and currency from the webpage
    price_div = soup.find("div", attrs={"data-last-price": True})
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]

    # Convert to USD if necessary
    usd_price = price
    if currency != "USD":
        fx = get_fx_to_usd(currency)
        usd_price = round(price * fx, 2)

    return {
        "ticker": ticker,
        "exchange": exchange,
        "price": price,
        "currency": currency,
        "usd_price": usd_price
    }


def display_portfolio_summary(portfolio):
    """
    Displays a summary of the portfolio, including allocations and total value.

    Args:
        portfolio (Portfolio): The user's portfolio object.
    """
    if not isinstance(portfolio, Portfolio):
        raise TypeError("Please provide an instance of the Portfolio type")

    portfolio_value = portfolio.get_total_value()

    position_data = []

    # Sort positions by market value (largest first)
    for position in sorted(portfolio.positions,
                           key=lambda x: x.quantity * x.stock.usd_price,
                           reverse=True):
        position_data.append([
            position.stock.ticker,
            position.stock.exchange,
            position.quantity,
            position.stock.usd_price,
            position.quantity * position.stock.usd_price,
            position.quantity * position.stock.usd_price / portfolio_value * 100
        ])

    # Print table with stock allocations
    print(tabulate(position_data,
                   headers=["Ticker", "Exchange", "Quantity", "Price", "Market Value", "% Allocation"],
                   tablefmt="psql",
                   floatfmt=".2f"
                   ))

    print(f"Total portfolio value: ${portfolio_value:,.2f}.")


# ---------------------------
# Main Execution
# ---------------------------

if __name__ == "__main__":
    # Define stocks (some in different currencies)
    shop = Stock("SHOP", "TSE")  # CAD
    msft = Stock("MSFT", "NASDAQ")  # USD
    googl = Stock("GOOGL", "NASDAQ")  # USD
    bns = Stock("BNS", "TSE")  # CAD

    # Create positions for the portfolio
    positions = [
        Position(shop, 10),
        Position(msft, 2),
        Position(bns, 100),
        Position(googl, 30)
    ]

    # Create the portfolio object
    portfolio = Portfolio(positions)

    # Display portfolio summary
    display_portfolio_summary(portfolio)
