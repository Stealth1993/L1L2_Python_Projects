import yfinance as yf
import mplfinance as mpf

# Get user inputs
ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Fetch historical data from Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)

# Check if data was retrieved successfully
if data.empty:
    print("No data found for the given ticker and date range.")
else:
    # Plot the candlestick chart using mplfinance
    mpf.plot(data, type='candle', title=f'{ticker} Stock Price', style='yahoo')