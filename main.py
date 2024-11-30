
#<-----------------------------------------------Importing Statements--------------------------------------------------------->
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import date, timedelta
import time

#<----------------------------------------------Extracting the Data---------------------------------------------------------->
# Fetch Stock Data
def fetch_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
            data[ticker] = stock_data
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
    return data
#<------------------------------------------Calculating the Performance metrics for the Summary-------------------------------------------------------------->

# Calculate Portfolio Performance Metrics
def calculate_performance_metrics(returns, market_returns, risk_free_rate=0.02):
    metrics = {}
    market_var = np.var(market_returns)
    
    for ticker in returns.columns:
        ticker_returns = returns[ticker]
        volatility = ticker_returns.std() * np.sqrt(252)
        annual_return = ticker_returns.mean() * 252
        
        sharpe = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
        beta = np.cov(ticker_returns, market_returns)[0, 1] / market_var if market_var > 0 else 0
        
        cum_returns = (1 + ticker_returns).cumprod()
        drawdowns = (cum_returns - cum_returns.expanding().max()) / cum_returns.expanding().max()
        max_drawdown = drawdowns.min() if len(drawdowns) > 0 else 0
        
        metrics[ticker] = {
            'Annual Return': annual_return,
            'Annual Volatility': volatility,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': max_drawdown,
            'Beta': beta
        }
    
    return pd.DataFrame(metrics).T

#<-------------------------------------------Real time visualization of stocks graphs ------------------------------------------------------------->
# Real-Time Stock Visualization
def create_stock_graphs(df, auto_refresh=True):
    st.subheader("Stock Price Visualization")
    graph_type = st.radio("Select Graph Type", ["Combined Graph", "Individual Graphs"], horizontal=True)
    

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
    normalized_df = df.div(df.iloc[0]) * 100
    if graph_type == "Combined Graph":
        fig = go.Figure()
        for column in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=normalized_df[column], name=column, mode='lines'))
        fig.update_layout(title="Normalized Stock Prices (Base=100)", xaxis_title="Date", yaxis_title="Normalized Price", height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        cols = st.columns(2)
        for idx, column in enumerate(df.columns):
            with cols[idx % 2]:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df[column], name=column, mode='lines'))
                fig.update_layout(title=f"{column} Stock Price", xaxis_title="Date", yaxis_title="Price", height=400)
                st.plotly_chart(fig, use_container_width=True)

    if auto_refresh:
        time.sleep(15)  # Refresh every 15 seconds
        st.rerun()  # Only refresh graphs

#<---------------------------------------------------Main Function ----------------------------------------------------->

# Main
def main():
    st.set_page_config(page_title="Financial Risk Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.title("Financial Risk Analysis Dashboard")
    
    # Sidebar Configuration
    st.sidebar.title("Portfolio Configuration")
    default_stocks = {'AAPL': 'Apple', 'GOOGL': 'Google', 'AMZN': 'Amazon', 'META': 'Meta'}
    default_end_date = date.today()
    default_start_date = default_end_date - timedelta(days=365)
    
    start_date = st.sidebar.date_input("Start Date", value=default_start_date, max_value=default_end_date)
    end_date = st.sidebar.date_input("End Date", value=default_end_date, min_value=start_date, max_value=default_end_date)
    
    selected_stocks = {ticker: name for ticker, name in default_stocks.items() if st.sidebar.checkbox(f"{name} ({ticker})", value=True)}
    custom_stock = st.sidebar.text_input("Add Custom Stocks (comma-separated)", placeholder="e.g., MSFT, TSLA")
    if custom_stock:
        custom_tickers = [tick.strip().upper() for tick in custom_stock.split(',')]
        selected_stocks.update({ticker: ticker for ticker in custom_tickers if ticker not in selected_stocks})
    
    weights = {}
    total_weight = 0
    for ticker in selected_stocks.keys():
        weight = st.sidebar.number_input(f"{ticker} Weight (%)", min_value=0.0, max_value=100.0, value=100.0 / len(selected_stocks), step=1.0, key=f"weight_{ticker}")
        weights[ticker] = weight
        total_weight += weight
    
    if total_weight != 100:
        st.sidebar.warning(f"Total weight = {total_weight}%. Please adjust to 100%")
    
    index_option = st.sidebar.selectbox("Select Market Index", ["^GSPC", "^DJI", "^IXIC"], format_func=lambda x: {"^GSPC": "S&P 500", "^DJI": "Dow Jones", "^IXIC": "NASDAQ"}[x])
    
    if selected_stocks:
        all_tickers = list(selected_stocks.keys()) + [index_option]
        with st.spinner("Fetching stock data..."):
            df = fetch_data(all_tickers, start_date, end_date)
            returns = df.pct_change().dropna()
            market_returns = returns[index_option]

            # Portfolio Summary with Allocation Pie Chart and Performance Metrics
            tab1 = st.container()
            with tab1:
                st.subheader("Portfolio Summary")

                # Two columns layout
                col1, col2 = st.columns(2)

                with col1:
                    # Portfolio Weight Allocation Pie Chart
                    st.header("Current Portfolio Allocation")
                    current_allocation = pd.DataFrame({
                        'Asset': list(selected_stocks.keys()),
                        'Weight': list(weights.values())
                    })
                    fig_current = px.pie(current_allocation, values='Weight', names='Asset', title='Current Weights')
                    st.plotly_chart(fig_current)

                with col2:
                    # Portfolio Performance Metrics
                    st.header("Portfolio Performance Metrics")
                    if 'performance_metrics' not in st.session_state:
                        st.session_state.performance_metrics = calculate_performance_metrics(returns, market_returns)
                    st.dataframe(st.session_state.performance_metrics.style.format("{:.2%}"))

                # Real-Time Stock Graphs (below summary)
                create_stock_graphs(df, auto_refresh=True)  # Real-time dynamic graphs with auto-refresh

                
#<-------------------------------------------------Initialization  ------------------------------------------------------->
if __name__ == "__main__":
    main()
