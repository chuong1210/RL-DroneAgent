from __future__ import annotations

import streamlit as st


DIRECTION_OF_ACTION = {
    "up": "NORTH ↑",
    "right": "EAST →",
    "down": "SOUTH ↓",
    "left": "WEST ←",
    "wait": "STOP ●",
}

# range used to normalise the episode-reward progress bar
REWARD_BAR_MIN = -150.0
REWARD_BAR_MAX = 60.0


def _row(label, value, color="#e4ecf5"):
    return f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                padding:9px 2px; border-bottom:1px solid rgba(100,160,220,0.08);">
        <span style="font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:600;
                     color:#8899b4; letter-spacing:1.2px;">{label}</span>
        <span style="font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700;
                     color:{color};">{value}</span>
    </div>"""


def render_info_panel(info, goal_name="", goal_pos=None, pickup_pos=None):
    position = info.get("position", (0, 0))
    has_package = info.get("has_package", 0)

    target = goal_pos if has_package else (pickup_pos or goal_pos)
    if target is not None:
        distance = abs(position[0] - target[0]) + abs(position[1] - target[1])
        dist_text = f"{distance} ô"
    else:
        dist_text = "—"

    action_name = info.get("last_action_name")
    direction = DIRECTION_OF_ACTION.get(action_name, "STOP ●")
    action_text = (action_name or "stop").upper()

    if info.get("success"):
        status, status_color = "THÀNH CÔNG", "#2ee6a8"
    elif info.get("truncated"):
        status, status_color = "THẤT BẠI", "#f2485c"
    else:
        status, status_color = "ĐANG CHẠY", "#22c7f0"

    last_reward = info.get("last_reward", 0.0)
    total_reward = info.get("cumulative_reward", 0.0)
    reward_color = "#2ee6a8" if last_reward >= 0 else "#f2485c"

    pct = (total_reward - REWARD_BAR_MIN) / (REWARD_BAR_MAX - REWARD_BAR_MIN)
    pct = max(0.0, min(1.0, pct)) * 100
    package_text = "ĐÃ LẤY HÀNG" if has_package else "CHƯA CÓ HÀNG"
    package_color = "#2ee6a8" if has_package else "#f0b429"

    st.markdown(
        f"""
        <div style="background:#0c121c; border:1px solid rgba(100,160,220,0.10); border-radius:8px; padding:16px 18px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700;
                        color:#22c7f0; letter-spacing:2px; margin-bottom:8px;">◈ THÔNG TIN</div>
            {_row("VỊ TRÍ", f"({position[0]}, {position[1]})", "#4e9cf5")}
            {_row("HƯỚNG", direction, "#e4ecf5")}
            {_row("GOAL", goal_name or "—", "#2ee6a8")}
            {_row("KHOẢNG CÁCH", dist_text, "#f0b429")}
            {_row("HÀNH ĐỘNG", action_text, "#9b6dff")}
            {_row("REWARD", f"{last_reward:+.1f}", reward_color)}
            {_row("TỔNG REWARD", f"{total_reward:+.1f}", reward_color)}
            {_row("BƯỚC", info.get("steps", 0), "#e4ecf5")}
            {_row("GÓI HÀNG", package_text, package_color)}
            {_row("TRẠNG THÁI", status, status_color)}
            <div style="margin-top:14px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:600;
                            color:#8899b4; letter-spacing:1.2px; margin-bottom:6px;">REWARD EPISODE</div>
                <div style="background:#101826; border:1px solid rgba(100,160,220,0.10);
                            border-radius:99px; height:14px; overflow:hidden;">
                    <div style="width:{pct:.1f}%; height:100%; border-radius:99px;
                                background:linear-gradient(90deg, #f2485c, #f0b429 45%, #2ee6a8);
                                transition:width 0.25s ease;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-top:4px;
                            font-family:'JetBrains Mono',monospace; font-size:9px; color:#4e5d73;">
                    <span>{REWARD_BAR_MIN:.0f}</span><span>{REWARD_BAR_MAX:.0f}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
