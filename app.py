import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.title("Stock Pair Correlation Finder")

# Input from user for the stock symbol
stock_symbol = st.text_input("Enter a stock symbol (e.g., KO for Coca-Cola):")

# If user provides a stock symbol
if stock_symbol:
    # Download historical data for the input stock
    stock_data = yf.download(stock_symbol, period="1y")

    # Display stock chart
    st.line_chart(stock_data['Close'], use_container_width=True)

    st.write("Looking for highly correlated pairs...")
    
    # Simulating pair correlation with dummy stocks for demonstration
    pair_candidates = ["PEP", "MCD", "PG"]
    correlations = []
    
    # Download data for correlation analysis
    for candidate in pair_candidates:
        candidate_data = yf.download(candidate, period="1y")['Close']
        correlation = np.corrcoef(stock_data['Close'], candidate_data)[0, 1]
        correlations.append((candidate, correlation))
    
    # Sort pairs by correlation
    sorted_pairs = sorted(correlations, key=lambda x: x[1], reverse=True)
    
    # Display most correlated pair
    st.write(f"The most correlated stock to {stock_symbol} is:", sorted_pairs[0])

