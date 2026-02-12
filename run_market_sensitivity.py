# pipeline/run_market_sensitivity.py

from engine.data_loader import load_price_data
from engine.returns import compute_log_returns
from engine.market import market_metrics
from visuals.market_plots import plot_stock_vs_market
from chat.event_explainer import explain_event_with_llm


def run_market_sensitivity_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    market_ticker: str = "^GSPC"
):
    """
    Run market sensitivity metrics in the SAME order as original main.py:
    1. Load market data
    2. Compute metrics
    3. Print metrics
    4. LLM explanation
    5. Visual regression plot
    """

    # -------------------------
    # 1️⃣ Compute stock returns
    # -------------------------
    stock_returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Load market data & returns
    # -------------------------
    market_prices = load_price_data(
        ticker=market_ticker,
        start=start_date,
        end=end_date
    )

    market_returns = compute_log_returns(market_prices)

    # -------------------------
    # 3️⃣ Compute market sensitivity metrics
    # -------------------------
    market_stats = market_metrics(
        stock_returns,
        market_returns
    )

    market_outputs = {
        "beta": f"{market_stats['Beta']:.2f}",
        "alpha_annual": f"{market_stats['Alpha']:.2%}",
        "r_squared": f"{market_stats['R2']:.2f}"
    }

    # -------------------------
    # 4️⃣ Print metrics (same wording & order)
    # -------------------------
    print("\nMarket Sensitivity Metrics\n")

    print(
        f"Beta: {market_stats['Beta']:.2f}\n"
        "(Beta > 1 → more aggressive than market)\n"
    )

    print(
        f"Alpha (annual): {market_stats['Alpha']:.2%}\n"
        "(Positive alpha → outperformed market-adjusted expectations)\n"
    )

    print(
        f"R²: {market_stats['R2']:.2f}\n"
        "(R² = 0.62 → 62% of movement explained by market)\n"
    )

    # -------------------------
    # 5️⃣ LLM explanation
    # -------------------------
    market_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Market Sensitivity Metrics",
        event_outputs=market_outputs
    )

    print("\n📘 Market Sensitivity Explanation")
    print(market_explanation)

    # -------------------------
    # 6️⃣ Visuals
    # -------------------------
    plot_stock_vs_market(
        stock_returns=stock_returns,
        market_returns=market_returns,
        stock_ticker=ticker,
        market_ticker=market_ticker
    )

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "beta": market_stats["Beta"],
        "alpha_annual": market_stats["Alpha"],
        "r_squared": market_stats["R2"],
        "explanation": market_explanation
    }
