from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


DISPLAY_COLUMNS = [
    "algo",
    "wind_mode",
    "success_rate_formatted",
    "avg_return_formatted",
    "avg_steps_formatted",
    "violation_rate_formatted",
    "collision_rate_formatted",
]

COLUMN_RENAME = {
    "algo": "AGENT",
    "wind_mode": "WIND",
    "success_rate_formatted": "SUCCESS %",
    "avg_return_formatted": "AVG RETURN",
    "avg_steps_formatted": "AVG STEPS",
    "violation_rate_formatted": "NO-FLY %",
    "collision_rate_formatted": "COLLISION %",
}


def render_comparison_table(results_dir="results"):
    path = Path(results_dir) / "summaries" / "aggregate_metrics.csv"
    if not path.exists():
        st.info("Chưa có aggregate_metrics.csv. Chạy sweep để sinh bảng mean ± std.")
        return
    df = pd.read_csv(path)

    # Format algorithm names
    if "algo" in df.columns:
        df["algo"] = df["algo"].str.replace("_", " ").str.upper()

    cols = [c for c in DISPLAY_COLUMNS if c in df.columns]
    table = df[cols].rename(columns={k: v for k, v in COLUMN_RENAME.items() if k in cols})

    # Custom CSS for the dataframe
    st.markdown("""
    <style>
    [data-testid="stDataFrame"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
        column_config={
            "AGENT": st.column_config.TextColumn("AGENT", width="medium"),
            "WIND": st.column_config.TextColumn("WIND", width="small"),
            "SUCCESS %": st.column_config.TextColumn("SUCCESS %", width="small"),
            "AVG RETURN": st.column_config.TextColumn("AVG RETURN", width="medium"),
            "AVG STEPS": st.column_config.TextColumn("AVG STEPS", width="small"),
            "NO-FLY %": st.column_config.TextColumn("NO-FLY %", width="small"),
            "COLLISION %": st.column_config.TextColumn("COLLISION %", width="small"),
        },
    )
