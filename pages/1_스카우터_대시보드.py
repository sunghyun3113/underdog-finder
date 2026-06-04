import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.players import (
    PLAYERS, K1_AVG, CLUBS, DISCLAIMER,
    get_players_by_league, get_verdict_color,
    get_speed_color, search_players,
)

st.set_page_config(
    page_title="스카우터 대시보드 | 언더독 파인더",
    page_icon="🔍",
    layout="wide",
)

def load_css():
    from pathlib import Path
    css_file = Path(__file__).parent.parent / "assets" / "style.css"
    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )

load_css()

# ── 상수 ──────────────────────────────────────────────────────────────────────
IDEAL_POS = {
    "GK":  (8,  34.0),
    "CB":  (22, 34.0),
    "LB":  (25, 12.0),
    "RB":  (25, 56.0),
    "CDM": (38, 34.0),
    "CM":  (52, 34.0),
    "CAM": (67, 34.0),
    "LW":  (78, 12.0),
    "RW":  (78, 56.0),
    "ST":  (88, 34.0),
}
PITCH_W, PITCH_H = 105, 68
CLUB_KEYS = {v: k for k, v in CLUBS.items()}
RANK_COLORS = ["#f5a623", "#9ca3af", "#c0813b", "#6b7280"]


# ── 헬퍼 함수 ─────────────────────────────────────────────────────────────────
def heat_color(score: int) -> str:
    if score >= 80:
        return "#10b981"
    if score >= 65:
        return "#f5a623"
    return "#ef4444"


def speed_score_norm(overall: float) -> float:
    return max(0.0, min(100.0, 100 - (overall - 2.5) / (5.5 - 2.5) * 100))


def draw_pitch_heatmap(pos: str, heat: int, player_id: int) -> plt.Figure:
    ix, iy = IDEAL_POS.get(pos, (52, PITCH_H / 2))
    rng = np.random.default_rng(seed=player_id * 17 + heat)
    offset = (100 - heat) * 0.22
    px = float(np.clip(ix + rng.uniform(-offset, offset), 5, 100))
    py = float(np.clip(iy + rng.uniform(-offset, offset), 3, 65))

    xg = np.linspace(0, PITCH_W, 350)
    yg = np.linspace(0, PITCH_H, 230)
    X, Y = np.meshgrid(xg, yg)
    sigma = 11.0
    ideal_map  = np.exp(-((X - ix) ** 2 + (Y - iy) ** 2) / (2 * sigma ** 2))
    player_map = np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * sigma ** 2))
    overlap    = np.minimum(ideal_map, player_map)

    rgba = np.zeros((*ideal_map.shape, 4))
    rgba[..., 0] = player_map * 0.9
    rgba[..., 1] = overlap * 0.35
    rgba[..., 2] = ideal_map * 0.9
    rgba[..., 3] = np.maximum(ideal_map, player_map) * 0.78

    fig, ax = plt.subplots(figsize=(6.5, 4.2), facecolor="#07090f")
    ax.set_facecolor("#0f3d1a")
    ax.set_xlim(0, PITCH_W)
    ax.set_ylim(0, PITCH_H)

    lc, lw = "#1e7a30", 1.2
    ax.add_patch(patches.Rectangle((0, 0), PITCH_W, PITCH_H,
                                   fill=False, edgecolor=lc, linewidth=lw))
    ax.axvline(PITCH_W / 2, color=lc, linewidth=lw)
    ax.add_patch(patches.Circle((PITCH_W / 2, PITCH_H / 2), 9.15,
                                fill=False, edgecolor=lc, linewidth=lw))
    ax.plot(PITCH_W / 2, PITCH_H / 2, "o", color=lc, markersize=2.5)
    for x0 in [0, PITCH_W - 16.5]:
        ax.add_patch(patches.Rectangle(
            (x0, (PITCH_H - 40.32) / 2), 16.5, 40.32,
            fill=False, edgecolor=lc, linewidth=lw))
    for x0 in [0, PITCH_W - 5.5]:
        ax.add_patch(patches.Rectangle(
            (x0, (PITCH_H - 18.32) / 2), 5.5, 18.32,
            fill=False, edgecolor=lc, linewidth=lw))

    ax.imshow(rgba, extent=[0, PITCH_W, 0, PITCH_H],
              origin="lower", aspect="auto", interpolation="bilinear")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.3)
    return fig


# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#e4e8f2;letter-spacing:0.05em'>🔍 UNDERDOG FINDER</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # 리그 필터
    selected_leagues = st.multiselect(
        "리그 필터",
        ["K3", "K4", "U리그"],
        default=["K3", "K4", "U리그"],
        key="league_filter",
    )
    pool = [p for p in PLAYERS if p["league"] in selected_leagues] if selected_leagues else PLAYERS

    # 선수 선택
    options = {f"{p['name']} ({p['club']} · {p['pos']})": p["id"] for p in pool}
    if not options:
        st.warning("선택된 리그에 선수가 없습니다.")
        st.stop()

    sel_label = st.selectbox("선수 선택", list(options.keys()), key="player_sel")
    player = next(p for p in PLAYERS if p["id"] == options[sel_label])

    # 비교 구단 선택
    club_label = st.selectbox("비교 구단", list(CLUBS.values()), key="club_sel")
    club_key = CLUB_KEYS[club_label]
    club_short = club_label.split("(")[0].strip()

    # 선수 프로필 카드
    v_color = get_verdict_color(player["verdict_type"])
    v_text  = "✅ 영입 권장" if player["verdict_type"] == "safe" else "⚠️ 조건부"
    st.markdown(f"""
    <div style="background:#111520;border-radius:12px;
                border:1px solid rgba(255,255,255,0.07);
                padding:1rem;margin-top:0.8rem;text-align:center">
      <div style="font-size:2.8rem">{player['emoji']}</div>
      <div style="font-size:1.15rem;font-weight:700;color:#e4e8f2;margin-top:0.3rem">
        {player['name']}
        <span style="color:#8892a4;font-size:0.85rem"> ({player['age']}세)</span>
      </div>
      <div style="color:#8892a4;font-size:0.82rem;margin-top:0.15rem">
        {player['club']} · {player['league']} · {player['pos']}
      </div>
      <div style="color:#5a6478;font-size:0.78rem;margin-top:0.1rem">
        등번호 #{player['number']}
      </div>
      <div style="margin-top:0.65rem">
        <span style="background:{v_color}22;color:{v_color};
                     border:1px solid {v_color}66;border-radius:6px;
                     padding:3px 12px;font-size:0.78rem;font-weight:600">
          {v_text}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 면책 문구
    st.markdown(f"""
    <div style="margin-top:1.4rem;padding:0.75rem;background:#0a0d14;
                border-radius:8px;border:1px solid rgba(255,255,255,0.05)">
      <p style="color:#4a5568;font-size:0.7rem;line-height:1.55;margin:0">
        {DISCLAIMER.strip()}
      </p>
    </div>
    """, unsafe_allow_html=True)


# ── 메인 영역 ──────────────────────────────────────────────────────────────────
speed_val = player["speed"]["overall"]
heat_val  = player["heat_score"][club_key]
top_sim   = player["sim"][0]
s_color   = get_speed_color(speed_val)
h_color   = heat_color(heat_val)
s_delta   = speed_val - K1_AVG["overall"]

# ── 상단 3개 지표 카드 ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div style="background:#111520;border-radius:12px;
                border:1px solid rgba(255,255,255,0.07);
                padding:1.3rem 1.2rem;text-align:center">
      <div style="color:#8892a4;font-size:0.72rem;font-weight:600;
                  letter-spacing:0.12em;text-transform:uppercase">
        ② 수비 전환 속도
      </div>
      <div style="font-size:2.4rem;font-weight:700;color:{s_color};margin:0.4rem 0">
        {speed_val}초
      </div>
      <div style="color:#8892a4;font-size:0.82rem">
        K1 평균 3.8초 대비
        <b style="color:{s_color}">{s_delta:+.1f}초</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background:#111520;border-radius:12px;
                border:1px solid rgba(255,255,255,0.07);
                padding:1.3rem 1.2rem;text-align:center">
      <div style="color:#8892a4;font-size:0.72rem;font-weight:600;
                  letter-spacing:0.12em;text-transform:uppercase">
        ④ 히트맵 일치율
      </div>
      <div style="font-size:2.4rem;font-weight:700;color:{h_color};margin:0.4rem 0">
        {heat_val}%
      </div>
      <div style="color:#8892a4;font-size:0.82rem">
        {club_short} 기준 포지셔닝
      </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="background:#111520;border-radius:12px;
                border:1px solid rgba(255,255,255,0.07);
                padding:1.3rem 1.2rem;text-align:center">
      <div style="color:#8892a4;font-size:0.72rem;font-weight:600;
                  letter-spacing:0.12em;text-transform:uppercase">
        ⑤ 유사 선수 매칭
      </div>
      <div style="font-size:2.0rem;font-weight:700;color:#a78bfa;margin:0.4rem 0">
        {top_sim['score']}%
      </div>
      <div style="color:#e4e8f2;font-size:0.95rem;font-weight:600">
        {top_sim['name']}
      </div>
      <div style="color:#8892a4;font-size:0.8rem">{top_sim['club']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── 중단 3개 컬럼 ─────────────────────────────────────────────────────────────
col_spd, col_map, col_sim = st.columns(3)

# ── 컬럼1: 수비 전환 속도 ─────────────────────────────────────────────────────
with col_spd:
    st.markdown(
        "<p style='color:#e4e8f2;font-weight:600;font-size:0.95rem;margin-bottom:0.4rem'>"
        "② 수비 전환 속도 분석</p>",
        unsafe_allow_html=True,
    )

    cats  = ["압박반응", "측면커버", "라인복귀", "스프린트"]
    p_val = [float(player["speed"][k]) for k in ["press", "cover", "line", "sprint"]]
    k_val = [float(K1_AVG[k]) for k in ["press", "cover", "line", "sprint"]]

    all_vals = list(p_val) + list(k_val)
    max_val = max(all_vals) if all_vals else 6.0

    fig_spd = go.Figure()
    fig_spd.add_trace(go.Bar(
        x=cats, y=p_val,
        name=player["name"],
        marker_color="#3b82f6",
        opacity=0.85,
        text=[f"{v}초" for v in p_val],
        textposition="outside",
        textfont=dict(color="#8892a4", size=10),
    ))
    for i, (cat, kv) in enumerate(zip(cats, k_val)):
        fig_spd.add_shape(
            type="line",
            x0=i - 0.45, x1=i + 0.45,
            y0=kv, y1=kv,
            line=dict(color="#ef4444", width=2, dash="dot"),
        )
    try:
        fig_spd.update_layout(
            paper_bgcolor="#111520", plot_bgcolor="#111520",
            font_color="#e4e8f2", height=230,
            margin=dict(l=10, r=10, t=20, b=30),
            showlegend=False,
            xaxis=dict(gridcolor="#1e2433", tickfont=dict(size=11)),
            yaxis=dict(gridcolor="#1e2433",
                       title=dict(text="초 (낮을수록 빠름)", font=dict(size=10)),
                       tickfont=dict(size=10), range=[0, max_val * 1.2]),
        )
    except Exception as e:
        st.error(f"차트 오류: {e}")
    st.plotly_chart(fig_spd, use_container_width=True)
    st.caption("🔴 점선 = K1 평균  |  막대가 낮을수록 빠른 전환")

    # 세부 지표 metrics
    ma, mb = st.columns(2)
    for i, (k, lbl) in enumerate(zip(
        ["press", "cover", "line", "sprint"],
        ["압박반응", "측면커버", "라인복귀", "스프린트"]
    )):
        pv = player["speed"][k]
        dv = pv - K1_AVG[k]
        (ma if i % 2 == 0 else mb).metric(lbl, f"{pv}초", f"{dv:+.1f}초")


# ── 컬럼2: 포지셔닝 히트맵 ───────────────────────────────────────────────────
with col_map:
    st.markdown(
        "<p style='color:#e4e8f2;font-weight:600;font-size:0.95rem;margin-bottom:0.4rem'>"
        "④ 포지셔닝 히트맵</p>",
        unsafe_allow_html=True,
    )

    fig_pitch = draw_pitch_heatmap(player["pos"], heat_val, player["id"])
    st.pyplot(fig_pitch, use_container_width=True)
    plt.close(fig_pitch)

    st.markdown(
        "<div style='display:flex;gap:1.2rem;font-size:0.73rem;"
        "color:#8892a4;margin-top:0.3rem;flex-wrap:wrap'>"
        "<span>🔵 이상 포지셔닝</span>"
        "<span>🔴 실제 포지셔닝</span>"
        "<span>🟣 일치 구간</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.metric(
        "히트맵 일치율",
        f"{heat_val}%",
        "K1 적합 수준" if heat_val >= 75 else "단계적 성장 필요",
    )


# ── 컬럼3: 유사 선수 + 레이더 ────────────────────────────────────────────────
with col_sim:
    st.markdown(
        "<p style='color:#e4e8f2;font-weight:600;font-size:0.95rem;margin-bottom:0.4rem'>"
        "⑤ 유사 선수 매칭</p>",
        unsafe_allow_html=True,
    )

    for i, sim in enumerate(player["sim"]):
        st.markdown(f"""
        <div style="background:#111520;border-radius:10px;
                    border:1px solid rgba(255,255,255,0.07);
                    padding:0.65rem 0.9rem;margin-bottom:0.45rem">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <span style="color:{RANK_COLORS[i]};font-weight:700;font-size:0.88rem">
                #{i+1}
              </span>
              <span style="color:#e4e8f2;font-weight:600;margin-left:0.35rem;font-size:0.9rem">
                {sim['name']}
              </span>
              <span style="color:#8892a4;font-size:0.78rem;margin-left:0.25rem">
                · {sim['club']}
              </span>
            </div>
            <span style="color:#a78bfa;font-weight:700;font-size:1.05rem">
              {sim['score']}%
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(sim["score"] / 100)

    # 레이더 차트
    r_labels = ["수비전환", "히트맵", "유사도", "인기도"]
    p_radar = [
        round(speed_score_norm(speed_val), 1),
        heat_val,
        player["sim"][0]["score"],
        min(100.0, player["weekly_hearts"] / 50.0),
    ]
    k_radar = [
        round(speed_score_norm(K1_AVG["overall"]), 1),
        85.0,
        100.0,
        60.0,
    ]

    fig_radar = go.Figure()
    for vals, name, fill_c, line_c in [
        (p_radar, player["name"], "rgba(59,130,246,0.18)", "#3b82f6"),
        (k_radar, "K1 평균",    "rgba(239,68,68,0.13)",  "#ef4444"),
    ]:
        theta = r_labels + [r_labels[0]]
        r_vals = vals + [vals[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals, theta=theta,
            fill="toself", fillcolor=fill_c,
            line=dict(color=line_c, width=2),
            name=name,
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="#0d1117",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="#1e2433",
                tickfont=dict(color="#5a6478", size=9),
            ),
            angularaxis=dict(
                gridcolor="#1e2433",
                tickfont=dict(color="#8892a4", size=10),
            ),
        ),
        paper_bgcolor="#111520",
        font_color="#e4e8f2",
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8892a4", size=9),
                    orientation="h", y=-0.12),
        height=270,
        margin=dict(l=30, r=30, t=15, b=10),
    )
    st.plotly_chart(fig_radar, use_container_width=True)


