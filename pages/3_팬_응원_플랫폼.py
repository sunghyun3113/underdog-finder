import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import time
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.players import (
    PLAYERS, K1_AVG, CLUBS, DISCLAIMER,
    get_players_by_league, get_top_by_hearts,
    get_verdict_color, get_speed_color,
)

st.set_page_config(
    page_title="팬 응원 플랫폼 | 언더독 파인더",
    page_icon="💗",
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

# ── Session state 초기화 ──────────────────────────────────────────────────────
if "hearts" not in st.session_state:
    st.session_state.hearts = {p["id"]: p["weekly_hearts"] for p in PLAYERS}
if "liked" not in st.session_state:
    st.session_state.liked = {p["id"]: False for p in PLAYERS}
if "total_liked" not in st.session_state:
    st.session_state.total_liked = 0

# ── 타이머 계산 (이번 주 일요일 자정까지) ────────────────────────────────────
_now = datetime.now()
_days_to_monday = (7 - _now.weekday()) % 7 or 7
_next_monday = (_now + timedelta(days=_days_to_monday)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
_secs = max(0, int((_next_monday - _now).total_seconds()))
timer_str = f"{_secs // 3600:02d}:{(_secs % 3600) // 60:02d}:{_secs % 60:02d}"

# ── 상단 배너 ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#be185d 0%,#7c3aed 100%);
            border-radius:12px;padding:1.3rem 1.6rem;margin-bottom:1.4rem">
  <div style="display:flex;justify-content:space-between;align-items:center;
              flex-wrap:wrap;gap:1rem">
    <div>
      <div style="font-size:1.15rem;font-weight:700;color:#fff">
        🔥 이번 주 응원 집계 중
      </div>
      <div style="font-size:0.87rem;color:rgba(255,255,255,0.88);margin-top:0.25rem">
        TOP3 선수에게 구단 스카우터 리포트 자동 발송
      </div>
      <div style="font-size:0.78rem;color:rgba(255,255,255,0.68);margin-top:0.1rem">
        팬의 하트가 실제 구단 스카우터에게 전달됩니다
      </div>
    </div>
    <div style="text-align:center;background:rgba(0,0,0,0.28);
                border-radius:10px;padding:0.8rem 1.5rem;min-width:160px">
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.6);
                  letter-spacing:0.12em;text-transform:uppercase">집계 마감까지</div>
      <div style="font-size:2.2rem;font-weight:700;color:#fff;
                  font-family:'Courier New',monospace;letter-spacing:0.05em">
        {timer_str}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 탭 ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏆 응원 랭킹", "🗳️ 베스트 11", "💼 내 응원"])

# ── 헬퍼 ─────────────────────────────────────────────────────────────────────
def days_ago(date_str: str) -> str:
    d = (datetime.now().date()
         - datetime.strptime(date_str, "%Y-%m-%d").date()).days
    return "오늘" if d == 0 else f"{d}일 전"

def rank_badge(rank: int) -> str:
    return ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}위"

def heat_avg(p: dict) -> int:
    hs = p["heat_score"]
    return int((hs["ulsan"] + hs["jeonbuk"] + hs["pohang"]) / 3)

