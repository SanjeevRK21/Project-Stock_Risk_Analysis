from engine.returns import compute_log_returns
from engine.risk import (
    annualized_volatility,
    downside_volatility,
    max_drawdown
)
from visuals.risk_plots import (
    plot_returns,
    plot_rolling_volatility,
    plot_drawdown
)
from chat.event_explainer import explain_event_with_llm


def run_risk_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    rolling_window: int = 30
):
    """
    Run risk metrics in the SAME order as original main.py:
    1. Compute & print metrics
    2. LLM explanation
    3. Visuals
    """

    # -------------------------
    # 1️⃣ Compute returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute risk metrics
    # -------------------------
    vol = annualized_volatility(returns)
    down_vol = downside_volatility(returns)
    mdd = max_drawdown(prices)

    risk_outputs = {
        "annualized_volatility": f"{vol:.2%}",
        "downside_volatility": f"{down_vol:.2%}",
        "max_drawdown": f"{mdd:.2%}"
    }

    # -------------------------
    # 3️⃣ Print metrics (same order)
    # -------------------------
    print("\nRisk Metrics")
    print(f"Annualized Volatility: {vol:.2%}")
    print(f"Downside Volatility: {down_vol:.2%}")
    print(f"Max Drawdown: {mdd:.2%}")

    
    # -------------------------
    # 5️⃣ Visuals (same order)
    # -------------------------
    plot_returns(returns, ticker)
    plot_rolling_volatility(
        returns,
        ticker,
        window=rolling_window
    )
    plot_drawdown(prices, ticker)

    # -------------------------
    # 4️⃣ LLM explanation
    # -------------------------
    
    risk_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Risk Metrics",
        event_outputs=risk_outputs
    )
   

    print("\n📘 Risk Metrics Explanation")
    print(risk_explanation)
    

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "annualized_volatility": vol,
        "downside_volatility": down_vol,
        "max_drawdown": mdd,
        "explanation": risk_explanation
    }
