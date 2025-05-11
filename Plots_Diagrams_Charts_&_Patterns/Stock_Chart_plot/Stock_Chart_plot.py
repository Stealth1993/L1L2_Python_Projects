import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Fetch historical data from Yahoo Finance
data = yf.download(ticker, start=start_date, end=end_date)
if data.empty:
    print("No data found for the given ticker and date range.")
else:
    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                          open=data['Open'],
                                          high=data['High'],
                                          low=data['Low'],
                                          close=data['Close'])])

    # Update layout
    fig.update_layout(title=f'{ticker} Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)

    # Show the chart
    fig.show()