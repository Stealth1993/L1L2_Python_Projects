import pandas_datareader.data as web
import datetime as dt
import mplfinance as mpf
import pandas as pd # Often needed when working with pandas_datareader

# Define the ticker symbol and the date range
symbol = input("Enter Stock Name (e.g., AAPL, MSFT, GOOGL): ")

# Define the date range using datetime objects
start_date = dt.datetime(2023, 1, 1)
end_date = dt.datetime(2025, 4, 4)

# --- Fetch Stock Data using pandas_datareader ---
try:
    # Attempt to fetch data from Yahoo Finance using pandas_datareader
    # Other data_source options might be available depending on pandas_datareader version
    data = web.DataReader(symbol, data_source='stooq', start=start_date, end=end_date)

except Exception as e:
    print(f"Error fetching data for {symbol}: {e}")
    print("Please check the ticker symbol and your internet connection.")
    exit() # Exit the program if data fetching fails

# --- Create a candlestick chart ---
# Check if data was fetched successfully and has the expected format
if not data.empty and isinstance(data.index, pd.DatetimeIndex):
    print(f"Successfully fetched data for {symbol}.")
    # mplfinance requires specific column names (Open, High, Low, Close, Volume)
    # pandas_datareader from yahoo typically provides these.

    try:
        mpf.plot(data,
                 type='candle',
                 style='charles', # You can choose different styles
                 title=f'{symbol} Candlestick Chart ({start_date.year} to {end_date.year})',
                 ylabel='Price',
                 volume=True, # Display volume sub-plot
                 show_nontrading=False # Do not show gaps for non-trading days
                )
    except Exception as e:
        print(f"Error creating candlestick chart: {e}")
        print("Please ensure the fetched data has 'Open', 'High', 'Low', 'Close', and 'Volume' columns.")

else:
    print(f"Could not fetch valid data for {symbol} in the specified date range or data format is incorrect.")
    print("Data fetched (first 5 rows):")
    print(data.head()) # Print the head of the fetched data to inspect its format