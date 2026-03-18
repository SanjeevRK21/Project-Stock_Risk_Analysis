# Stock Risk Analysis Engine
A modular Python-based quantitative analysis engine designed to evaluate stock performance using risk metrics, risk-adjusted ratios, and visual analytics.

This project provides a structured pipeline to:
- Fetch historical market data
- Compute returns
- Analyze risk characteristic
- Evaluate risk-adjusted performance
- Generate insightful visualizations

## Features
### Data Pipeline
- Fetches historical stock price data using Yahoo Finance API
- Handles missing data and ensures clean time series
- Flexible date range selection  
👉 Implemented in:  [`data_loader.py`](./data_loader.py)

### Returns Engine
- Computes daily log returns for accurate financial modeling  
👉 Implemented in:  [`returns.py`](./returns.py)

### Risk Metrics
- Provides core risk analysis across the full dataset:
- Annualized Volatility – Measures total risk scaled to yearly terms
- Downside Volatility – Captures only negative return risk
- Maximum Drawdown – Measures worst peak-to-trough decline  
👉 Implemented in: [`risk.py`](./risk.py)

### Risk-Adjusted Metrics
Evaluates return efficiency relative to risk:
- Sharpe Ratio – Return per unit of total risk
- Sortino Ratio – Return per unit of downside risk
- Calmar Ratio – Return vs worst drawdown  
👉 Implemented in: [`risk_adjusted.py`](./risk_adjusted.py)

### Visualization Suite
- Risk Visuals
- Daily returns plot
- Rolling volatility
- Drawdown curve  
👉 Implemented in: [`risk_plots.py`](./risk_plots.py)

### Risk-Adjusted Visuals
- Rolling Sharpe ratio
- Summary tables
- Bar chart comparison  
👉 Implemented in: [`risk_adjusted_plots.py`](./risk_adjusted_plots.py)

## System Workflow
```
Price Data → Log Returns → Risk Metrics → Risk-Adjusted Metrics → Visualizations  
```

## Installation   
```
git clone https://github.com/your-username/your-repo-name.git  
cd your-repo-name  
  
pip install -r requirements.txt  
```
## Required Libraries  
- pandas  
- numpy
- matplotlib
- yfinance

## Usage  
Example workflow from the main script:  
Reference:  
```
ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"

prices = load_price_data(ticker, start_date, end_date)

returns = compute_log_returns(prices)

# Risk Metrics
vol = annualized_volatility(returns)
down_vol = downside_volatility(returns)
mdd = max_drawdown(prices)

# Risk-Adjusted Metrics
sharpe = sharpe_ratio(returns)
sortino = sortino_ratio(returns)
calmar = calmar_ratio(prices)
```

## Sample Outputs  
1. Risk Metrics  
Annualized Volatility (%)  
Downside Volatility (%)  
Maximum Drawdown (%)  

3. Risk-Adjusted Metrics
Sharpe Ratio (>1 is good)  
Sortino Ratio (>1 is good)  
Calmar Ratio (>1 preferred)  

### Project Structure
```
.
├── engine/
│   ├── data_loader.py
│   ├── returns.py
│   ├── risk.py
│   ├── risk_adjusted.py
│
├── visuals/
│   ├── risk_plots.py
│   ├── risk_adjusted_plots.py
│
├── main.py
└── README.md
```

### Key Design Principles  
- Modular Architecture → Separate engines for returns, risk, and performance
- Extensible → Easy to plug in new metrics (alpha, beta, etc.)
- Quantitative Rigor → Uses log returns and annualized scaling
- Visualization-Driven → Insights through plots, not just numbers

### Future Improvements
- Add alpha, beta, and factor models
- Portfolio-level analytics
- Backtesting engine
- Integration with live market feeds
- Web dashboard (React / Streamlit)

### License
MIT License

### Author
Sanjeev Raj
