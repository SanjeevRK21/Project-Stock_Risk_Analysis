# Project-Stock_Risk_Analysis
This is my first project stepping into Quant Field 

1️. Project Overview 
This project focuses on building a foundational quantitative finance analysis tool that evaluates the performance and risk characteristics of a single stock using historical market data.
The goal is to move beyond simply observing stock prices and instead analyze:
How returns are generated over time
How risky the stock is
Whether the returns justify the risk taken
Using daily historical price data sourced from Yahoo Finance, the project transforms raw prices into return series and computes core risk and performance metrics commonly used by quantitative analysts and portfolio managers.
The project emphasizes time-series analysis, risk-adjusted evaluation, and practical financial intuition, rather than trading or prediction.

2️. What the Project Does (End-to-End Flow)

Step 1: Data Collection & Cleaning
Fetch historical daily stock prices using the Yahoo Finance API
Use adjusted closing prices to account for dividends and splits
Handle missing values and ensure consistent time indexing

Step 2: Return Computation
Convert price data into daily and monthly log returns
Use log returns due to their mathematical properties and industry usage
Prepare the data for statistical and risk analysis

Step 3: Risk Measurement
The project calculates multiple dimensions of risk:
Volatility (daily and annualized)
Rolling volatility to observe how risk changes over time
Maximum drawdown to quantify worst-case losses

Step 4: Risk-Adjusted Performance Metrics
Sharpe Ratio to evaluate return per unit of total risk
Sortino Ratio to evaluate return relative to downside risk only

Step 5: Visualization & Interpretation
Plot price movement, returns, volatility, and drawdowns
Use visual analysis to interpret market behavior during calm and turbulent periods

3. Final Output:  
A structured analysis that clearly explains:
How the stock behaves over time,
How risky it is and
whether its returns are justified given the risk profile
