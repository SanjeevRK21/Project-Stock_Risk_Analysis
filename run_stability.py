# pipeline/run_stability.py

from engine.returns import compute_log_returns
from engine.stability import (
    rolling_sharpe,
    max_drawdown_duration,
    recovery_time,
    drawdown_duration
)
from visuals.stability_plots import (
    plot_rolling_sharpe,
    plot_drawdown_duration
)
from chat.event_explainer import explain_event_with_llm


def run_stability_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    rolling_window: int = 30
):
    """
    Run stability metrics in the SAME order as original main.py:
    1. Compute stability metrics
    2. Print metrics
    3. LLM explanation
    4. Visualizations
    """

    # -------------------------
    # 1️⃣ Compute returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute stability metrics
    # -------------------------
    rolling_sharpe_series = rolling_sharpe(
        returns,
        window=rolling_window
    )

    max_dd_duration = max_drawdown_duration(prices)
    recovery_days = recovery_time(prices)

    stability_outputs = {
        "max_underwater_duration_days": f"{max_dd_duration}",
        "recovery_time_days": f"{recovery_days}",
        "rolling_sharpe_window_days": f"{rolling_window}"
    }

    # -------------------------
    # 3️⃣ Print metrics (same wording)
    # -------------------------
    print("\nStability Metrics")

    print(
        f"Max Drawdown Duration (days): {max_dd_duration}\n"
        "The longest continuous period during which the stock stayed "
        "below its previous peak"
    )

    print(
        f"Recovery Time (days): {recovery_days}\n"
        "After the deepest drawdown (worst crash), how many days it took "
        "for the stock to climb back to its previous peak."
    )

    # -------------------------
    # 4️⃣ LLM explanation
    # -------------------------
    stability_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Stability Metrics",
        event_outputs=stability_outputs
    )

    print("\n📘 Stability Metrics Explanation")
    print(stability_explanation)

    # -------------------------
    # 5️⃣ Visuals
    # -------------------------
    plot_rolling_sharpe(
        rolling_sharpe_series,
        ticker,
        window=rolling_window
    )

    dd_duration_series = drawdown_duration(prices)
    plot_drawdown_duration(
        dd_duration_series,
        ticker
    )

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "max_drawdown_duration_days": max_dd_duration,
        "recovery_time_days": recovery_days,
        "rolling_sharpe_series": rolling_sharpe_series,
        "explanation": stability_explanation
    }
