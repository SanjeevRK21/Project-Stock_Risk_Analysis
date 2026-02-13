# pipeline/run_investment_simulation.py

from engine.investment_simulator import simulate_investment
from visuals.investment_plots import (
    plot_portfolio_value,
    plot_portfolio_value_with_extremes,
    plot_daily_pnl,
    plot_drawdown_in_currency
)
from chat.event_explainer import explain_event_with_llm


def run_investment_simulation(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 100_000
):
    """
    Run investment simulation in the SAME order as original main.py:
    1. Simulate portfolio
    2. Print summary
    3. LLM explanation
    4. Visualizations
    """

    # -------------------------
    # 1️⃣ Simulate investment
    # -------------------------
    investment_stats = simulate_investment(
        prices,
        initial_capital
    )

    # -------------------------
    # 2️⃣ Print results (same wording)
    # -------------------------
    print("\nInvestment Simulation Results")

    print(
        f"Initial Investment: "
        f"{investment_stats['initial_investment']:.2f}"
    )

    print(
        f"Final Value: "
        f"{investment_stats['final_value']:.2f}"
    )

    print(
        f"Lowest Value: {investment_stats['min_value']:.2f} "
        f"on {investment_stats['min_value_date'].date()}"
    )

    print(
        f"Highest Value: {investment_stats['max_value']:.2f} "
        f"on {investment_stats['max_value_date'].date()}"
    )

    print(
        f"Largest Daily Gain: {investment_stats['max_daily_gain']:.2f} "
        f"on {investment_stats['max_daily_gain_date'].date()}"
    )

    print(
        f"Largest Daily Loss: {investment_stats['max_daily_loss']:.2f} "
        f"on {investment_stats['max_daily_loss_date'].date()}"
    )

    # -------------------------
    # 3️⃣ Prepare LLM outputs
    # -------------------------
    investment_outputs = {
        "initial_investment": f"{investment_stats['initial_investment']:.2f}",
        "final_value": f"{investment_stats['final_value']:.2f}",

        "lowest_value": f"{investment_stats['min_value']:.2f}",
        "lowest_value_date": (
            investment_stats["min_value_date"].date().isoformat()
        ),

        "highest_value": f"{investment_stats['max_value']:.2f}",
        "highest_value_date": (
            investment_stats["max_value_date"].date().isoformat()
        ),

        "largest_daily_gain": f"{investment_stats['max_daily_gain']:.2f}",
        "largest_daily_gain_date": (
            investment_stats["max_daily_gain_date"].date().isoformat()
        ),

        "largest_daily_loss": f"{investment_stats['max_daily_loss']:.2f}",
        "largest_daily_loss_date": (
            investment_stats["max_daily_loss_date"].date().isoformat()
        )
    }

    # -------------------------
    # 4️⃣ LLM explanation
    # -------------------------
    investment_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Investment Simulation",
        event_outputs=investment_outputs
    )

    print("\n💰 Investment Simulation Explanation")
    print(investment_explanation)

    # -------------------------
    # 5️⃣ Visuals
    # -------------------------
    plot_portfolio_value(
        investment_stats["portfolio_series"],
        ticker
    )

    plot_portfolio_value_with_extremes(
        investment_stats["portfolio_series"],
        investment_stats["min_value_date"],
        investment_stats["max_value_date"],
        ticker
    )

    plot_daily_pnl(
        investment_stats["portfolio_series"],
        investment_stats["max_daily_gain_date"],
        investment_stats["max_daily_loss_date"],
        ticker
    )

    plot_drawdown_in_currency(
        investment_stats["portfolio_series"],
        ticker
    )

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "initial_investment": investment_stats["initial_investment"],
        "final_value": investment_stats["final_value"],
        "min_value": investment_stats["min_value"],
        "max_value": investment_stats["max_value"],
        "max_daily_gain": investment_stats["max_daily_gain"],
        "max_daily_loss": investment_stats["max_daily_loss"],
        "explanation": investment_explanation
    }