# ══════════════════════ TAB 1: 응원 랭킹 ══════════════════════════════════════
with tab1:
    league_filter = st.radio(
        "리그 필터", ["전체", "K3", "K4", "U리그"],
        horizontal=True, key="fan_league",
        label_visibility="collapsed",
    )

    pool = PLAYERS if league_filter == "전체" else [
        p for p in PLAYERS if p["league"] == league_filter
    ]
    sorted_pl = sorted(
        pool,
        key=lambda p: st.session_state.hearts[p["id"]],
        reverse=True,
    )
    max_h = max((st.session_state.hearts[p["id"]] for p in sorted_pl), default=1)

    for row_start in range(0, len(sorted_pl), 3):
        cols = st.columns(3)
        for col_idx, p in enumerate(sorted_pl[row_start:row_start + 3]):
            rank    = row_start + col_idx + 1
            hearts  = st.session_state.hearts[p["id"]]
            liked   = st.session_state.liked[p["id"]]
            # 팬 플랫폼: 분석 수치 비공개 (스카우터 전용)

            with cols[col_idx]:
                # ── 선수 카드 (TOP3 금/은/동 테두리, 분석 수치 비공개) ──
                rank_cls = (
                    "fan-card rank-1" if rank == 1 else
                    "fan-card rank-2" if rank == 2 else
                    "fan-card rank-3" if rank == 3 else
                    "fan-card"
                )
                # 스카우터 조회 요약
                scout_html = ""
                if p["scouts"]:
                    s = p["scouts"][0]
                    scout_html = (
                        f"<div style='color:#8892a4;font-size:0.72rem;"
                        f"margin-top:0.35rem'>"
                        f"👀 {s['club']} 스카우터 {s['count']}회 조회</div>"
                    )

                st.markdown(f"""
                <div class="{rank_cls}" style="padding:1rem 1rem 0.8rem">
                  <div style="display:flex;justify-content:space-between;
                              align-items:flex-start;margin-bottom:0.5rem">
                    <span style="font-size:1.15rem;font-weight:800;color:#e4e8f2">
                      {rank_badge(rank)}
                    </span>
                    <span style="background:rgba(100,116,139,0.12);color:#8892a4;
                                 font-size:0.62rem;border-radius:4px;
                                 padding:2px 7px;font-weight:600">
                      {p['league']}
                    </span>
                  </div>

                  <div style="font-size:1.8rem;line-height:1">{p['emoji']}</div>

                  <div style="font-size:1.05rem;font-weight:700;
                              color:#e4e8f2;margin-top:0.25rem">
                    {p['name']}
                    <span style="color:#8892a4;font-size:0.78rem">({p['age']}세)</span>
                  </div>
                  <div style="color:#8892a4;font-size:0.76rem;margin-bottom:0.5rem">
                    {p['club']} · {p['pos']}
                  </div>

                  <div style="font-size:1.1rem;font-weight:700;color:#ec4899">
                    💗 {hearts:,}
                  </div>

                  {scout_html}

                  <div style="margin-top:0.6rem;font-size:0.68rem;
                              color:#4a5568;border-top:1px solid #1e2433;
                              padding-top:0.45rem">
                    💡 상세 분석 데이터는 구단 스카우터 전용입니다
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── 하트 버튼 ──────────────────────────────────────────────
                if liked:
                    st.button(
                        "💗 응원완료",
                        key=f"heart_{p['id']}",
                        use_container_width=True,
                        disabled=True,
                    )
                else:
                    if st.button(
                        "💗 응원하기",
                        key=f"heart_{p['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.hearts[p["id"]] += 1
                        st.session_state.liked[p["id"]] = True
                        st.session_state.total_liked += 1
                        st.balloons()
                        st.rerun()

                # ── 진행바 ────────────────────────────────────────────────
                st.progress(min(1.0, hearts / max_h))

                # ── 스카우터 조회 배지 ────────────────────────────────────
                if p["scouts"]:
                    s = p["scouts"][0]
                    st.markdown(
                        f"<div style='color:#8892a4;font-size:0.71rem;"
                        f"margin-top:0.15rem;margin-bottom:0.4rem'>"
                        f"👀 {s['club']} {s['count']}회 조회 · {days_ago(s['last'])}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

# ══════════════════════ TAB 2: 베스트 11 ══════════════════════════════════════
with tab2:

    # ── 포지션별 1위 선수 찾기 ──────────────────────────────────────────────
    best_by_pos = {}
    for player in PLAYERS:
        pos    = player["pos"]
        hearts = st.session_state.hearts.get(player["id"], player["weekly_hearts"])
        if pos not in best_by_pos or hearts > best_by_pos[pos]["hearts"]:
            best_by_pos[pos] = {
                "name":   player["name"],
                "hearts": hearts,
                "emoji":  player["emoji"],
                "club":   player["club"],
                "league": player["league"],
            }

    st.markdown("### 🏆 팬이 선택한 베스트 11")
    st.caption("포지션별 응원 수 1위 선수 · 하트를 누를수록 실시간 변동")

    groups = {
        "⚽ 공격":     ["ST", "LW", "RW"],
        "🎯 미드필더": ["CAM", "CM", "CDM"],
        "🛡️ 수비":    ["LB", "CB", "RB"],
        "🧤 골키퍼":  ["GK"],
    }

    for group_name, positions in groups.items():
        st.markdown(f"**{group_name}**")
        cols = st.columns(len(positions))
        for col, pos in zip(cols, positions):
            with col:
                if pos in best_by_pos:
                    p = best_by_pos[pos]
                    st.markdown(f"""
                    <div style="
                        background:rgba(236,72,153,0.08);
                        border:1px solid rgba(236,72,153,0.3);
                        border-radius:10px;
                        padding:12px 8px;
                        text-align:center;
                    ">
                        <div style="font-size:28px;margin-bottom:6px">{p['emoji']}</div>
                        <div style="font-size:11px;color:#ec4899;
                                    font-weight:600;margin-bottom:2px">{pos}</div>
                        <div style="font-size:13px;font-weight:700;
                                    color:#f9fafb;margin-bottom:2px">{p['name']}</div>
                        <div style="font-size:10px;color:#94a3b8;
                                    margin-bottom:4px">{p['club']}</div>
                        <div style="font-size:12px;color:#f472b6;
                                    font-weight:600">💗 {p['hearts']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        background:rgba(100,116,139,0.08);
                        border:1px dashed rgba(100,116,139,0.3);
                        border-radius:10px;
                        padding:12px 8px;
                        text-align:center;
                    ">
                        <div style="font-size:28px;margin-bottom:6px">❓</div>
                        <div style="font-size:11px;color:#64748b;
                                    font-weight:600;margin-bottom:2px">{pos}</div>
                        <div style="font-size:13px;color:#64748b">TBD</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════ TAB 3: 내 응원 ════════════════════════════════════════
with tab3:
    liked_pls = [p for p in PLAYERS if st.session_state.liked[p["id"]]]
    sent_total = sum(
        st.session_state.hearts[p["id"]] - p["weekly_hearts"]
        for p in liked_pls
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("응원한 선수", f"{len(liked_pls)}명")
    with c2:
        st.metric("보낸 총 하트", f"{max(0, sent_total):,}개")

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    if liked_pls:
        all_sorted   = sorted(PLAYERS, key=lambda p: st.session_state.hearts[p["id"]], reverse=True)
        rank_map     = {p["id"]: i + 1 for i, p in enumerate(all_sorted)}

        st.markdown(
            "<p style='color:#e4e8f2;font-weight:600;font-size:0.95rem'>"
            "내가 응원한 선수</p>",
            unsafe_allow_html=True,
        )
        for p in liked_pls:
            rank    = rank_map[p["id"]]
            hearts  = st.session_state.hearts[p["id"]]
            v_color = get_verdict_color(p["verdict_type"])
            st.markdown(f"""
            <div style="background:#111520;border-radius:12px;
                        border:1px solid rgba(255,255,255,0.07);
                        padding:0.85rem 1.1rem;margin-bottom:0.45rem;
                        display:flex;justify-content:space-between;align-items:center">
              <div>
                <span style="font-size:1.4rem">{p['emoji']}</span>
                <span style="color:#e4e8f2;font-weight:700;margin-left:0.5rem;
                             font-size:0.98rem">{p['name']}</span>
                <span style="color:#8892a4;font-size:0.78rem;margin-left:0.4rem">
                  {p['club']} · {p['pos']}
                </span>
              </div>
              <div style="text-align:right">
                <div style="color:#ec4899;font-weight:700">💗 {hearts:,}</div>
                <div style="color:#8892a4;font-size:0.73rem">
                  {rank_badge(rank)} 전체 {rank}위
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#111520;border-radius:12px;
                    border:1px solid rgba(255,255,255,0.07);
                    padding:3.5rem 2rem;text-align:center;margin-top:1rem">
          <div style="font-size:2.5rem">💗</div>
          <div style="color:#e4e8f2;font-size:1.05rem;font-weight:600;margin-top:0.8rem">
            아직 응원한 선수가 없어요
          </div>
          <div style="color:#8892a4;font-size:0.85rem;margin-top:0.4rem">
            랭킹 탭에서 마음에 드는 선수를 응원해보세요!
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── 뉴스 티커 ─────────────────────────────────────────────────────────────────
TICKERS = [
    "🔥 한남대 김민재 이번 주 응원 급상승 중",
    "👀 한남대 조현준 울산HD 스카우터 조회 확인",
    "🏆 TOP3 → 매주 구단 스카우트 리포트 자동 발송",
    "💗 시흥 공민현 누적 응원 급증",
    "📊 이번 주 전체 응원 역대 최고 기록 갱신 중",
]
st.markdown("---")
st.info(f"📡 실시간 뉴스  |  {random.choice(TICKERS)}")

st.markdown(
    "<div class='disclaimer-footer'>"
    "⚠️ 본 플랫폼의 AI 분석 수치는 시뮬레이션 기반이며 "
    "실제 선수의 능력치와 무관합니다. 공모전 시연 목적으로 제작되었습니다."
    "</div>",
    unsafe_allow_html=True,
)
