from engine.data_loader import get_available_date_range, load_price_data


ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"

prices = load_price_data(ticker, start_date, end_date)

# Risk Metrics
from engine.returns import compute_log_returns
from engine.risk import (
    annualized_volatility,
    downside_volatility,
    max_drawdown
)

returns = compute_log_returns(prices)

vol = annualized_volatility(returns)
down_vol = downside_volatility(returns)
mdd = max_drawdown(prices)

risk_outputs = {
    "annualized_volatility": f"{vol:.2%}",
    "downside_volatility": f"{down_vol:.2%}",
    "max_drawdown": f"{mdd:.2%}"
}

print("\nRisk Metrics")
print(f"Annualized Volatility: {vol:.2%}") 
print(f"Downside Volatility: {down_vol:.2%}") 
print(f"Max Drawdown: {mdd:.2%}")

# Risk visuals
from visuals.risk_plots import (
    plot_returns,
    plot_rolling_volatility,
    plot_drawdown
)

plot_returns(returns, ticker)
plot_rolling_volatility(returns, ticker)
plot_drawdown(prices, ticker)

#Risk Adjusted Metrics
from engine.risk_adjusted import sharpe_ratio, sortino_ratio, calmar_ratio

sharpe = sharpe_ratio(returns)
sortino = sortino_ratio(returns)
calmar = calmar_ratio(prices)

risk_adjusted_outputs = {
    "sharpe_ratio": f"{sharpe:.2f}",
    "sortino_ratio": f"{sortino:.2f}",
    "calmar_ratio": f"{calmar:.2f}"
}

print("\nRisk-Adjusted Metrics")
print(f"Sharpe Ratio: (Reward per unit of total risk) (>1 is good)\n {sharpe:.2f}")
print(f"Sortino Ratio: (Reward per unit of downside risk) (>1 is good)\n {sortino:.2f}")
print(f"Calmar Ratio: (Reward per unit of worst-case pain) (>1 means annual growth exceeded worst drawdown)\n {calmar:.2f}")

#Risk Adjusted visuals
from visuals.risk_adjusted_plots import (
    plot_rolling_sharpe,
    show_risk_adjusted_summary
)

# Risk-adjusted visuals
plot_rolling_sharpe(returns, ticker)
show_risk_adjusted_summary(sharpe, sortino, calmar)

from visuals.risk_adjusted_plots import plot_risk_adjusted_summary
plot_risk_adjusted_summary(sharpe, sortino, calmar, ticker)
