
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta
import time

def fetch_data(tickers, start_date, end_date):
    """Fetch stock data for given tickers and date range"""
    data = pd.DataFrame()
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
            data[ticker] = stock_data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
    return data

def create_stock_graphs(df):
    """Create and display stock visualizations"""
    st.subheader("Stock Price Visualization")
    graph_type = st.radio(
        "Select Graph Type",
        ["Combined Graph", "Individual Graphs"],
        horizontal=True
    )
    
    auto_refresh = st.checkbox("Enable Auto-refresh (30 seconds)", value=True)
        # Display key metrics
    st.subheader("Current Stock Metrics")
    metrics_cols = st.columns(len(df.columns))
    for idx, column in enumerate(df.columns):
        with metrics_cols[idx]:
            current_price = df[column].iloc[-1]
            price_change = df[column].iloc[-1] - df[column].iloc[-2]
            percent_change = (price_change / df[column].iloc[-2]) * 100
                
            st.metric(
                label=column,
                value=f"${current_price:.2f}",
                delta=f"{percent_change:.2f}%"
            )
    if df is not None:
        normalized_df = df.div(df.iloc[0]) * 100  # Normalize data for comparison
        
        if graph_type == "Combined Graph":
            fig = go.Figure()
            for column in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=normalized_df[column],
                        name=column,
                        mode='lines'
                    )
                )
            fig.update_layout(
                title="Normalized Stock Prices (Base=100)",
                xaxis_title="Date",
                yaxis_title="Normalized Price",
                height=600,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            cols = st.columns(2)
            for idx, column in enumerate(df.columns):
                with cols[idx % 2]:
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df[column],
                            name=column,
                            mode='lines'
                        )
                    )
                    fig.update_layout(
                        title=f"{column} Stock Price",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

        if auto_refresh:
            time.sleep(30)
            st.rerun()

def create_stock_summary(df):
    """Display Stock Summary"""
    st.subheader("Stock Summary")
    if df is not None:
        for column in df.columns:
            st.write(f"**{column}**")
            current_price = df[column].iloc[-1]
            prev_close = df[column].iloc[-2]
            price_change = current_price - prev_close
            percent_change = (price_change / prev_close) * 100

            summary_data = {
                "Metric": [
                    "Open", "Prev. Close", "Today's Low", "Today's High",
                    "52-Wk Low", "52-Wk High", "Current Price", "Change"
                ],
                "Value": [
                    f"${current_price:.2f}", f"${prev_close:.2f}",
                    f"${df[column].min():.2f}", f"${df[column].max():.2f}",
                    f"${df[column].min():.2f}", f"${df[column].max():.2f}",
                    f"${current_price:.2f}", f"{percent_change:.2f}%"
                ]
            }

            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df)

def main():
    # Page configuration
    st.set_page_config(
        page_title="Financial Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

 

    
    st.title("Financial Risk Analysis Dashboard")
    
    # Sidebar
    st.sidebar.title("Portfolio Configuration")
    
    default_stocks = {'AAPL': 'Apple', 'GOOGL': 'Google', 'AMZN': 'Amazon', 'META': 'Meta'}
    default_end_date = date.today()
    default_start_date = default_end_date - timedelta(days=365)
    
    start_date = st.sidebar.date_input("Start Date", value=default_start_date, max_value=default_end_date)
    end_date = st.sidebar.date_input("End Date", value=default_end_date, min_value=start_date, max_value=default_end_date)
    
    selected_stocks = {}
    for ticker, name in default_stocks.items():
        if st.sidebar.checkbox(f"{name} ({ticker})", value=True):
            selected_stocks[ticker] = name
    
    custom_stock = st.sidebar.text_input("Add Custom Stocks (comma-separated)", placeholder="e.g., MSFT, TSLA")
    if custom_stock:
        custom_tickers = [tick.strip().upper() for tick in custom_stock.split(',')]
        for ticker in custom_tickers:
            if ticker and ticker not in selected_stocks:
                selected_stocks[ticker] = ticker
    
    # Portfolio weights
    st.sidebar.subheader("Portfolio Weights")
    weights = {}
    total_weight = 0
    for ticker in selected_stocks.keys():
        weight = st.sidebar.number_input(
            f"{ticker} Weight (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0 / len(selected_stocks),
            step=1.0,
            key=f"weight_{ticker}"
        )
        weights[ticker] = weight
        total_weight += weight
    
    if total_weight != 100:
        st.sidebar.warning(f"Total weight = {total_weight}%. Please adjust to 100%")
    
    # Market Index Selection
    st.sidebar.subheader("Benchmark Index")
    index_option = st.sidebar.selectbox(
        "Select Market Index",
        options=["^GSPC", "^DJI", "^IXIC"],
        format_func=lambda x: {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ"
        }[x]
    )
    
    if selected_stocks:
        all_tickers = list(selected_stocks.keys()) + [index_option]
        with st.spinner("Fetching stock data..."):
            df = fetch_data(all_tickers, start_date, end_date)
            
            tab1, tab2 = st.tabs(["Real-Time Visualization", "Stock Summary"])
            
            with tab1:
                # Display portfolio summary
                st.subheader("Portfolio Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Selected Stocks:")
                    for ticker, name in selected_stocks.items():
                        st.write(f"• {name} ({ticker}): {weights[ticker]}%")
                
                with col2:
                    st.write("Date Range:")
                    st.write(f"Start: {start_date}")
                    st.write(f"End: {end_date}")
                    st.write(f"Benchmark: {index_option}")
                
                create_stock_graphs(df)
            
            with tab2:
                create_stock_summary(df)

if __name__ == "__main__":
    main()