st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

# ── 하단 AI 종합 판정 ─────────────────────────────────────────────────────────
verdict_type = player["verdict_type"]
v_color = get_verdict_color(verdict_type)
ai_text = player["ai_verdict"][club_key]

if verdict_type == "safe":
    bg   = "rgba(16,185,129,0.10)"
    bd   = "rgba(16,185,129,0.40)"
    icon = "✅"
    vtxt = "영입 권장"
    left_bar = "4px solid #10b981"
else:
    bg   = "rgba(245,166,35,0.10)"
    bd   = "rgba(245,166,35,0.40)"
    icon = "⚠️"
    vtxt = "조건부 검토"
    left_bar = "4px solid #f5a623"

st.markdown(f"""
<div style="background:{bg};border:1px solid {bd};
            border-left:{left_bar};border-radius:12px;
            padding:1.5rem 1.8rem;margin-top:0.5rem">
  <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.85rem">
    <span style="font-size:2rem">{icon}</span>
    <div>
      <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.12em;
                  text-transform:uppercase;color:{v_color};opacity:0.8">AI 종합 판정</div>
      <div style="font-size:1.4rem;font-weight:700;color:{v_color}">{vtxt}</div>
    </div>
  </div>
  <p style="color:#d1d9e6;font-size:0.93rem;line-height:1.8;margin:0 0 1rem">
    {ai_text}
  </p>
  <div style="display:flex;gap:0.55rem;flex-wrap:wrap">
    <span style="background:rgba(255,255,255,0.06);color:#8892a4;
                 border-radius:6px;padding:3px 11px;font-size:0.74rem">
      📊 K리그1 실측값 기반
    </span>
    <span style="background:rgba(255,255,255,0.06);color:#8892a4;
                 border-radius:6px;padding:3px 11px;font-size:0.74rem">
      🏆 승리경기 이상값
    </span>
    <span style="background:rgba(255,255,255,0.06);color:#8892a4;
                 border-radius:6px;padding:3px 11px;font-size:0.74rem">
      🔒 추정값 없음
    </span>
  </div>
</div>
<div class="disclaimer-footer">
  ⚠️ 본 플랫폼의 AI 분석 수치는 시뮬레이션 기반이며 실제 선수의 능력치와 무관합니다.
  공모전 시연 목적으로 제작되었습니다.
</div>
""", unsafe_allow_html=True)
