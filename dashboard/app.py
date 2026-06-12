from __future__ import annotations

import base64
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.factory import create_agent
from dashboard.components.comparison_charts import render_comparison_charts
from dashboard.components.grid_display import render_grid_figure
from dashboard.components.info_panel import render_info_panel
from dashboard.components.learning_curve import ALGO_NAMES, render_learning_curves
from envs import DroneDeliveryEnv
from experiments.io_utils import load_config


DRONE_ICON_PATH = PROJECT_ROOT / "drone.png"
DRONE_ICON = Image.open(DRONE_ICON_PATH) if DRONE_ICON_PATH.exists() else "🚁"

st.set_page_config(
    page_title="Drone RL Mission Control",
    page_icon=DRONE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-root: #080d14;
    --bg-panel: #0c121c;
    --bg-card: #101826;
    --text: #e4ecf5;
    --text-dim: #8899b4;
    --text-faint: #4e5d73;
    --border: rgba(100, 160, 220, 0.10);
    --border-hi: rgba(100, 180, 240, 0.30);
    --cyan: #22c7f0;
    --amber: #f0b429;
    --green: #2ee6a8;
    --red: #f2485c;
    --purple: #9b6dff;
    --blue: #4e9cf5;
    --mono: 'JetBrains Mono', monospace;
    --sans: 'Inter', 'Segoe UI', sans-serif;
}

* { box-sizing: border-box; }
html, body, .stApp { font-family: var(--sans); }

.stApp {
    background:
        radial-gradient(ellipse at 12% 0%,  rgba(34, 199, 240, 0.06) 0%, transparent 42%),
        radial-gradient(ellipse at 88% 100%, rgba(155, 109, 255, 0.05) 0%, transparent 42%),
        var(--bg-root);
    color: var(--text);
}

.block-container {
    padding: 0.6rem 1.6rem 2rem 1.6rem !important;
    max-width: 100% !important;
}

