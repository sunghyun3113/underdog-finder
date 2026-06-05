import streamlit as st
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.players import (
    PLAYERS, DISCLAIMER,
    get_speed_color, get_verdict_color,
)

st.set_page_config(
    page_title="영상 분석 센터 | 언더독 파인더",
    page_icon="📹",
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

# ── 세션 상태 ─────────────────────────────────────────────────────────────────
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "analyzed_ids" not in st.session_state:
    st.session_state.analyzed_ids = []

# ── 실제 분석 완료 구단 ───────────────────────────────────────────────────────
REAL_CLUBS = {
    "시흥시민축구단": "K3",
    "연세대학교":     "U리그",
    "한남대학교":     "U리그",
}

# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#e4e8f2;letter-spacing:0.05em'>📹 UNDERDOG FINDER</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.page_link("app.py",                          label="🏠  홈")
    st.page_link("pages/1_영상_분석_센터.py",        label="📹  영상 분석 센터")
    st.page_link("pages/2_스카우터_대시보드.py",      label="🔍  스카우터 대시보드")
    st.page_link("pages/3_팬_응원_플랫폼.py",         label="💗  팬 응원 플랫폼")
    st.markdown("---")

    # 분석 가이드
    st.markdown(
        "<p style='color:#94a3b8;font-size:0.72rem;font-weight:700;"
        "letter-spacing:0.1em;text-transform:uppercase'>📋 분석 가이드</p>",
        unsafe_allow_html=True,
    )
    st.markdown("""
<div style='font-size:0.78rem;color:#8892a4;line-height:1.8'>
  • 권장 영상 길이: <b style='color:#e4e8f2'>5분 이상</b><br>
  • 권장 화질: <b style='color:#e4e8f2'>720p 이상</b><br>
  • 지원 리그: <b style='color:#e4e8f2'>K3·K4·U리그</b><br>
  • AI 모델: <b style='color:#e4e8f2'>YOLO v8</b> (선수 추적)
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # 실제 분석 완료 구단
    st.markdown(
        "<p style='color:#94a3b8;font-size:0.72rem;font-weight:700;"
        "letter-spacing:0.1em;text-transform:uppercase'>✅ 실제 분석 완료 구단</p>",
        unsafe_allow_html=True,
    )
    for club, league in REAL_CLUBS.items():
        st.markdown(
            f"<div style='font-size:0.78rem;color:#10b981;margin-bottom:0.2rem'>"
            f"✅ {club} <span style='color:#5a6478'>({league})</span></div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        "<div style='font-size:0.76rem;color:#5a6478;margin-top:0.4rem'>"
        "나머지 구단: AI 추정값</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 면책 문구
    st.markdown(
        f"<div style='padding:0.6rem;background:#0a0d14;border-radius:8px;"
        f"border:1px solid rgba(255,255,255,0.05)'>"
        f"<p style='color:#4a5568;font-size:0.68rem;line-height:1.55;margin:0'>"
        f"⚠️ {DISCLAIMER.strip()}</p></div>",
        unsafe_allow_html=True,
    )

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:2rem;font-weight:900;letter-spacing:0.06em;"
    "background:linear-gradient(135deg,#00d4ff,#a855f7);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
    "background-clip:text'>📹 AI 영상 분석 센터</div>"
    "<div style='color:#8892a4;font-size:0.95rem;margin-bottom:1.5rem'>"
    "경기 영상을 입력하면 AI가 선수별 수비 전환 속도, "
    "포지셔닝 히트맵, 유사 선수를 자동으로 분석합니다</div>",
    unsafe_allow_html=True,
)

# ── 입력 방식 선택 ────────────────────────────────────────────────────────────
st.markdown(
    "<div style='color:#5a6478;font-size:0.72rem;font-weight:700;"
    "letter-spacing:0.15em;text-transform:uppercase;border-bottom:"
    "1px solid #1e2433;padding-bottom:0.4rem;margin-bottom:1rem'>"
    "영상 입력</div>",
    unsafe_allow_html=True,
)

input_method = st.radio(
    "입력 방식",
    ["🔗 유튜브 링크", "📁 영상 파일 업로드"],
    horizontal=True,
    label_visibility="collapsed",
    key="input_method",
)

col_input, col_select = st.columns([3, 2])

with col_input:
    if input_method == "🔗 유튜브 링크":
        video_url = st.text_input(
            "유튜브 경기 영상 URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="video_url",
        )
        url_valid = video_url.strip().startswith("https://") if video_url else False
        if video_url and not url_valid:
            st.warning("유효한 https:// URL을 입력해주세요.")
    else:
        uploaded_file = st.file_uploader(
            "경기 영상 파일 업로드 (mp4, avi, mov)",
            type=["mp4", "avi", "mov"],
            key="video_file",
        )
        url_valid = uploaded_file is not None

with col_select:
    # 구단 선택
    all_clubs = sorted(set(p["club"] for p in PLAYERS))
    selected_club = st.selectbox("구단 선택", all_clubs, key="club_select")

    # 구단 선수 multiselect
    club_players = [p for p in PLAYERS if p["club"] == selected_club]
    player_opts  = {f"{p['name']} ({p['pos']})": p["id"] for p in club_players}
    selected_names = st.multiselect(
        "분석할 선수 선택",
        list(player_opts.keys()),
        default=list(player_opts.keys())[:3],
        key="player_select",
    )
    selected_ids = [player_opts[n] for n in selected_names]

# ── 분석 시작 버튼 ────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

can_run = (url_valid or input_method == "🔗 유튜브 링크" and False) and bool(selected_ids)
can_run = bool(selected_ids) and (
    (input_method == "🔗 유튜브 링크" and video_url.strip().startswith("https://"))
    if input_method == "🔗 유튜브 링크"
    else uploaded_file is not None
)

btn_col, _ = st.columns([1, 3])
with btn_col:
    run_btn = st.button(
        "🤖 AI 분석 시작",
        use_container_width=True,
        disabled=not can_run,
        key="run_analysis",
    )

if run_btn:
    st.session_state.analysis_done = False
    st.session_state.analyzed_ids  = selected_ids

    progress_bar = st.progress(0.0)
    status_box   = st.empty()

    steps = [
        (0.0,  "⏳ 영상 로드 중..."),
        (0.2,  "👁️ 선수 감지 중... (YOLO v8)"),
        (0.4,  "⚡ 수비 전환 속도 측정 중..."),
        (0.6,  "🗺️ 포지셔닝 히트맵 생성 중..."),
        (0.8,  "🔗 유사 선수 매칭 중..."),
        (1.0,  "✅ 분석 완료!"),
    ]

    for pct, msg in steps:
        progress_bar.progress(pct)
        status_box.markdown(
            f"<div style='background:#111520;border-radius:8px;"
            f"border:1px solid rgba(255,255,255,0.07);padding:0.7rem 1rem;"
            f"color:#e4e8f2;font-size:0.9rem'><b>{msg}</b></div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.8)

    progress_bar.progress(1.0)
    st.session_state.analysis_done = True
    st.rerun()

# ── 분석 결과 ─────────────────────────────────────────────────────────────────
if st.session_state.analysis_done and st.session_state.analyzed_ids:
    st.markdown(
        "<div style='color:#5a6478;font-size:0.72rem;font-weight:700;"
        "letter-spacing:0.15em;text-transform:uppercase;border-bottom:"
        "1px solid #1e2433;padding-bottom:0.4rem;margin:1.5rem 0 1rem'>"
        "분석 결과</div>",
        unsafe_allow_html=True,
    )
    st.success("✅ 분석이 완료되었습니다! 선수별 결과를 확인하세요.")

    result_players = [p for p in PLAYERS if p["id"] in st.session_state.analyzed_ids]

    for i in range(0, len(result_players), 3):
        cols = st.columns(3)
        for col_idx, p in enumerate(result_players[i:i + 3]):
            spd       = p["speed"]["overall"]
            s_color   = get_speed_color(spd)
            method    = p.get("analysis_method", "estimated")
            data_src  = p.get("data_source", "AI 추정값")
            h_avg     = int((p["heat_score"]["ulsan"] +
                             p["heat_score"]["jeonbuk"] +
                             p["heat_score"]["pohang"]) / 3)

            if method == "measured":
                badge = ("<span style='background:rgba(16,185,129,0.15);color:#10b981;"
                         "border:1px solid rgba(16,185,129,0.3);border-radius:6px;"
                         "padding:2px 8px;font-size:0.7rem;font-weight:600'>✅ 실측값</span>")
            else:
                badge = ("<span style='background:rgba(100,116,139,0.15);color:#94a3b8;"
                         "border:1px solid rgba(100,116,139,0.3);border-radius:6px;"
                         "padding:2px 8px;font-size:0.7rem;font-weight:600'>📊 추정값</span>")

            with cols[col_idx]:
                st.markdown(f"""
                <div style="background:#111520;border-radius:12px;
                            border:1px solid rgba(255,255,255,0.07);
                            padding:1.1rem;margin-bottom:0.4rem">
                  <div style="font-size:1.6rem;margin-bottom:0.3rem">{p['emoji']}</div>
                  <div style="font-size:1rem;font-weight:700;color:#e4e8f2">
                    {p['name']}
                    <span style="color:#8892a4;font-size:0.8rem"> · {p['pos']}</span>
                  </div>
                  <div style="color:#8892a4;font-size:0.76rem;margin-bottom:0.7rem">
                    {p['club']} · {p['league']}
                  </div>
                  <div style="display:flex;flex-direction:column;gap:0.35rem;
                              font-size:0.82rem">
                    <div>⚡ 수비 전환
                      <b style="color:{s_color};margin-left:0.3rem">{spd}초</b>
                      <span style="color:#5a6478;font-size:0.72rem">
                        (K1 avg 3.8초)
                      </span>
                    </div>
                    <div>🗺️ 히트맵 일치율
                      <b style="color:#a78bfa;margin-left:0.3rem">{h_avg}%</b>
                    </div>
                    <div>🔗 유사 선수
                      <b style="color:#e4e8f2;margin-left:0.3rem">
                        {p['sim'][0]['name']}
                      </b>
                      <span style="color:#a78bfa"> {p['sim'][0]['score']}%</span>
                    </div>
                  </div>
                  <div style="margin-top:0.7rem">{badge}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    if st.button("📊 스카우터 대시보드에서 상세 분석 보기 →",
                 use_container_width=False, key="go_dashboard"):
        st.switch_page("pages/2_스카우터_대시보드.py")

elif not st.session_state.analysis_done:
    # 초기 안내
    st.markdown("""
    <div style="background:#111520;border-radius:12px;
                border:1px solid rgba(255,255,255,0.07);
                padding:2.5rem 2rem;text-align:center;margin-top:1rem">
      <div style="font-size:2.5rem;margin-bottom:0.8rem">📹</div>
      <div style="color:#e4e8f2;font-size:1rem;font-weight:600">
        영상을 입력하고 분석을 시작하세요
      </div>
      <div style="color:#8892a4;font-size:0.85rem;margin-top:0.4rem">
        유튜브 링크 또는 영상 파일을 업로드한 후<br>
        구단과 선수를 선택하고 AI 분석을 실행하세요.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── 면책 문구 ─────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='disclaimer-footer'>"
    "⚠️ 본 플랫폼의 AI 분석 수치는 시뮬레이션 기반이며 "
    "실제 선수의 능력치와 무관합니다. 공모전 시연 목적으로 제작되었습니다."
    "</div>",
    unsafe_allow_html=True,
)
