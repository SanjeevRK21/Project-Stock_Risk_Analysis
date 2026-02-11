# pipeline/run_growth.py

from engine.growth import total_return, cagr
from visuals.growth_plots import (
    plot_price_series,
    plot_cumulative_returns
)
from chat.event_explainer import explain_event_with_llm


def run_growth_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str
):
    """
    Run growth metrics in the SAME order as original main.py:
    1. Compute growth metrics
    2. Print results
    3. LLM explanation
    4. Visualizations
    """

    # -------------------------
    # 1️⃣ Compute growth metrics
    # -------------------------
    total_return_value = total_return(prices)
    cagr_value = cagr(prices)

    growth_outputs = {
        "total_return": f"{total_return_value:.2%}",
        "cagr": f"{cagr_value:.2%}"
    }

    # -------------------------
    # 2️⃣ Print metrics
    # -------------------------
    print("\nGrowth Metrics")
    print(f"Total Return: {total_return_value:.2%}")
    print(f"CAGR: {cagr_value:.2%}")

    # -------------------------
    # 3️⃣ LLM explanation
    # -------------------------
    growth_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Growth Metrics",
        event_outputs=growth_outputs
    )

    print("\n📘 Growth Metrics Explanation")
    print(growth_explanation)

    # -------------------------
    # 4️⃣ Visuals
    # -------------------------
    plot_price_series(
        prices,
        ticker
    )

    plot_cumulative_returns(
        prices,
        ticker
    )

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "total_return": total_return_value,
        "cagr": cagr_value,
        "explanation": growth_explanation
    }
