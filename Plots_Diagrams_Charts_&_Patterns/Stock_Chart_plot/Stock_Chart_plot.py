import requests
import yfinance as yf
import plotly.graph_objects as go

# Get user inputs
company_name = input("Enter the company name (e.g., Apple): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Get ticker symbol from company name using Yahoo Finance API
url = f"https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={company_name}"
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    # Look for the first stock (equity) match
    for item in data.get('items', []):
        if item.get('type') == 'equity':
            ticker = item['symbol']
            break
    else:
        print("No matching stock ticker symbol found for the given company name.")
        exit()
except requests.exceptions.RequestException as e:
    print(f"Error querying the API: {e}")
    exit()
except ValueError:
    print("Error parsing JSON response.")
    exit()

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
    fig.update_layout(title=f'{company_name} Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)
    fig.show()