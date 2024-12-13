

# Financial Risk Analysis Dashboard 📊💼

## Overview 🚀

The **Financial Risk Analysis Dashboard** is an interactive web application built using **Streamlit**, designed to help investors and financial analysts assess and optimize their portfolios. With a focus on **financial risk**, the app provides tools for portfolio optimization, CAPM analysis, efficient frontier visualization, and financial ratio analysis. Whether you're a beginner investor or a seasoned analyst, this dashboard is your go-to tool for making informed investment decisions! 💸

### Key Features 🌟

1. **Portfolio Optimization** 🔄
   - Optimize your portfolio by calculating **maximum Sharpe ratio** and **minimum volatility** to find the best balance between **risk and return**.
   - Visualize **optimal allocations** and **performance metrics**.

2. **CAPM Analysis** 📈
   - Use the **Capital Asset Pricing Model (CAPM)** to evaluate the **expected return**, **beta** (risk level), and the **market performance** of each asset in your portfolio.
   - Compare individual stock performance against the **market index**.

3. **Efficient Frontier** 🌐
   - Visualize the **efficient frontier** to explore the best risk-return trade-offs for different portfolio allocations.
   - Find the optimal portfolio location based on your **desired risk** and **return**.

4. **Financial Ratios Analysis** 🧮
   - Evaluate key financial ratios like **Net Profit Margin** and **Return on Equity (ROE)** on a **quarterly** and **annual** basis.
   - Track and visualize trends for each selected stock.

5. **Real-Time Stock Visualizations** 📉
   - Get live updates and interactive graphs for **stock prices**, **portfolio performance**, and **historical trends**.

6. **Custom Portfolio Weights** ⚖️
   - Set custom portfolio weights, or use the **Equal Weight** option to diversify your investments evenly across selected assets.

## Technologies Used ⚙️

- **Python**: Main programming language for implementing the logic and analysis.
- **Streamlit**: Framework for creating the interactive web interface.
- **Plotly**: For creating interactive charts and visualizations (e.g., performance metrics, stock prices, portfolio allocations).
- **yFinance**: To fetch real-time stock data and historical prices.
- **Pandas & NumPy**: For data manipulation, calculations, and analysis.
- **scikit-learn**: For statistical and optimization functions (used in CAPM and portfolio optimization).
- **Plotly Express**: For easy and effective plotting of financial data.
  
## Getting Started 🚀

### 1. Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/your-username/financial-risk-analysis-dashboard.git
cd financial-risk-analysis-dashboard
```

### 2. Install Dependencies 📦

Ensure you have Python 3.8 or higher installed. Then, create a virtual environment and install the required dependencies:

```bash
# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt
```

### 3. Run the Dashboard 🚀

Run the app locally using:

```bash
streamlit run app.py
```

This will start a local web server, and you can access the dashboard in your browser at `http://localhost:8501`.

## Features in Detail 🌍

### Portfolio Optimization 🔄

In the **Portfolio Overview** tab, users can adjust their portfolio weights or use the **Equal Weights** button to evenly distribute investments. The app calculates the **optimal allocation** based on **maximum Sharpe ratio** and **minimum volatility**, comparing different portfolios' performance. 📊

### CAPM Analysis 📈

The **CAPM (Capital Asset Pricing Model)** tool helps you determine the expected return of each asset, its **beta** (risk factor), and compare it to the **market index**. The analysis helps you understand whether a stock is worth the risk in relation to its market performance. 🏆

### Efficient Frontier 🌐

Visualize the **Efficient Frontier** to understand how different portfolio allocations perform in terms of risk and return. You can see a graph plotting various risk-return profiles and pinpoint the best investment strategies based on your desired risk level. 📍

### Financial Ratios 📊

Analyze the financial health of the companies you're investing in! Get key financial ratios like **Net Profit Margin** and **Return on Equity** (ROE), with the option to explore data on both **quarterly** and **annual** bases. 📅

### Real-Time Data & Visualization 📉

Keep track of **stock prices**, **portfolio performance**, and **market movements** in real-time, with interactive charts that help visualize the data intuitively. 🔄

## How to Use the Dashboard 🛠️

1. **Select Stocks** 📈
   - Enter the stock tickers you wish to analyze (e.g., AAPL, MSFT, TSLA).
   
2. **Set Investment Amount** 💵
   - Input your total investment amount and adjust the portfolio weights (either manually or equally).

3. **Market Index Selection** 🌍
   - Choose the market index (e.g., S&P 500) for CAPM analysis and portfolio comparison.

4. **Explore Analysis** 📊
   - Use tabs to explore **portfolio optimization**, **CAPM analysis**, **efficient frontier**, and **financial ratio analysis**.

## Example Visualizations 🎨

Here are some sample visualizations you can expect from the website:

- **Portfolio Weights Comparison** 📉 &  **Portfolio Performance Metrics** 🏆
<img width="1705" alt="image" src="https://github.com/user-attachments/assets/8cd325d9-9401-40a9-b841-29c57405c5d6" />


- **Optimised Portfolio Weighhts** 
![image](https://github.com/user-attachments/assets/65326b10-472a-4946-b852-6765891ef77e)


- **Efficient Frontier Graph** 🌍
<img width="1705" alt="image" src="https://github.com/user-attachments/assets/5fb7d3cb-f5d7-4ba9-91e7-36a80044eeba" />



  
- **Real Time Visualization** 📊
  <img width="1705" alt="image" src="https://github.com/user-attachments/assets/f393b6e5-f4ad-4527-957e-b6fbca10d0fd" />

- **Financial Ratios (e.g., ROE, Net Profit Margin)** 📈

![image](https://github.com/user-attachments/assets/8b426f12-e5c4-4007-bc35-cf4435b8fff7)



## Contribution 🤝

Feel free to fork the repository and submit pull requests. Contributions are welcome!

If you find a bug or have suggestions for new features, please [open an issue]


### 🚀 **Start Exploring Your Investments Today!**

With the **Financial Risk Analysis Dashboard**, you’re just a few clicks away from smarter, data-driven investment decisions! Whether you're optimizing your portfolio, analyzing risk, or evaluating stock performance, this application is here to guide you through the process. 🌟



## 👨‍💻 Author  

**Satheesh Meadi**  
Master's Student in Data Science | NLP Enthusiast  
📧 Email: smeadi1@umbc.edu  
🌐 GitHub: [GitHub](https://github.com/SATHEESH-MEADI)  
📚 LinkedIn: [Satheesh Meadi](https://www.linkedin.com/in/satheesh-meadi/)














