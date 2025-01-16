import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# App title
st.title("Stock Pair Correlation Finder")

# Input stock symbol
stock_symbol = st.text_input("Enter a stock symbol (e.g., KO for Coca-Cola):")

# Date range selector
st.write("Select the date range for analysis:")
start_date = st.date_input("Start Date", value=pd.Timestamp("2023-01-01"))
end_date = st.date_input("End Date", value=pd.Timestamp("2023-12-31"))

# Proceed only if a stock symbol and valid date range are provided
if stock_symbol and start_date < end_date:
    # Fetch historical data for the selected stock
    st.write(f"Fetching data for {stock_symbol}...")
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Ensure data is available for the selected stock
    if not stock_data.empty:
        # Display stock chart
        st.write(f"Price trend for {stock_symbol}:")
        st.line_chart(stock_data['Close'], use_container_width=True)

        st.write("Identifying the most correlated stock...")
        
        # List of candidate stocks for correlation
        pair_candidates = ["PEP", "MCD", "PG"]  # Example list (can be expanded)
        correlations = []

        # Calculate correlation with each candidate
        for candidate in pair_candidates:
            candidate_data = yf.download(candidate, start=start_date, end=end_date)['Close']
            if not candidate_data.empty:
                # Align both datasets to the same dates
                combined_data = pd.concat([stock_data['Close'], candidate_data], axis=1).dropna()
                combined_data.columns = [stock_symbol, candidate]

                # Compute correlation
                correlation = np.corrcoef(combined_data[stock_symbol], combined_data[candidate])[0, 1]
                correlations.append((candidate, correlation))

        # Sort pairs by correlation
        sorted_pairs = sorted(correlations, key=lambda x: x[1], reverse=True)

        # Display most correlated stock and correlation value
        most_correlated_stock, highest_correlation = sorted_pairs[0]
        st.write(f"The most correlated stock to {stock_symbol} is {most_correlated_stock} "
                 f"with a correlation value of **{highest_correlation:.2f}**.")

        # Fetch and display the chart for the most correlated stock
        st.write(f"Price trend for {most_correlated_stock}:")
        correlated_stock_data = yf.download(most_correlated_stock, start=start_date, end=end_date)
        st.line_chart(correlated_stock_data['Close'], use_container_width=True)

        # Display both charts side by side for comparison
        st.write("Comparison of Price Trends:")
        combined_data = pd.concat([stock_data['Close'], correlated_stock_data['Close']], axis=1).dropna()
        combined_data.columns = [stock_symbol, most_correlated_stock]
        st.line_chart(combined_data, use_container_width=True)

    else:
        st.error(f"No data found for {stock_symbol}. Please check the stock symbol or try a different date range.")
else:
    st.warning("Please provide a valid stock symbol and date range.")
