import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Underdog Finder",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 공통 CSS 로드 ─────────────────────────────────────────────────────────────
def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )

load_css()

# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div class='uf-logo' style='font-size:1.6rem;margin-bottom:0.2rem'>⚽ UNDERDOG</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### 메뉴")
    st.page_link("app.py",                         label="🏠  홈")
    st.page_link("pages/1_스카우터_대시보드.py",    label="🔍  스카우터 대시보드")
    st.page_link("pages/2_팬_응원_플랫폼.py",       label="💗  팬 응원 플랫폼")
    st.markdown("---")
    st.markdown(
        "<small style='color:#5a6478'>K리그 하부 리그 AI 스카우팅<br>© 2026 Underdog Finder</small>",
        unsafe_allow_html=True,
    )

# ── 히어로 ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="uf-logo">UNDERDOG FINDER</div>'
    '<div class="uf-tagline">데이터 황무지인 하부 리그의 원석을 발굴하는 AI 스카우팅 플랫폼</div>',
    unsafe_allow_html=True,
)

# ── 핵심 지표 카드 3개 ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">핵심 분석 지표</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card blue">
        <div class="metric-icon">⚡</div>
        <div class="metric-title">② 수비 전환 속도</div>
        <div class="metric-value">2.9<span style="font-size:1rem;color:#8892a4">초</span></div>
        <div class="metric-sub">볼 탈취 → 전방 전개 최고 기록</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card purple">
        <div class="metric-icon">🗺️</div>
        <div class="metric-title">④ 히트맵 일치율</div>
        <div class="metric-value">92<span style="font-size:1rem;color:#8892a4">%</span></div>
        <div class="metric-sub">이상적 포지션 커버리지 매칭</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card orange">
        <div class="metric-icon">🔗</div>
        <div class="metric-title">⑤ 유사 선수 매칭</div>
        <div class="metric-value">91<span style="font-size:1rem;color:#8892a4">%</span></div>
        <div class="metric-sub">프로 선수 스타일 코사인 유사도</div>
    </div>
    """, unsafe_allow_html=True)

# ── 플랫폼 소개 ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">플랫폼 소개</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])
with c1:
    st.markdown("""
K3·K4·U리그 등 **데이터가 거의 없는 하부 리그**에서
AI 영상 분석 + 통계 기반으로 **숨겨진 유망주를 자동 발굴**합니다.

| 기능 | 설명 |
|------|------|
| 🎥 영상 분석 | yt-dlp + OpenCV로 경기 영상을 자동 처리 |
| ⚡ 전환 속도 | 수비→공격 전환 반응 시간을 프레임 단위로 측정 |
| 🗺️ 히트맵 | 포지션별 활동 영역을 이상적 패턴과 매칭 |
| 🔗 유사 선수 | K1 선수 스탯과 코사인 유사도 비교 |
| 💗 팬 플랫폼 | 팬이 직접 유망주를 응원하고 기록 |
    """)

with c2:
    st.markdown("#### 이번 주 응원 TOP3")
    from core.players import PLAYERS, get_top_by_hearts
    top3 = get_top_by_hearts(3)
    rank_colors = ["#fbbf24", "#cbd5e1", "#b45309"]
    for i, p in enumerate(top3):
        score = p["sim"][0]["score"]
        bar = int(score / 10)
        st.markdown(
            f"<span style='color:{rank_colors[i]};font-weight:700'>"
            f"{'🥇' if i==0 else '🥈' if i==1 else '🥉'}</span> "
            f"**{p['name']}** ({p['pos']}) · {p['club']}<br>"
            f"<span style='color:#a855f7'>{'█' * bar}{'░' * (10 - bar)}</span> "
            f"<span style='color:#e4e8f2'>{score}%</span> "
            f"<span style='color:#ec4899'>💗 {p['weekly_hearts']:,}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("")

# ── CTA ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">시작하기</div>', unsafe_allow_html=True)
b1, b2, _ = st.columns([1, 1, 3])
with b1:
    if st.button("🔍  스카우터 대시보드 →", use_container_width=True):
        st.switch_page("pages/1_스카우터_대시보드.py")
with b2:
    if st.button("💗  팬 응원 플랫폼 →", use_container_width=True):
        st.switch_page("pages/2_팬_응원_플랫폼.py")

# ── 면책 문구 ─────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='disclaimer-footer'>"
    "⚠️ 본 플랫폼의 AI 분석 수치는 시뮬레이션 기반이며 "
    "실제 선수의 능력치와 무관합니다. 공모전 시연 목적으로 제작되었습니다."
    "</div>",
    unsafe_allow_html=True,
)
