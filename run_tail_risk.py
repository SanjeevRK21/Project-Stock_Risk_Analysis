# pipeline/run_tail_risk.py

from engine.returns import compute_log_returns
from engine.tail_risk import (
    skewness,
    kurtosis_excess,
    value_at_risk,
    conditional_value_at_risk
)
from visuals.tail_risk_plots import plot_return_distribution
from chat.event_explainer import explain_event_with_llm


def run_tail_risk_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    confidence_level: float = 0.95
):
    """
    Run tail risk metrics in the SAME order as original main.py:
    1. Compute & print metrics
    2. LLM explanation
    3. Visual distribution plot
    """

    # -------------------------
    # 1️⃣ Compute returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute tail risk metrics
    # -------------------------
    skew_val = skewness(returns)
    kurt_val = kurtosis_excess(returns)
    var_95 = value_at_risk(returns, confidence_level)
    cvar_95 = conditional_value_at_risk(returns, confidence_level)

    tail_risk_outputs = {
        "skewness": f"{skew_val:.2f}",
        "kurtosis": f"{kurt_val:.2f}",
        "value_at_risk_95": f"{var_95:.2%}",
        "conditional_var_95": f"{cvar_95:.2%}"
    }

    # -------------------------
    # 3️⃣ Print metrics (same wording & order)
    # -------------------------
    print(
        "\nTail Risk Metrics (What do losses look like when things go really wrong?)"
    )

    print(
        "Skewness:\n"
        "(>0 - rare big gains, <0 - rare big losses "
        "(most days look fine, but crashes are sudden and severe), "
        "~~0 normal most of the days)\n"
        f"{skew_val:.2f}"
    )

    print(
        "Excess Kurtosis:\n"
        "(How frequently extreme events happen)\n"
        "(>0 fat tails = crashes more frequently, "
        "<0 thin tails = very rare extremes)\n"
        f"{kurt_val:.2f}"
    )

    print(
        "VaR (95%):\n"
        "(Worst loss threshold for 95% of days — "
        "losses won’t exceed this most of the time)\n"
        f"{var_95:.2%}"
    )

    print(
        "CVaR (95%):\n"
        "(Average loss during the worst 5% of days)\n"
        f"{cvar_95:.2%}"
    )

    print(
        "\nIn the graph:\n"
        "• Blue histogram → daily return distribution\n"
        "• Orange curve → normal distribution fit\n"
        "• Red dashed line → VaR (95%) threshold\n"
        "• Dark red solid line → CVaR (95%) average worst loss"
    )

    # -------------------------
    # 4️⃣ LLM explanation
    # -------------------------
    tail_risk_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Tail Risk Metrics",
        event_outputs=tail_risk_outputs
    )

    print("\n📘 Tail Risk Metrics Explanation")
    print(tail_risk_explanation)

    # -------------------------
    # 5️⃣ Visuals
    # -------------------------
    plot_return_distribution(
        returns,
        ticker,
        var_95,
        cvar_95
    )

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "skewness": skew_val,
        "kurtosis": kurt_val,
        "var_95": var_95,
        "cvar_95": cvar_95,
        "explanation": tail_risk_explanation
    }
