import requests
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# Cache to store company name to ticker symbol mappings
ticker_cache = {}

def get_ticker(company_name):
    # Check if the ticker is already cached
    if company_name in ticker_cache:
        return ticker_cache[company_name]
    
    # API URL to search for the ticker symbol
    url = f"https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={company_name}"
    for attempt in range(3):  # Try up to 3 times
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an error for bad responses
            data = response.json()
            for item in data.get('items', []):
                if item.get('type') == 'equity':
                    ticker = item['symbol']
                    ticker_cache[company_name] = ticker  # Cache the ticker
                    return ticker
            print("No matching stock ticker symbol found for the given company name.")
            exit()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                if attempt < 2:
                    print("Rate limit exceeded. Waiting 10 seconds to retry...")
                    time.sleep(10)
                else:
                    print("Rate limit exceeded. Please try again later.")
                    exit()
            else:
                print(f"Error querying the API: {e}")
                exit()
        except requests.exceptions.RequestException as e:
            print(f"Error querying the API: {e}")
            exit()
        except ValueError:
            print("Error parsing JSON response.")
            exit()
    return None

# Get user inputs
company_name = input("Enter the company name (e.g., Apple): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Get ticker symbol
ticker = get_ticker(company_name)
if ticker is None:
    print("Failed to retrieve ticker symbol.")
    exit()

# Check if end date is in the future
current_date = datetime.now().date()
end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
if end_date_dt > current_date:
    print(f"Note: The end date {end_date} is in the future. Data will be fetched up to the current date.")

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