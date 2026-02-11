# pipeline/run_drawdown_events.py

import pandas as pd

from engine.drawdown_events import drawdown_events_df
from visuals.drawdown_events_plots import (
    show_top_drawdowns,
    show_top_recovery_times,
    show_recent_drawdowns,
    show_recent_recoveries,
    plot_top_drawdowns,
    plot_top_recovery_times,
    plot_recent_drawdown_durations,
    plot_recent_recovery_times
)
from chat.event_explainer import explain_event_with_llm


def _format_drawdown_event(event_row: pd.Series) -> dict:
    """Format a single drawdown/recovery event for LLM explanation."""
    return {
        "peak_date": event_row["peak_date"].date().isoformat(),
        "trough_date": event_row["trough_date"].date().isoformat(),
        "recovery_date": (
            event_row["recovery_date"].date().isoformat()
            if pd.notna(event_row["recovery_date"])
            else "Not yet recovered"
        ),
        "drawdown_percent": f"{event_row['drawdown_pct']:.2f}%",
        "drawdown_duration_days": int(event_row["drawdown_duration_days"]),
        "recovery_time_days": (
            int(event_row["recovery_time_days"])
            if pd.notna(event_row["recovery_time_days"])
            else "Ongoing"
        )
    }


def run_drawdown_events(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    n: int = 10
):
    """
    Run drawdown & recovery historical analysis:
    - Worst & recent events
    - Tabular summaries
    - LLM explanations
    - Visual comparisons
    """

    # -------------------------
    # 1️⃣ Extract drawdown events
    # -------------------------
    dd_events = drawdown_events_df(prices)

    if dd_events.empty:
        print("No drawdown events detected.")
        return None

    # -------------------------
    # 2️⃣ Tabular summaries
    # -------------------------
    show_top_drawdowns(dd_events, n=n)
    show_top_recovery_times(dd_events, n=n)
    show_recent_drawdowns(dd_events, n=n)
    show_recent_recoveries(dd_events, n=n)

    # -------------------------
    # 3️⃣ Select key events
    # -------------------------
    worst_drawdown_event = (
        dd_events.sort_values("drawdown_pct")
        .iloc[0]
    )

    most_recent_drawdown_event = (
        dd_events.sort_values("trough_date", ascending=False)
        .iloc[0]
    )

    worst_recovery_event = (
        dd_events
        .dropna(subset=["recovery_time_days"])
        .sort_values("recovery_time_days", ascending=False)
        .iloc[0]
    )

    most_recent_recovery_event = (
        dd_events
        .dropna(subset=["recovery_date"])
        .sort_values("recovery_date", ascending=False)
        .iloc[0]
    )

    # -------------------------
    # 4️⃣ Format events for LLM
    # -------------------------
    worst_drawdown_outputs = _format_drawdown_event(worst_drawdown_event)
    recent_drawdown_outputs = _format_drawdown_event(most_recent_drawdown_event)
    worst_recovery_outputs = _format_drawdown_event(worst_recovery_event)
    recent_recovery_outputs = _format_drawdown_event(most_recent_recovery_event)

    # -------------------------
    # 5️⃣ LLM explanations
    # -------------------------
    worst_drawdown_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Worst Drawdown Event",
        event_outputs=worst_drawdown_outputs
    )
    print("\n📕 Worst Drawdown Explanation")
    print(worst_drawdown_explanation)

    recent_drawdown_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Most Recent Drawdown Event",
        event_outputs=recent_drawdown_outputs
    )
    print("\n📘 Most Recent Drawdown Explanation")
    print(recent_drawdown_explanation)

    worst_recovery_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Worst Recovery Event",
        event_outputs=worst_recovery_outputs
    )
    print("\n📕 Worst Recovery Explanation")
    print(worst_recovery_explanation)

    recent_recovery_explanation = explain_event_with_llm(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        event_name="Most Recent Recovery Event",
        event_outputs=recent_recovery_outputs
    )
    print("\n📘 Most Recent Recovery Explanation")
    print(recent_recovery_explanation)

    # -------------------------
    # 6️⃣ Visual summaries
    # -------------------------
    plot_top_drawdowns(dd_events, n=n)
    plot_top_recovery_times(dd_events, n=n)
    plot_recent_drawdown_durations(dd_events, n=n)
    plot_recent_recovery_times(dd_events, n=n)

    # -------------------------
    # Return values (optional)
    # -------------------------
    return {
        "worst_drawdown": worst_drawdown_outputs,
        "most_recent_drawdown": recent_drawdown_outputs,
        "worst_recovery": worst_recovery_outputs,
        "most_recent_recovery": recent_recovery_outputs
    }