/* ── HERO ── */
.hero {
    display: flex; align-items: center; gap: 22px;
    background: linear-gradient(100deg, rgba(34,199,240,0.07), rgba(155,109,255,0.04));
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 24px;
    margin-bottom: 16px;
    position: relative;
}
.hero img { width: 64px; filter: drop-shadow(0 0 14px rgba(34,199,240,0.4)); }
.hero-title {
    font-family: var(--mono); font-size: 22px; font-weight: 800;
    letter-spacing: 1.5px; color: #f0f4fa;
}
.hero-title span { color: var(--cyan); }
.hero-sub { font-size: 12.5px; color: var(--text-dim); margin-top: 2px; }
.hero::after {
    content: '● SYS ONLINE';
    position: absolute; top: 12px; right: 18px;
    font-family: var(--mono); font-size: 10px; font-weight: 700;
    color: var(--green); letter-spacing: 1.5px;
    animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse { 0%,100% {opacity:.5;} 50% {opacity:1;} }

/* ── PANEL ── */
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.panel-title {
    font-family: var(--mono); font-size: 12px; font-weight: 700;
    color: var(--cyan); letter-spacing: 2px; margin-bottom: 12px;
}
.ctrl-label {
    font-family: var(--mono); font-size: 10.5px; font-weight: 600;
    color: var(--text-dim); letter-spacing: 1.4px;
    text-transform: uppercase; display: block;
    margin: 10px 0 4px 0;
}

/* ── QUICK STATS ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    text-align: center;
}
.stat-label {
    font-family: var(--mono); font-size: 9.5px; font-weight: 600;
    color: var(--text-faint); letter-spacing: 1.2px; text-transform: uppercase;
}
.stat-value {
    font-family: var(--mono); font-size: 22px; font-weight: 800;
    margin-top: 2px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    height: 44px; padding: 0 18px;
    background: transparent;
    border-radius: 8px 8px 0 0;
    color: var(--text-faint) !important;
    font-family: var(--mono) !important;
    font-weight: 600; font-size: 12.5px;
    letter-spacing: 1px;
    border: 1px solid transparent; border-bottom: none;
    margin-bottom: -1px;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-dim) !important; background: rgba(34,199,240,0.04); }
.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    background: rgba(34,199,240,0.07);
    border-color: var(--border);
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--mono) !important;
    font-size: 12px !important; font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    border-radius: 7px !important;
    height: 40px !important;
    width: 100%;
    transition: all 0.15s !important;
}
.stButton > button[kind="primary"] {
    background: var(--cyan) !important;
    color: #06121c !important;
    border: 1px solid var(--cyan) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #45d4f6 !important;
    box-shadow: 0 0 18px rgba(34,199,240,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--bg-card) !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border-hi) !important;
}
.stButton > button[kind="secondary"]:hover {
    color: var(--cyan) !important;
    border-color: var(--cyan) !important;
    background: rgba(34,199,240,0.06) !important;
}

/* ── INPUTS ── */
.stSelectbox [data-baseweb="select"], .stNumberInput input {
    font-family: var(--mono) !important;
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: 7px !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stRadio [role="radiogroup"] { gap: 6px; }
.stRadio [role="radio"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
    color: var(--text-dim) !important;
    padding: 4px 12px !important;
}
.stRadio [role="radio"][aria-checked="true"] {
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
    background: rgba(34,199,240,0.08) !important;
}
.stSlider [role="slider"] { background: rgba(34,199,240,0.2) !important; }

h3 {
    font-family: var(--mono) !important; font-size: 15px !important;
    color: var(--cyan) !important; letter-spacing: 1.5px; text-transform: uppercase;
}
h4 {
    font-family: var(--mono) !important; font-size: 12.5px !important;
    color: var(--text-dim) !important; letter-spacing: 1.2px; text-transform: uppercase;
}
.stCaption { font-family: var(--mono) !important; color: var(--text-faint) !important; font-size: 11px !important; }
hr { border-color: var(--border) !important; margin: 14px 0 !important; }

.stSuccess {
    background: rgba(46,230,168,0.07) !important;
    border: 1px solid rgba(46,230,168,0.25) !important;
    color: var(--green) !important; border-radius: 7px !important;
}
.stInfo {
    background: rgba(34,199,240,0.06) !important;
    border: 1px solid rgba(34,199,240,0.2) !important;
    color: var(--cyan) !important; border-radius: 7px !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-root); }
::-webkit-scrollbar-thumb { background: rgba(100,160,220,0.16); border-radius: 3px; }

[data-baseweb="popover"], [data-baseweb="menu"] { background: var(--bg-card) !important; }
[data-baseweb="option"] { font-family: var(--mono) !important; font-size: 12px !important; color: var(--text-dim) !important; }
[data-baseweb="option"]:hover { background: rgba(34,199,240,0.07) !important; color: var(--cyan) !important; }

[data-testid="column"] { background: transparent; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS & SETTINGS
# ═══════════════════════════════════════════════════════════════════════════
GOALS = {
    "G0 — (0, 6)": (0, 6),
    "G1 — (3, 6)": (3, 6),
    "G2 — (6, 0)": (6, 0),
}
MAP_TYPES = ["Cố định", "Medium (ngẫu nhiên)"]
SIM_ALGOS = ["sarsa", "q_learning", "double_q_learning", "heuristic", "random"]
COMPARE_ALGOS = ["random", "heuristic", "q_learning", "sarsa"]

ss = st.session_state
_DEFAULTS = {
    "cfg_train_eps": 2500,
    "cfg_eval_eps": 100,
    "cfg_window": 100,
    "cfg_target": 85,
    "cfg_wind": "observable",
    "map_seed": 7,
    "sim_autorun": False,
}
for k, v in _DEFAULTS.items():
    ss.setdefault(k, v)


@st.cache_data
def base_config():
    return load_config("experiments/configs.yaml")


def medium_no_fly(map_seed: int, goal: tuple) -> tuple:
    """Random 10-cell no-fly layout avoiding start / pickup / goal."""
    cfg = base_config()["environment"]
    start = tuple(cfg["start_pos"])
    pickup = tuple(cfg["pickup_pos"])
    rng = np.random.default_rng(map_seed)
    blocked = {start, pickup, goal}
    cells = [(r, c) for r in range(cfg["rows"]) for c in range(cfg["cols"]) if (r, c) not in blocked]
    chosen = rng.choice(len(cells), size=10, replace=False)
    return tuple(cells[i] for i in chosen)


def resolve_map(map_type: str, map_seed: int, goal: tuple) -> tuple:
    if map_type == MAP_TYPES[0]:
        return tuple(tuple(p) for p in base_config()["environment"]["no_fly_zones"])
    return medium_no_fly(map_seed, goal)


def build_env_config(goal: tuple, no_fly: tuple) -> dict:
    raw = base_config()
    env_cfg = dict(raw["environment"])
    env_cfg["dropoff_pos"] = list(goal)
    env_cfg["no_fly_zones"] = [list(p) for p in no_fly]
    return {"environment": env_cfg, "training": raw["training"]}


# ═══════════════════════════════════════════════════════════════════════════
# TRAINING & EVALUATION (cached, curve recorded)
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def train_with_curve(algo: str, wind_mode: str, goal: tuple, no_fly: tuple, episodes: int, seed: int = 0):
    cfg = build_env_config(goal, no_fly)
    env = DroneDeliveryEnv(wind_mode=wind_mode, config=cfg, seed=seed)
    agent = create_agent(algo, env, config=cfg, seed=seed)
    trains = getattr(agent, "requires_training", False)

    if not trains:
        episodes = min(episodes, 600 if algo == "random" else 1500)

    eps_start, eps_end = 1.0, 0.02
    decay = (eps_end / eps_start) ** (1.0 / max(1, int(episodes * 0.7)))

    returns, successes = [], []
    for ep in range(episodes):
        obs, _ = env.reset(seed=seed * 100_000 + ep)
        epsilon = max(eps_end, eps_start * (decay ** ep)) if trains else 0.0
        done = False
        info = {}
        while not done:
            state = env.state_encoder(obs) if trains else obs
            action = agent.select_action(state, epsilon=epsilon)
            next_obs, reward, term, trunc, info = env.step(action)
            if trains:
                agent.update(state, action, reward, env.state_encoder(next_obs), term)
            obs = next_obs
            done = term or trunc
        returns.append(env.cumulative_reward)
        successes.append(int(info.get("success", False)))

    curve = pd.DataFrame({"episode": range(episodes), "return": returns, "success": successes})
    return agent, curve


@st.cache_data(show_spinner=False)
def evaluate(algo: str, wind_mode: str, goal: tuple, no_fly: tuple, train_eps: int, eval_eps: int):
    agent, _ = train_with_curve(algo, wind_mode, goal, no_fly, train_eps)
    cfg = build_env_config(goal, no_fly)
    env = DroneDeliveryEnv(wind_mode=wind_mode, config=cfg, seed=12345)
    trains = getattr(agent, "requires_training", False)

    steps_list, succ, coll_eps = [], 0, 0
    for ep in range(eval_eps):
        obs, _ = env.reset(seed=900_000 + ep)
        done = False
        info = {}
        while not done:
            state = env.state_encoder(obs) if trains else obs
            action = agent.select_action(state, epsilon=0.0)
            obs, _, term, trunc, info = env.step(action)
            done = term or trunc
        steps_list.append(env.steps)
        succ += int(info.get("success", False))
        coll_eps += int(env.total_collisions > 0)

    return {
        "success_rate": succ / eval_eps,
        "avg_steps": float(np.mean(steps_list)),
        "std_steps": float(np.std(steps_list)),
        "collision_rate": coll_eps / eval_eps,
    }


def get_agent(algo, wind_mode, goal, no_fly, train_eps):
    with st.spinner(f"Đang train {ALGO_NAMES.get(algo, algo)}..."):
        agent, curve = train_with_curve(algo, wind_mode, goal, no_fly, train_eps)
    return agent, curve


# ═══════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════
_icon_b64 = base64.b64encode(DRONE_ICON_PATH.read_bytes()).decode() if DRONE_ICON_PATH.exists() else ""
st.markdown(f"""
<div class="hero">
    <img src="data:image/png;base64,{_icon_b64}" alt="drone">
    <div>
        <div class="hero-title"><span>◈</span> DRONE RL MISSION CONTROL</div>
        <div class="hero-sub">Drone giao hàng trong gió stochastic · Random / Heuristic / Q-Learning / SARSA · Mô phỏng từng bước & so sánh thuật toán</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════
tab_sim, tab_curves, tab_compare, tab_replay, tab_settings = st.tabs([
    "🎮 MÔ PHỎNG", "📈 LEARNING CURVES", "📊 SO SÁNH", "🔁 REPLAY", "⚙️ CÀI ĐẶT",
])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — MÔ PHỎNG (controls | grid | info)
# ═══════════════════════════════════════════════════════════════════════════
with tab_sim:
    col_ctrl, col_grid, col_info = st.columns([1.05, 1.95, 1.05], gap="medium")

    # ── LEFT: CONTROL PANEL ──
    with col_ctrl:
        st.markdown('<div class="panel"><div class="panel-title">◈ ĐIỀU KHIỂN</div></div>', unsafe_allow_html=True)

        st.markdown('<span class="ctrl-label">Thuật toán</span>', unsafe_allow_html=True)
        algo = st.selectbox(
            "Thuật toán", SIM_ALGOS,
            format_func=lambda a: ALGO_NAMES.get(a, a),
            index=0, label_visibility="collapsed", key="sel_algo",
        )

        st.markdown('<span class="ctrl-label">Chọn Goal</span>', unsafe_allow_html=True)
        goal_name = st.selectbox(
            "Goal", list(GOALS.keys()),
            index=0, label_visibility="collapsed", key="sel_goal",
        )
        goal_pos = GOALS[goal_name]

        st.markdown('<span class="ctrl-label">Bản đồ / Độ khó</span>', unsafe_allow_html=True)
        map_type = st.selectbox(
            "Bản đồ", MAP_TYPES,
            index=0, label_visibility="collapsed", key="sel_map",
        )
        if st.button("🗺 Tạo bản đồ & train lại", use_container_width=True, key="btn_remap"):
            ss.map_seed = int(np.random.default_rng().integers(1, 1_000_000))
            ss.pop("sim_key", None)
            st.rerun()

        st.markdown('<span class="ctrl-label">Tốc độ Auto (ms)</span>', unsafe_allow_html=True)
        speed_ms = st.slider("Tốc độ", 50, 1000, 200, 50, label_visibility="collapsed", key="sld_speed")

        st.markdown('<span class="ctrl-label">Mô phỏng</span>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            btn_run = st.button("▶ Chạy thuật toán", type="primary", use_container_width=True, key="btn_run")
        with b2:
            btn_step = st.button("⏭ Bước tiếp", type="secondary", use_container_width=True, key="btn_step")
        b3, b4 = st.columns(2)
        with b3:
            btn_stop = st.button("⏹ Dừng", type="secondary", use_container_width=True, key="btn_stop")
        with b4:
            btn_new = st.button("↺ Episode mới", type="secondary", use_container_width=True, key="btn_new")

    # resolve config & trained agent
    wind_mode = ss.cfg_wind
    no_fly = resolve_map(map_type, ss.map_seed, goal_pos)
    agent, _curve = get_agent(algo, wind_mode, goal_pos, no_fly, ss.cfg_train_eps)

    # ── SIM STATE MACHINE ──
    sim_key = f"{algo}|{wind_mode}|{goal_name}|{map_type}|{ss.map_seed}|{ss.cfg_train_eps}"
    if ss.get("sim_key") != sim_key:
        ss.sim_key = sim_key
        env_cfg = build_env_config(goal_pos, no_fly)
        ss.sim_env = DroneDeliveryEnv(wind_mode=wind_mode, config=env_cfg, seed=0)
        ss.sim_obs, ss.sim_info = ss.sim_env.reset(seed=0)
        ss.sim_done = False
        ss.sim_autorun = False
        ss.sim_ep_seed = 0
        ss.stats_episodes = 0
        ss.stats_successes = 0

    def new_episode():
        ss.sim_ep_seed += 1
        ss.sim_obs, ss.sim_info = ss.sim_env.reset(seed=ss.sim_ep_seed * 1009)
        ss.sim_done = False

    def step_once():
        if ss.sim_done:
            return
        env = ss.sim_env
        trains = getattr(agent, "requires_training", False)
        state = env.state_encoder(ss.sim_obs) if trains else ss.sim_obs
        action = agent.select_action(state, epsilon=0.0)
        ss.sim_obs, _, term, trunc, info = env.step(action)
        ss.sim_info = info
        if term or trunc:
            ss.sim_done = True
            ss.sim_autorun = False
            ss.stats_episodes += 1
            ss.stats_successes += int(info.get("success", False))

    if btn_new:
        ss.sim_autorun = False
        new_episode()
    if btn_stop:
        ss.sim_autorun = False
    if btn_step:
        ss.sim_autorun = False
        step_once()
    if btn_run:
        if ss.sim_done:
            new_episode()
        ss.sim_autorun = True
    if ss.sim_autorun and not ss.sim_done:
        step_once()

    # ── QUICK STATS (under controls) ──
    with col_ctrl:
        st.markdown('<span class="ctrl-label">Thống kê nhanh</span>', unsafe_allow_html=True)
        rate = (ss.stats_successes / ss.stats_episodes * 100) if ss.stats_episodes else 0.0
        s1, s2, s3 = st.columns(3)
        s1.markdown(f'<div class="stat-card"><div class="stat-label">Episode</div><div class="stat-value" style="color:var(--blue);">{ss.stats_episodes}</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-card"><div class="stat-label">Thành công</div><div class="stat-value" style="color:var(--green);">{ss.stats_successes}</div></div>', unsafe_allow_html=True)
        s3.markdown(f'<div class="stat-card"><div class="stat-label">Tỷ lệ</div><div class="stat-value" style="color:var(--amber);">{rate:.0f}%</div></div>', unsafe_allow_html=True)

    # ── CENTER: GRID ──
    with col_grid:
        env = ss.sim_env
        info = ss.sim_info
        if info.get("success"):
            grid_title = "✅ GIAO HÀNG THÀNH CÔNG"
        elif info.get("truncated"):
            grid_title = "❌ HẾT BƯỚC — THẤT BẠI"
        elif ss.sim_autorun:
            grid_title = f"🚁 ĐANG BAY  ·  BƯỚC {env.steps}"
        else:
            grid_title = f"⏸ {ALGO_NAMES.get(algo, algo).upper()}  ·  BƯỚC {env.steps}"
        st.plotly_chart(
            render_grid_figure(env, grid_title, goal_name=goal_name.split(" — ")[0]),
            width="stretch", config={"displayModeBar": False},
        )

    # ── RIGHT: INFO PANEL ──
    with col_info:
        render_info_panel(
            ss.sim_info,
            goal_name=goal_name,
            goal_pos=goal_pos,
            pickup_pos=tuple(base_config()["environment"]["pickup_pos"]),
        )

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — LEARNING CURVES
# ═══════════════════════════════════════════════════════════════════════════
with tab_curves:
    st.markdown("### 📈 Đường cong học tập")
    if ss.sim_autorun:
        st.caption("⏸ Tạm dừng cập nhật biểu đồ trong khi mô phỏng auto đang chạy...")
    else:
        st.caption(
            f"Goal {goal_name} · Bản đồ: {map_type} · Wind: {wind_mode} · "
            f"{ss.cfg_train_eps} episodes · cửa sổ trượt {ss.cfg_window}"
        )
        curves = {}
        for a in COMPARE_ALGOS:
            _, curve = get_agent(a, wind_mode, goal_pos, no_fly, ss.cfg_train_eps)
            curves[a] = curve
        render_learning_curves(curves, window=ss.cfg_window, target_pct=float(ss.cfg_target))

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — SO SÁNH
# ═══════════════════════════════════════════════════════════════════════════
with tab_compare:
    st.markdown("### 📊 So sánh 4 phương pháp")
    if ss.sim_autorun:
        st.caption("⏸ Tạm dừng cập nhật biểu đồ trong khi mô phỏng auto đang chạy...")
    else:
        st.caption(
            f"Đánh giá greedy (ε=0) · {ss.cfg_eval_eps} episodes/thuật toán · "
            f"Goal {goal_name} · Bản đồ: {map_type}"
        )
        with st.spinner("Đang đánh giá các thuật toán..."):
            metrics = {
                a: evaluate(a, wind_mode, goal_pos, no_fly, ss.cfg_train_eps, ss.cfg_eval_eps)
                for a in COMPARE_ALGOS
            }
        render_comparison_charts(metrics)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4 — REPLAY
# ═══════════════════════════════════════════════════════════════════════════
with tab_replay:
    st.markdown("### 🔁 Replay episode hoàn chỉnh")
    r1, r2, r3 = st.columns([1, 1.6, 1])
    with r1:
        st.markdown('<span class="ctrl-label">Seed</span>', unsafe_allow_html=True)
        replay_seed = st.selectbox("Seed replay", list(range(10)), index=0, label_visibility="collapsed", key="sel_replay_seed")
    with r2:
        st.markdown('<span class="ctrl-label">Delay mỗi bước (giây)</span>', unsafe_allow_html=True)
        replay_delay = st.slider("Delay", 0.05, 1.0, 0.25, 0.05, label_visibility="collapsed", key="sld_replay")
    with r3:
        st.markdown('<span class="ctrl-label">&nbsp;</span>', unsafe_allow_html=True)
        btn_replay = st.button("▶ Phát replay", type="primary", use_container_width=True, key="btn_replay")

    replay_box = st.empty()
    replay_info = st.empty()

    if btn_replay:
        env_cfg = build_env_config(goal_pos, no_fly)
        renv = DroneDeliveryEnv(wind_mode=wind_mode, config=env_cfg, seed=int(replay_seed))
        obs, info = renv.reset(seed=int(replay_seed))
        trains = getattr(agent, "requires_training", False)
        replay_box.plotly_chart(render_grid_figure(renv, "🚀 BẮT ĐẦU REPLAY", goal_name=goal_name.split(" — ")[0]), width="stretch")
        time.sleep(replay_delay)
        done = False
        while not done:
            state = renv.state_encoder(obs) if trains else obs
            action = agent.select_action(state, epsilon=0.0)
            obs, _, term, trunc, info = renv.step(action)
            done = term or trunc
            title = "✅ THÀNH CÔNG" if info.get("success") else ("❌ THẤT BẠI" if done else f"🚁 BƯỚC {renv.steps}")
            replay_box.plotly_chart(render_grid_figure(renv, title, goal_name=goal_name.split(" — ")[0]), width="stretch")
            time.sleep(replay_delay)
        with replay_info.container():
            render_info_panel(info, goal_name=goal_name, goal_pos=goal_pos,
                              pickup_pos=tuple(base_config()["environment"]["pickup_pos"]))
    else:
        env_cfg = build_env_config(goal_pos, no_fly)
        renv = DroneDeliveryEnv(wind_mode=wind_mode, config=env_cfg, seed=int(replay_seed))
        renv.reset(seed=int(replay_seed))
        replay_box.plotly_chart(render_grid_figure(renv, "⏸ SẴN SÀNG REPLAY", goal_name=goal_name.split(" — ")[0]), width="stretch")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5 — CÀI ĐẶT
# ═══════════════════════════════════════════════════════════════════════════
with tab_settings:
    st.markdown("### ⚙️ Cài đặt")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("#### Huấn luyện")
        st.number_input("Số episode huấn luyện", min_value=500, max_value=5000, step=500, key="cfg_train_eps")
        st.number_input("Số episode đánh giá (So sánh)", min_value=50, max_value=500, step=50, key="cfg_eval_eps")
        st.selectbox("Chế độ gió (wind mode)", ["observable", "hidden"], key="cfg_wind")
    with c2:
        st.markdown("#### Biểu đồ")
        st.slider("Cửa sổ trung bình trượt", 20, 300, step=10, key="cfg_window")
        st.slider("Target success rate (%)", 50, 100, step=5, key="cfg_target")
        st.markdown("#### Cache")
        if st.button("🗑 Xóa cache & train lại toàn bộ", type="secondary", key="btn_clear"):
            st.cache_resource.clear()
            st.cache_data.clear()
            ss.pop("sim_key", None)
            st.rerun()

    st.divider()
    st.markdown("#### Thông số môi trường")
    env_c = base_config()["environment"]
    st.markdown(f"""
    ```
    Lưới          : {env_c['rows']}×{env_c['cols']}     Start: {tuple(env_c['start_pos'])} · Pickup P: {tuple(env_c['pickup_pos'])}
    Goal hiện tại : {goal_name}
    Max bước      : {env_c['max_steps']}
    Reward        : step {env_c['step_penalty']} · wait {env_c['wait_penalty']} · va chạm {env_c['collision_penalty']}
                    no-fly {env_c['no_fly_penalty']} · pickup +{env_c['pickup_reward']} · dropoff +{env_c['dropoff_reward']}
    Gió           : Markov P(giữ)=0.7 · P(đổi)=0.1 · P(đẩy)={env_c['wind_push_probability']}
    ```
    """)

# ═══════════════════════════════════════════════════════════════════════════
# AUTORUN LOOP — one step per rerun so the Stop button stays responsive
# ═══════════════════════════════════════════════════════════════════════════
if ss.sim_autorun and not ss.sim_done:
    time.sleep(speed_ms / 1000.0)
    st.rerun()
