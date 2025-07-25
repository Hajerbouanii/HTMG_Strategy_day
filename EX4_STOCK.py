# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:13:46 2025

@author: BSmeaton
"""
# pip install yfinance matplotlib

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import yfinance as yf

# === CONFIGURABLE VARIABLES ===
stock_symbol = "HTWS.L"  # <-- Change this to any valid ticker
num_years = 5  # <-- Change this to desired number of years

# === DATE RANGE SETUP ===
end_date = datetime.today()
start_date = end_date - timedelta(days=365 * num_years)

# === FETCH DATA ===
ticker = yf.Ticker(stock_symbol)
data = ticker.history(
    start=start_date.strftime("%Y-%m-%d"),
    end=end_date.strftime("%Y-%m-%d"),
    interval="1d",
)

# === PLOT DATA ===
if data.empty:
    print(
        f"No data found for {stock_symbol}. Please check the symbol or your connection."
    )
else:
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label=f"{stock_symbol} Close Price")
    plt.title(f"{stock_symbol} Daily Closing Price - Last {num_years} Years")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
