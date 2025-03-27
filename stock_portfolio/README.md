
# Stock Portfolio Tracker
 Target webpage: [Google Finance]( https://www.google.com/finance/)
 
## Overview
This project allows users to track their stock portfolio, including investments in multiple stocks listed on different exchanges. It automatically fetches the current stock price, converts non-USD prices to USD, and displays a summary of the portfolio, including total value and percentage allocations for each stock.

### Features:
- Fetches live stock price data from Google Finance.
- Supports multiple stock exchanges and currencies.
- Converts stock prices to USD for uniform portfolio analysis.
- Provides a summary of the portfolio with percentage allocations.
- Displays stock data in a user-friendly table format.

### Tools & Technologies

- **Python**: The primary programming language used for the development of the portfolio tracker.
- **Requests**: For making HTTP requests to retrieve stock and exchange data.
- **BeautifulSoup**: For parsing and extracting relevant data from HTML pages.
- **Tabulate**: To format and display the portfolio summary in a clean tabular format.
- **Google Finance**: Used as the source for live stock price and currency data.
- **Data Classes**: Python `dataclass` to manage stock and portfolio objects.

## Usage
1) Create Stock Objects: Create Stock objects with the ticker and exchange details.

2) Create Positions: Define how many shares you own for each stock by creating Position objects.

3) Create Portfolio: Combine all your stock positions into a Portfolio object.

4) Display Portfolio Summary: Use the display_portfolio_summary function to get a detailed portfolio overview.

### Example Usage:


- first configure the ``` if __name__ == "__main__":``` section of the script then:
```bash
python stock_portfolio.py
```

## Output:
This will display a summary of your portfolio in a tabular format:

```pgsql
Copy
Edit
+--------+-----------+----------+--------+--------------+-----------------+
| Ticker | Exchange  | Quantity | Price  | Market Value | % Allocation    |
+--------+-----------+----------+--------+--------------+-----------------+
| MSFT   | NASDAQ    |        2 | 318.99 |     637.98   | 15.62           |
| GOOGL  | NASDAQ    |       30 | 2763.74|    82912.20  | 78.56           |
| SHOP   | TSE       |       10 | 1592.34|    15923.40  | 4.47            |
| BNS    | TSE       |      100 | 106.73 |     10673.00 | 1.72            |
+--------+-----------+----------+--------+--------------+-----------------+

Total portfolio value: $105,146.58.
```

##  How It Works
- The Stock class fetches live stock price data using the get_price_information function from Google Finance. If the stock is not priced in USD, the price is converted to USD using the current exchange rate from Google Finance.

- The Portfolio class holds multiple Position objects and calculates the total portfolio value in USD.

- The display_portfolio_summary function outputs the stock positions, including the percentage allocation, and displays the total portfolio value.
