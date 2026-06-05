import json
import os

# ========================================
# ⚠️  DISCLAIMER / 면책 문구
# ========================================
# 본 플랫폼의 모든 AI 분석 수치
# (수비 전환 속도, 히트맵 일치율, 유사 선수 매칭 점수 등)는
# 시뮬레이션 기반의 가상 데이터입니다.
# - 실제 선수의 능력치 및 경기력과 무관합니다.
# - 특정 선수에 대한 평가·비교가 아닙니다.
# - 구단명은 2026년 실제 참가 구단 기준입니다.
# - 선수 이름은 실제 선수단 공개 정보를 참고했으나
#   분석 수치는 모두 시뮬레이션입니다.
# - 본 서비스는 공모전 시연 목적으로 제작되었습니다.
# ========================================

def load_analysis_data() -> dict:
    data = {}
    files = {
        "siheung": "data/siheung_analysis.json",
        "yonsei":  "data/yonsei_analysis.json",
        "hannam":  "data/hannam_analysis.json",
    }
    for key, path in files.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data[key] = json.load(f)
    return data

ANALYSIS_DATA = load_analysis_data()


def get_real_speed(player_id: int) -> tuple:
    for data in ANALYSIS_DATA.values():
        for p in data.get("players", []):
            if p["id"] == player_id:
                return p.get("speed"), p.get("transition_method", "estimated")
    return None, None


def get_real_heatmap(player_id: int) -> list:
    for data in ANALYSIS_DATA.values():
        for p in data.get("players", []):
            if p["id"] == player_id:
                return p.get("heatmap_points", [])
    return []


K1_AVG = {"overall": 3.8, "press": 2.1, "cover": 4.2, "line": 3.9, "sprint": 4.8}

CLUBS = {
    "ulsan":   "울산 HD (4-3-3)",
    "jeonbuk": "전북 현대 (4-2-3-1)",
    "pohang":  "포항 스틸러스 (3-4-3)",
}

DISCLAIMER = """
⚠️ 본 플랫폼의 AI 분석 수치는 시뮬레이션 기반이며
실제 선수의 능력치와 무관합니다.
선수 평가가 아닌 플랫폼 시연 목적입니다.
"""

PLAYERS = []

# ── K3 리그 (15명) ────────────────────────────────────────────────────────────
PLAYERS.extend([
    # ── 시흥시민축구단 ─────────────────────────────────────────────────────────
    {
        "id": 1, "name": "주현성", "number": 1,
        "birth_year": 2000, "age": 26,
        "club": "시흥시민축구단", "league": "K3",
        "pos": "GK", "emoji": "🧤", "color": "1d4ed8",
        "speed": {"overall": 3.2, "press": 2.0, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 80, "jeonbuk": 78, "pohang": 76},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 82},
            {"name": "양한빈",  "club": "전북 현대", "score": 78},
            {"name": "이창근",  "club": "대전",       "score": 74},
            {"name": "구성윤",  "club": "포항",       "score": 70},
        ],
        "weekly_hearts": 1850, "total_hearts": 11100,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 2, "last": "2026-05-20"},
            {"club": "전북현대", "count": 1, "last": "2026-04-15"},
        ],
        "verdict_type": "safe", "change": 12.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 울산 HD 포지셔닝 히트맵 일치율 80%. 조현우(울산 HD)과 플레이 패턴 82% 유사. K1 백업 골키퍼 즉시 영입 권장.",
            "jeonbuk": "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 전북 현대 포지셔닝 히트맵 일치율 78%. 조현우(울산 HD)과 플레이 패턴 82% 유사. 전북 수문장 후보 즉시 영입 권장.",
            "pohang":  "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 76%. 조현우(울산 HD)과 플레이 패턴 82% 유사. 포항 GK 라인 즉시 보강 권장.",
        },
    },
    {
        "id": 2, "name": "박현준", "number": 3,
        "birth_year": 2002, "age": 24,
        "club": "시흥시민축구단", "league": "K3",
        "pos": "CB", "emoji": "🛡️", "color": "1d4ed8",
        "speed": {"overall": 3.5, "press": 2.2, "cover": 4.4, "line": 4.1, "sprint": 5.1},
        "heat_score": {"ulsan": 72, "jeonbuk": 75, "pohang": 69},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 76},
            {"name": "임채민",  "club": "울산 HD",   "score": 72},
            {"name": "김영빈",  "club": "광주",       "score": 68},
            {"name": "불투이",  "club": "전북 현대", "score": 65},
        ],
        "weekly_hearts": 1300, "total_hearts": 6500,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 7.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 울산 HD 포지셔닝 히트맵 일치율 72%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. 추가 성장 후 재평가 권장.",
            "jeonbuk": "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 전북 현대 포지셔닝 히트맵 일치율 75%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. 추가 성장 후 영입 재검토 권장.",
            "pohang":  "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 포항 스틸러스 포지셔닝 히트맵 일치율 69%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. 장기 모니터링 후 재평가 권장.",
        },
    },
    {
        "id": 3, "name": "황신중", "number": 8,
        "birth_year": 2001, "age": 25,
        "club": "시흥시민축구단", "league": "K3",
        "pos": "CM", "emoji": "🎯", "color": "1d4ed8",
        "speed": {"overall": 3.1, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 84, "jeonbuk": 82, "pohang": 80},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 85},
            {"name": "이명재",  "club": "울산 HD",   "score": 82},
            {"name": "정우영",  "club": "전북 현대", "score": 78},
            {"name": "김동현",  "club": "서울",       "score": 74},
        ],
        "weekly_hearts": 2200, "total_hearts": 13200,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대",   "count": 3, "last": "2026-05-22"},
            {"club": "포항스틸러스", "count": 2, "last": "2026-05-10"},
        ],
        "verdict_type": "safe", "change": 15.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 울산 HD 포지셔닝 히트맵 일치율 84%. 박진섭(전북 현대)과 플레이 패턴 85% 유사. 중원 장악력 즉시 전력화 가능.",
            "jeonbuk": "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 전북 현대 포지셔닝 히트맵 일치율 82%. 박진섭(전북 현대)과 플레이 패턴 85% 유사. 전북 미드필드 즉시 보강 권장.",
            "pohang":  "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 80%. 박진섭(전북 현대)과 플레이 패턴 85% 유사. 포항 중원 즉시 선발 투입 권장.",
        },
    },
    {
        "id": 4, "name": "안은산", "number": 19,
        "birth_year": 2003, "age": 23,
        "club": "시흥시민축구단", "league": "K3",
        "pos": "CAM", "emoji": "⚡", "color": "1d4ed8",
        "speed": {"overall": 3.0, "press": 1.8, "cover": 3.9, "line": 3.6, "sprint": 4.4},
        "heat_score": {"ulsan": 88, "jeonbuk": 85, "pohang": 82},
        "sim": [
            {"name": "이동경",  "club": "울산 HD",   "score": 87},
            {"name": "강성진",  "club": "전북 현대", "score": 83},
            {"name": "오현규",  "club": "전북 현대", "score": 79},
            {"name": "엄원상",  "club": "울산 HD",   "score": 76},
        ],
        "weekly_hearts": 2400, "total_hearts": 16800,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 3, "last": "2026-05-28"},
            {"club": "전북현대", "count": 2, "last": "2026-05-15"},
        ],
        "verdict_type": "safe", "change": 18.3,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 울산 HD 포지셔닝 히트맵 일치율 88%. 이동경(울산 HD)과 플레이 패턴 87% 유사. 창의적 공격 전개 즉시 영입 권장.",
            "jeonbuk": "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 전북 현대 포지셔닝 히트맵 일치율 85%. 이동경(울산 HD)과 플레이 패턴 87% 유사. 전북 공격 핵심 즉시 영입 권장.",
            "pohang":  "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 포항 스틸러스 포지셔닝 히트맵 일치율 82%. 이동경(울산 HD)과 플레이 패턴 87% 유사. 포항 공격형 MF 즉시 활용 권장.",
        },
    },
    {
        "id": 5, "name": "공민현", "number": 9,
        "birth_year": 2000, "age": 26,
        "club": "시흥시민축구단", "league": "K3",
        "pos": "ST", "emoji": "⚽", "color": "1d4ed8",
        "speed": {"overall": 3.4, "press": 2.1, "cover": 4.2, "line": 3.9, "sprint": 4.8},
        "heat_score": {"ulsan": 73, "jeonbuk": 70, "pohang": 68},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 74},
            {"name": "오세훈",    "club": "서울",       "score": 70},
            {"name": "조규성",    "club": "전북 현대", "score": 67},
            {"name": "일류첸코",  "club": "포항",       "score": 64},
        ],
        "weekly_hearts": 1250, "total_hearts": 5000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 1, "last": "2026-04-28"},
        ],
        "verdict_type": "caution", "change": 6.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 울산 HD 포지셔닝 히트맵 일치율 73%. 주민규(전북 현대)과 플레이 패턴 74% 유사. 6개월 후 재스카우팅 권장.",
            "jeonbuk": "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 전북 현대 포지셔닝 히트맵 일치율 70%. 주민규(전북 현대)과 플레이 패턴 74% 유사. 추가 성장 후 재평가 권장.",
            "pohang":  "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 포항 스틸러스 포지셔닝 히트맵 일치율 68%. 주민규(전북 현대)과 플레이 패턴 74% 유사. 임대 후 성장세 확인 필요.",
        },
    },

    # ── 경주한국수력원자력 ─────────────────────────────────────────────────────
    {
        "id": 6, "name": "이성주", "number": 12,
        "birth_year": 2003, "age": 23,
        "club": "경주한국수력원자력", "league": "K3",
        "pos": "GK", "emoji": "🧤", "color": "d97706",
        "speed": {"overall": 3.9, "press": 2.2, "cover": 4.3, "line": 4.0, "sprint": 4.9},
        "heat_score": {"ulsan": 68, "jeonbuk": 65, "pohang": 70},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 68},
            {"name": "양한빈",  "club": "전북 현대", "score": 64},
            {"name": "이창근",  "club": "대전",       "score": 62},
            {"name": "구성윤",  "club": "포항",       "score": 65},
        ],
        "weekly_hearts": 850, "total_hearts": 4250,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 5.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 울산 HD 포지셔닝 히트맵 일치율 68%. 조현우(울산 HD)과 플레이 패턴 68% 유사. 추가 성장 후 영입 재검토 권장.",
            "jeonbuk": "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 전북 현대 포지셔닝 히트맵 일치율 65%. 조현우(울산 HD)과 플레이 패턴 68% 유사. 추가 훈련 후 재평가 권장.",
            "pohang":  "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 포항 스틸러스 포지셔닝 히트맵 일치율 70%. 조현우(울산 HD)과 플레이 패턴 68% 유사. 장기 모니터링 대상으로 분류.",
        },
    },
    {
        "id": 7, "name": "류승범", "number": 14,
        "birth_year": 1999, "age": 27,
        "club": "경주한국수력원자력", "league": "K3",
        "pos": "CB", "emoji": "🛡️", "color": "d97706",
        "speed": {"overall": 3.8, "press": 2.3, "cover": 4.6, "line": 4.2, "sprint": 5.3},
        "heat_score": {"ulsan": 64, "jeonbuk": 68, "pohang": 62},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 66},
            {"name": "임채민",  "club": "울산 HD",   "score": 63},
            {"name": "김영빈",  "club": "광주",       "score": 62},
            {"name": "불투이",  "club": "전북 현대", "score": 64},
        ],
        "weekly_hearts": 700, "total_hearts": 2800,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 3.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 울산 HD 포지셔닝 히트맵 일치율 64%. 홍정호(전북 현대)과 플레이 패턴 66% 유사. 장기 모니터링 대상으로 분류.",
            "jeonbuk": "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 전북 현대 포지셔닝 히트맵 일치율 68%. 홍정호(전북 현대)과 플레이 패턴 66% 유사. 추가 성장 후 재평가 권장.",
            "pohang":  "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 포항 스틸러스 포지셔닝 히트맵 일치율 62%. 홍정호(전북 현대)과 플레이 패턴 66% 유사. 임대 후 성장세 확인 필요.",
        },
    },
    {
        "id": 8, "name": "국관우", "number": 77,
        "birth_year": 2002, "age": 24,
        "club": "경주한국수력원자력", "league": "K3",
        "pos": "CM", "emoji": "🎯", "color": "d97706",
        "speed": {"overall": 3.5, "press": 2.0, "cover": 4.2, "line": 3.9, "sprint": 4.8},
        "heat_score": {"ulsan": 76, "jeonbuk": 74, "pohang": 78},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 76},
            {"name": "이명재",  "club": "울산 HD",   "score": 72},
            {"name": "정우영",  "club": "전북 현대", "score": 74},
            {"name": "김동현",  "club": "서울",       "score": 70},
        ],
        "weekly_hearts": 1400, "total_hearts": 7000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 2, "last": "2026-05-19"},
        ],
        "verdict_type": "safe", "change": 11.3,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 울산 HD 포지셔닝 히트맵 일치율 76%. 박진섭(전북 현대)과 플레이 패턴 76% 유사. 중원 보강 즉시 선발 경쟁 투입 권장.",
            "jeonbuk": "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 전북 현대 포지셔닝 히트맵 일치율 74%. 박진섭(전북 현대)과 플레이 패턴 76% 유사. 전북 중원 즉시 활용 가능.",
            "pohang":  "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 포항 스틸러스 포지셔닝 히트맵 일치율 78%. 박진섭(전북 현대)과 플레이 패턴 76% 유사. 포항 미드필드 즉시 전력화 가능.",
        },
    },
    {
        "id": 9, "name": "정성호", "number": 19,
        "birth_year": 2001, "age": 25,
        "club": "경주한국수력원자력", "league": "K3",
        "pos": "RW", "emoji": "🔥", "color": "d97706",
        "speed": {"overall": 3.3, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 80, "jeonbuk": 77, "pohang": 82},
        "sim": [
            {"name": "엄원상",  "club": "울산 HD", "score": 82},
            {"name": "양현준",  "club": "강원",     "score": 78},
            {"name": "이동준",  "club": "전남",     "score": 74},
            {"name": "이강인",  "club": "PSG",      "score": 71},
        ],
        "weekly_hearts": 1500, "total_hearts": 9000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",     "count": 2, "last": "2026-05-24"},
            {"club": "포항스틸러스", "count": 1, "last": "2026-05-08"},
        ],
        "verdict_type": "safe", "change": 14.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 울산 HD 포지셔닝 히트맵 일치율 80%. 엄원상(울산 HD)과 플레이 패턴 82% 유사. 측면 공격 즉시 전력화 가능.",
            "jeonbuk": "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 전북 현대 포지셔닝 히트맵 일치율 77%. 엄원상(울산 HD)과 플레이 패턴 82% 유사. 전북 우측 날개 즉시 영입 권장.",
            "pohang":  "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 포항 스틸러스 포지셔닝 히트맵 일치율 82%. 엄원상(울산 HD)과 플레이 패턴 82% 유사. 포항 윙 즉시 선발 투입 권장.",
        },
    },
    {
        "id": 10, "name": "전정호", "number": 22,
        "birth_year": 1999, "age": 27,
        "club": "경주한국수력원자력", "league": "K3",
        "pos": "ST", "emoji": "⚽", "color": "d97706",
        "speed": {"overall": 4.0, "press": 2.3, "cover": 4.5, "line": 4.2, "sprint": 5.2},
        "heat_score": {"ulsan": 62, "jeonbuk": 66, "pohang": 63},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 64},
            {"name": "오세훈",    "club": "서울",       "score": 62},
            {"name": "조규성",    "club": "전북 현대", "score": 63},
            {"name": "일류첸코",  "club": "포항",       "score": 61},
        ],
        "weekly_hearts": 620, "total_hearts": 2480,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 2.9,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 울산 HD 포지셔닝 히트맵 일치율 62%. 주민규(전북 현대)과 플레이 패턴 64% 유사. 임대 후 성장세 확인 필요.",
            "jeonbuk": "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 전북 현대 포지셔닝 히트맵 일치율 66%. 주민규(전북 현대)과 플레이 패턴 64% 유사. 6개월 후 재스카우팅 권장.",
            "pohang":  "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 포항 스틸러스 포지셔닝 히트맵 일치율 63%. 주민규(전북 현대)과 플레이 패턴 64% 유사. 추가 성장 후 재평가 권장.",
        },
    },

    # ── 창원FC ─────────────────────────────────────────────────────────────────
    {
        "id": 11, "name": "이세민", "number": 21,
        "birth_year": 2006, "age": 20,
        "club": "창원FC", "league": "K3",
        "pos": "GK", "emoji": "🧤", "color": "b91c1c",
        "speed": {"overall": 3.8, "press": 2.2, "cover": 4.3, "line": 4.0, "sprint": 4.9},
        "heat_score": {"ulsan": 67, "jeonbuk": 64, "pohang": 69},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 66},
            {"name": "양한빈",  "club": "전북 현대", "score": 63},
            {"name": "이창근",  "club": "대전",       "score": 65},
            {"name": "구성윤",  "club": "포항",       "score": 68},
        ],
        "weekly_hearts": 750, "total_hearts": 3000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 5.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 울산 HD 포지셔닝 히트맵 일치율 67%. 조현우(울산 HD)과 플레이 패턴 66% 유사. 추가 훈련 후 영입 재검토 권장.",
            "jeonbuk": "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 전북 현대 포지셔닝 히트맵 일치율 64%. 조현우(울산 HD)과 플레이 패턴 66% 유사. 장기 모니터링 후 재평가 권장.",
            "pohang":  "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 포항 스틸러스 포지셔닝 히트맵 일치율 69%. 조현우(울산 HD)과 플레이 패턴 66% 유사. 추가 성장 후 재평가 권장.",
        },
    },
    {
        "id": 12, "name": "신승민", "number": 18,
        "birth_year": 2003, "age": 23,
        "club": "창원FC", "league": "K3",
        "pos": "LB", "emoji": "↙️", "color": "b91c1c",
        "speed": {"overall": 3.4, "press": 2.0, "cover": 4.1, "line": 3.8, "sprint": 4.7},
        "heat_score": {"ulsan": 75, "jeonbuk": 79, "pohang": 73},
        "sim": [
            {"name": "이용",    "club": "전북 현대", "score": 74},
            {"name": "설영우",  "club": "울산 HD",   "score": 70},
            {"name": "황현수",  "club": "전북 현대", "score": 72},
            {"name": "이기혁",  "club": "강원",       "score": 68},
        ],
        "weekly_hearts": 1600, "total_hearts": 8000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 1, "last": "2026-05-12"},
        ],
        "verdict_type": "safe", "change": 9.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 울산 HD 포지셔닝 히트맵 일치율 75%. 이용(전북 현대)과 플레이 패턴 74% 유사. 측면 수비 즉시 선발 경쟁 투입 권장.",
            "jeonbuk": "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 전북 현대 포지셔닝 히트맵 일치율 79%. 이용(전북 현대)과 플레이 패턴 74% 유사. 전북 좌측 수비 즉시 보강 권장.",
            "pohang":  "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 포항 스틸러스 포지셔닝 히트맵 일치율 73%. 이용(전북 현대)과 플레이 패턴 74% 유사. 포항 LB 즉시 전력화 가능.",
        },
    },
    {
        "id": 13, "name": "박진홍", "number": 5,
        "birth_year": 2004, "age": 22,
        "club": "창원FC", "league": "K3",
        "pos": "CDM", "emoji": "⚓", "color": "b91c1c",
        "speed": {"overall": 3.7, "press": 2.1, "cover": 4.3, "line": 4.0, "sprint": 4.9},
        "heat_score": {"ulsan": 72, "jeonbuk": 69, "pohang": 74},
        "sim": [
            {"name": "이순민",  "club": "수원FC",   "score": 72},
            {"name": "홍윤상",  "club": "포항",      "score": 70},
            {"name": "원두재",  "club": "울산 HD",  "score": 68},
            {"name": "이진현",  "club": "포항",      "score": 66},
        ],
        "weekly_hearts": 1000, "total_hearts": 5000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "포항스틸러스", "count": 1, "last": "2026-04-30"},
        ],
        "verdict_type": "caution", "change": 7.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 울산 HD 포지셔닝 히트맵 일치율 72%. 이순민(수원FC)과 플레이 패턴 72% 유사. 추가 성장 후 재평가 권장.",
            "jeonbuk": "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 전북 현대 포지셔닝 히트맵 일치율 69%. 이순민(수원FC)과 플레이 패턴 72% 유사. 6개월 후 재스카우팅 권장.",
            "pohang":  "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 포항 스틸러스 포지셔닝 히트맵 일치율 74%. 이순민(수원FC)과 플레이 패턴 72% 유사. 임대 후 성장세 확인 필요.",
        },
    },
    {
        "id": 14, "name": "장영기", "number": 15,
        "birth_year": 2003, "age": 23,
        "club": "창원FC", "league": "K3",
        "pos": "LW", "emoji": "💨", "color": "b91c1c",
        "speed": {"overall": 3.2, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 80, "jeonbuk": 77, "pohang": 83},
        "sim": [
            {"name": "엄원상",  "club": "울산 HD", "score": 80},
            {"name": "양현준",  "club": "강원",     "score": 76},
            {"name": "이동준",  "club": "전남",     "score": 73},
            {"name": "이강인",  "club": "PSG",      "score": 70},
        ],
        "weekly_hearts": 1800, "total_hearts": 10800,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 2, "last": "2026-05-21"},
            {"club": "전북현대", "count": 1, "last": "2026-05-07"},
        ],
        "verdict_type": "safe", "change": 13.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 울산 HD 포지셔닝 히트맵 일치율 80%. 엄원상(울산 HD)과 플레이 패턴 80% 유사. 측면 돌파력 즉시 영입 권장.",
            "jeonbuk": "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 전북 현대 포지셔닝 히트맵 일치율 77%. 엄원상(울산 HD)과 플레이 패턴 80% 유사. 전북 좌측 날개 즉시 전력화 가능.",
            "pohang":  "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 83%. 엄원상(울산 HD)과 플레이 패턴 80% 유사. 포항 윙 즉시 영입 권장.",
        },
    },
    {
        "id": 15, "name": "이동현", "number": 99,
        "birth_year": 2005, "age": 21,
        "club": "창원FC", "league": "K3",
        "pos": "ST", "emoji": "⚽", "color": "b91c1c",
        "speed": {"overall": 3.9, "press": 2.2, "cover": 4.4, "line": 4.1, "sprint": 5.1},
        "heat_score": {"ulsan": 65, "jeonbuk": 68, "pohang": 63},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 66},
            {"name": "오세훈",    "club": "서울",       "score": 65},
            {"name": "조규성",    "club": "전북 현대", "score": 67},
            {"name": "일류첸코",  "club": "포항",       "score": 63},
        ],
        "weekly_hearts": 900, "total_hearts": 3600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 4.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 울산 HD 포지셔닝 히트맵 일치율 65%. 주민규(전북 현대)과 플레이 패턴 66% 유사. 6개월 후 재스카우팅 권장.",
            "jeonbuk": "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 전북 현대 포지셔닝 히트맵 일치율 68%. 주민규(전북 현대)과 플레이 패턴 66% 유사. 추가 성장 후 재평가 권장.",
            "pohang":  "수비 전환 속도 3.9초 (K1 평균 3.8초 대비 +0.1초). 포항 스틸러스 포지셔닝 히트맵 일치율 63%. 주민규(전북 현대)과 플레이 패턴 66% 유사. 장기 모니터링 대상으로 분류.",
        },
    },
])


# ── K4 리그 (15명) ────────────────────────────────────────────────────────────
PLAYERS.extend([
    # ── 세종 SA FC ────────────────────────────────────────────────────────────
    {
        "id": 16, "name": "이재훈", "number": 1,
        "birth_year": 2005, "age": 21,
        "club": "세종 SA FC", "league": "K4",
        "pos": "GK", "emoji": "🧤", "color": "0891b2",
        "speed": {"overall": 4.2, "press": 2.5, "cover": 4.8, "line": 4.5, "sprint": 5.5},
        "heat_score": {"ulsan": 52, "jeonbuk": 50, "pohang": 55},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 52},
            {"name": "양한빈",  "club": "전북 현대", "score": 50},
            {"name": "이창근",  "club": "대전",       "score": 48},
            {"name": "구성윤",  "club": "포항",       "score": 51},
        ],
        "weekly_hearts": 320, "total_hearts": 1600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 4.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 울산 HD 포지셔닝 히트맵 일치율 52%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 전북 현대 포지셔닝 히트맵 일치율 50%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 포항 스틸러스 포지셔닝 히트맵 일치율 55%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 17, "name": "곽승민", "number": 30,
        "birth_year": 2004, "age": 22,
        "club": "세종 SA FC", "league": "K4",
        "pos": "CB", "emoji": "🛡️", "color": "0891b2",
        "speed": {"overall": 4.5, "press": 2.7, "cover": 5.0, "line": 4.7, "sprint": 5.8},
        "heat_score": {"ulsan": 46, "jeonbuk": 44, "pohang": 48},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 50},
            {"name": "임채민",  "club": "울산 HD",   "score": 48},
            {"name": "김영빈",  "club": "광주",       "score": 48},
            {"name": "불투이",  "club": "전북 현대", "score": 49},
        ],
        "weekly_hearts": 260, "total_hearts": 1040,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 2.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 울산 HD 포지셔닝 히트맵 일치율 46%. 홍정호(전북 현대)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 전북 현대 포지셔닝 히트맵 일치율 44%. 홍정호(전북 현대)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 48%. 홍정호(전북 현대)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 18, "name": "성기완", "number": 47,
        "birth_year": 2004, "age": 22,
        "club": "세종 SA FC", "league": "K4",
        "pos": "CM", "emoji": "🎯", "color": "0891b2",
        "speed": {"overall": 3.8, "press": 2.2, "cover": 4.4, "line": 4.1, "sprint": 5.0},
        "heat_score": {"ulsan": 65, "jeonbuk": 63, "pohang": 67},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 65},
            {"name": "이명재",  "club": "울산 HD",   "score": 63},
            {"name": "정우영",  "club": "전북 현대", "score": 62},
            {"name": "김동현",  "club": "서울",       "score": 60},
        ],
        "weekly_hearts": 680, "total_hearts": 3400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 1, "last": "2026-05-10"},
        ],
        "verdict_type": "safe", "change": 8.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 울산 HD 포지셔닝 히트맵 일치율 65%. 박진섭(전북 현대)과 플레이 패턴 65% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "jeonbuk": "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 전북 현대 포지셔닝 히트맵 일치율 63%. 박진섭(전북 현대)과 플레이 패턴 65% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "pohang":  "수비 전환 속도 3.8초 (K1 평균 3.8초 대비 ±0.0초). 포항 스틸러스 포지셔닝 히트맵 일치율 67%. 박진섭(전북 현대)과 플레이 패턴 65% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
        },
    },
    {
        "id": 19, "name": "김원형", "number": 88,
        "birth_year": 2005, "age": 21,
        "club": "세종 SA FC", "league": "K4",
        "pos": "CAM", "emoji": "⚡", "color": "0891b2",
        "speed": {"overall": 4.0, "press": 2.3, "cover": 4.5, "line": 4.2, "sprint": 5.1},
        "heat_score": {"ulsan": 60, "jeonbuk": 58, "pohang": 62},
        "sim": [
            {"name": "이동경",  "club": "울산 HD",   "score": 60},
            {"name": "강성진",  "club": "전북 현대", "score": 58},
            {"name": "오현규",  "club": "전북 현대", "score": 57},
            {"name": "엄원상",  "club": "울산 HD",   "score": 55},
        ],
        "weekly_hearts": 540, "total_hearts": 2700,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 6.3,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 울산 HD 포지셔닝 히트맵 일치율 60%. 이동경(울산 HD)과 플레이 패턴 60% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 전북 현대 포지셔닝 히트맵 일치율 58%. 이동경(울산 HD)과 플레이 패턴 60% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 포항 스틸러스 포지셔닝 히트맵 일치율 62%. 이동경(울산 HD)과 플레이 패턴 60% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 20, "name": "육재경", "number": 42,
        "birth_year": 2004, "age": 22,
        "club": "세종 SA FC", "league": "K4",
        "pos": "ST", "emoji": "⚽", "color": "0891b2",
        "speed": {"overall": 4.3, "press": 2.5, "cover": 4.8, "line": 4.5, "sprint": 5.6},
        "heat_score": {"ulsan": 50, "jeonbuk": 48, "pohang": 52},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 52},
            {"name": "오세훈",    "club": "서울",       "score": 50},
            {"name": "조규성",    "club": "전북 현대", "score": 51},
            {"name": "일류첸코",  "club": "포항",       "score": 49},
        ],
        "weekly_hearts": 290, "total_hearts": 1160,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 3.1,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 울산 HD 포지셔닝 히트맵 일치율 50%. 주민규(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 전북 현대 포지셔닝 히트맵 일치율 48%. 주민규(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 포항 스틸러스 포지셔닝 히트맵 일치율 52%. 주민규(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },

    # ── 평택시티즌FC ──────────────────────────────────────────────────────────
    {
        "id": 21, "name": "박지현", "number": 99,
        "birth_year": 2005, "age": 21,
        "club": "평택시티즌FC", "league": "K4",
        "pos": "GK", "emoji": "🧤", "color": "7c3aed",
        "speed": {"overall": 4.4, "press": 2.6, "cover": 4.9, "line": 4.6, "sprint": 5.7},
        "heat_score": {"ulsan": 50, "jeonbuk": 48, "pohang": 52},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 52},
            {"name": "양한빈",  "club": "전북 현대", "score": 50},
            {"name": "이창근",  "club": "대전",       "score": 48},
            {"name": "구성윤",  "club": "포항",       "score": 51},
        ],
        "weekly_hearts": 350, "total_hearts": 1400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 3.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 울산 HD 포지셔닝 히트맵 일치율 50%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 전북 현대 포지셔닝 히트맵 일치율 48%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 52%. 조현우(울산 HD)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 22, "name": "권도윤", "number": 66,
        "birth_year": 2004, "age": 22,
        "club": "평택시티즌FC", "league": "K4",
        "pos": "CB", "emoji": "🛡️", "color": "7c3aed",
        "speed": {"overall": 4.5, "press": 2.7, "cover": 5.1, "line": 4.8, "sprint": 5.9},
        "heat_score": {"ulsan": 48, "jeonbuk": 46, "pohang": 50},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 52},
            {"name": "임채민",  "club": "울산 HD",   "score": 50},
            {"name": "김영빈",  "club": "광주",       "score": 49},
            {"name": "불투이",  "club": "전북 현대", "score": 51},
        ],
        "weekly_hearts": 280, "total_hearts": 1120,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 2.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 울산 HD 포지셔닝 히트맵 일치율 48%. 홍정호(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 전북 현대 포지셔닝 히트맵 일치율 46%. 홍정호(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.5초 (K1 평균 3.8초 대비 +0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 50%. 홍정호(전북 현대)과 플레이 패턴 52% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 23, "name": "구하민", "number": 79,
        "birth_year": 2004, "age": 22,
        "club": "평택시티즌FC", "league": "K4",
        "pos": "CDM", "emoji": "⚓", "color": "7c3aed",
        "speed": {"overall": 4.1, "press": 2.4, "cover": 4.7, "line": 4.4, "sprint": 5.4},
        "heat_score": {"ulsan": 58, "jeonbuk": 56, "pohang": 60},
        "sim": [
            {"name": "이순민",  "club": "수원FC",  "score": 58},
            {"name": "홍윤상",  "club": "포항",     "score": 56},
            {"name": "원두재",  "club": "울산 HD", "score": 55},
            {"name": "이진현",  "club": "포항",     "score": 54},
        ],
        "weekly_hearts": 470, "total_hearts": 2350,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 5.1,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.1초 (K1 평균 3.8초 대비 +0.3초). 울산 HD 포지셔닝 히트맵 일치율 58%. 이순민(수원FC)과 플레이 패턴 58% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.1초 (K1 평균 3.8초 대비 +0.3초). 전북 현대 포지셔닝 히트맵 일치율 56%. 이순민(수원FC)과 플레이 패턴 58% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.1초 (K1 평균 3.8초 대비 +0.3초). 포항 스틸러스 포지셔닝 히트맵 일치율 60%. 이순민(수원FC)과 플레이 패턴 58% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 24, "name": "이도안", "number": 14,
        "birth_year": 2004, "age": 22,
        "club": "평택시티즌FC", "league": "K4",
        "pos": "RW", "emoji": "🔥", "color": "7c3aed",
        "speed": {"overall": 3.6, "press": 2.1, "cover": 4.2, "line": 3.9, "sprint": 4.8},
        "heat_score": {"ulsan": 68, "jeonbuk": 66, "pohang": 70},
        "sim": [
            {"name": "엄원상",  "club": "울산 HD", "score": 68},
            {"name": "양현준",  "club": "강원",     "score": 66},
            {"name": "이동준",  "club": "전남",     "score": 65},
            {"name": "이강인",  "club": "PSG",      "score": 63},
        ],
        "weekly_hearts": 880, "total_hearts": 4400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "인천유나이티드", "count": 1, "last": "2026-05-18"},
        ],
        "verdict_type": "safe", "change": 9.7,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 울산 HD 포지셔닝 히트맵 일치율 68%. 엄원상(울산 HD)과 플레이 패턴 68% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "jeonbuk": "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 전북 현대 포지셔닝 히트맵 일치율 66%. 엄원상(울산 HD)과 플레이 패턴 68% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "pohang":  "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 포항 스틸러스 포지셔닝 히트맵 일치율 70%. 엄원상(울산 HD)과 플레이 패턴 68% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
        },
    },
    {
        "id": 25, "name": "정태율", "number": 22,
        "birth_year": 2005, "age": 21,
        "club": "평택시티즌FC", "league": "K4",
        "pos": "ST", "emoji": "⚽", "color": "7c3aed",
        "speed": {"overall": 4.3, "press": 2.5, "cover": 4.8, "line": 4.5, "sprint": 5.6},
        "heat_score": {"ulsan": 52, "jeonbuk": 50, "pohang": 54},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 54},
            {"name": "오세훈",    "club": "서울",       "score": 52},
            {"name": "조규성",    "club": "전북 현대", "score": 52},
            {"name": "일류첸코",  "club": "포항",       "score": 50},
        ],
        "weekly_hearts": 420, "total_hearts": 1680,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 4.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 울산 HD 포지셔닝 히트맵 일치율 52%. 주민규(전북 현대)과 플레이 패턴 54% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 전북 현대 포지셔닝 히트맵 일치율 50%. 주민규(전북 현대)과 플레이 패턴 54% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.3초 (K1 평균 3.8초 대비 +0.5초). 포항 스틸러스 포지셔닝 히트맵 일치율 54%. 주민규(전북 현대)과 플레이 패턴 54% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },

    # ── 남양주시민구단 ────────────────────────────────────────────────────────
    {
        "id": 26, "name": "김덕화", "number": 21,
        "birth_year": 2004, "age": 22,
        "club": "남양주시민구단", "league": "K4",
        "pos": "GK", "emoji": "🧤", "color": "059669",
        "speed": {"overall": 4.4, "press": 2.6, "cover": 4.9, "line": 4.6, "sprint": 5.6},
        "heat_score": {"ulsan": 50, "jeonbuk": 48, "pohang": 52},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 50},
            {"name": "양한빈",  "club": "전북 현대", "score": 49},
            {"name": "이창근",  "club": "대전",       "score": 47},
            {"name": "구성윤",  "club": "포항",       "score": 49},
        ],
        "weekly_hearts": 220, "total_hearts": 880,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 2.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 울산 HD 포지셔닝 히트맵 일치율 50%. 조현우(울산 HD)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 전북 현대 포지셔닝 히트맵 일치율 48%. 조현우(울산 HD)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.4초 (K1 평균 3.8초 대비 +0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 52%. 조현우(울산 HD)과 플레이 패턴 50% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 27, "name": "정동규", "number": 3,
        "birth_year": 2004, "age": 22,
        "club": "남양주시민구단", "league": "K4",
        "pos": "CB", "emoji": "🛡️", "color": "059669",
        "speed": {"overall": 4.6, "press": 2.8, "cover": 5.2, "line": 4.9, "sprint": 6.0},
        "heat_score": {"ulsan": 45, "jeonbuk": 43, "pohang": 47},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 49},
            {"name": "임채민",  "club": "울산 HD",   "score": 47},
            {"name": "김영빈",  "club": "광주",       "score": 47},
            {"name": "불투이",  "club": "전북 현대", "score": 48},
        ],
        "weekly_hearts": 200, "total_hearts": 800,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 1.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.6초 (K1 평균 3.8초 대비 +0.8초). 울산 HD 포지셔닝 히트맵 일치율 45%. 홍정호(전북 현대)과 플레이 패턴 49% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.6초 (K1 평균 3.8초 대비 +0.8초). 전북 현대 포지셔닝 히트맵 일치율 43%. 홍정호(전북 현대)과 플레이 패턴 49% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.6초 (K1 평균 3.8초 대비 +0.8초). 포항 스틸러스 포지셔닝 히트맵 일치율 47%. 홍정호(전북 현대)과 플레이 패턴 49% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 28, "name": "김성규", "number": 19,
        "birth_year": 2004, "age": 22,
        "club": "남양주시민구단", "league": "K4",
        "pos": "CM", "emoji": "🎯", "color": "059669",
        "speed": {"overall": 4.0, "press": 2.3, "cover": 4.6, "line": 4.3, "sprint": 5.2},
        "heat_score": {"ulsan": 60, "jeonbuk": 58, "pohang": 62},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 61},
            {"name": "이명재",  "club": "울산 HD",   "score": 59},
            {"name": "정우영",  "club": "전북 현대", "score": 60},
            {"name": "김동현",  "club": "서울",       "score": 58},
        ],
        "weekly_hearts": 490, "total_hearts": 2450,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 5.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 울산 HD 포지셔닝 히트맵 일치율 60%. 박진섭(전북 현대)과 플레이 패턴 61% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 전북 현대 포지셔닝 히트맵 일치율 58%. 박진섭(전북 현대)과 플레이 패턴 61% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.0초 (K1 평균 3.8초 대비 +0.2초). 포항 스틸러스 포지셔닝 히트맵 일치율 62%. 박진섭(전북 현대)과 플레이 패턴 61% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
    {
        "id": 29, "name": "이민석", "number": 13,
        "birth_year": 2004, "age": 22,
        "club": "남양주시민구단", "league": "K4",
        "pos": "LW", "emoji": "💨", "color": "059669",
        "speed": {"overall": 3.7, "press": 2.1, "cover": 4.3, "line": 4.0, "sprint": 4.9},
        "heat_score": {"ulsan": 65, "jeonbuk": 63, "pohang": 67},
        "sim": [
            {"name": "엄원상",  "club": "울산 HD", "score": 67},
            {"name": "양현준",  "club": "강원",     "score": 65},
            {"name": "이동준",  "club": "전남",     "score": 64},
            {"name": "이강인",  "club": "PSG",      "score": 62},
        ],
        "weekly_hearts": 590, "total_hearts": 2950,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "safe", "change": 7.4,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 울산 HD 포지셔닝 히트맵 일치율 65%. 엄원상(울산 HD)과 플레이 패턴 67% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "jeonbuk": "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 전북 현대 포지셔닝 히트맵 일치율 63%. 엄원상(울산 HD)과 플레이 패턴 67% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
            "pohang":  "수비 전환 속도 3.7초 (K1 평균 3.8초 대비 -0.1초). 포항 스틸러스 포지셔닝 히트맵 일치율 67%. 엄원상(울산 HD)과 플레이 패턴 67% 유사. K4에서 두각을 나타내며 조기 영입 검토가 권장됩니다.",
        },
    },
    {
        "id": 30, "name": "한성민", "number": 38,
        "birth_year": 2002, "age": 24,
        "club": "남양주시민구단", "league": "K4",
        "pos": "ST", "emoji": "⚽", "color": "059669",
        "speed": {"overall": 4.2, "press": 2.4, "cover": 4.7, "line": 4.4, "sprint": 5.5},
        "heat_score": {"ulsan": 52, "jeonbuk": 50, "pohang": 54},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 53},
            {"name": "오세훈",    "club": "서울",       "score": 52},
            {"name": "조규성",    "club": "전북 현대", "score": 52},
            {"name": "일류첸코",  "club": "포항",       "score": 51},
        ],
        "weekly_hearts": 310, "total_hearts": 1240,
        "is_liked": False, "my_hearts": 0,
        "scouts": [],
        "verdict_type": "caution", "change": 3.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 울산 HD 포지셔닝 히트맵 일치율 52%. 주민규(전북 현대)과 플레이 패턴 53% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "jeonbuk": "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 전북 현대 포지셔닝 히트맵 일치율 50%. 주민규(전북 현대)과 플레이 패턴 53% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
            "pohang":  "수비 전환 속도 4.2초 (K1 평균 3.8초 대비 +0.4초). 포항 스틸러스 포지셔닝 히트맵 일치율 54%. 주민규(전북 현대)과 플레이 패턴 53% 유사. K4 리그 수준으로 즉시 전력화보다 단계적 성장이 필요합니다.",
        },
    },
])


# ── U리그 (15명) ──────────────────────────────────────────────────────────────
PLAYERS.extend([
    # ── 연세대학교 ────────────────────────────────────────────────────────────
    {
        "id": 31, "name": "김현", "number": 1,
        "birth_year": 2004, "age": 22,
        "club": "연세대학교", "league": "U리그",
        "pos": "GK", "emoji": "🧤", "color": "1e40af",
        "speed": {"overall": 3.4, "press": 2.1, "cover": 4.2, "line": 3.9, "sprint": 4.7},
        "heat_score": {"ulsan": 78, "jeonbuk": 75, "pohang": 72},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 80},
            {"name": "양한빈",  "club": "전북 현대", "score": 77},
            {"name": "이창근",  "club": "대전",       "score": 74},
            {"name": "구성윤",  "club": "포항",       "score": 72},
        ],
        "weekly_hearts": 2200, "total_hearts": 13200,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 2, "last": "2026-05-22"},
            {"club": "전북현대", "count": 3, "last": "2026-05-15"},
        ],
        "verdict_type": "caution", "change": 16.4,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 울산 HD 포지셔닝 히트맵 일치율 78%. 조현우(울산 HD)과 플레이 패턴 80% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "jeonbuk": "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 전북 현대 포지셔닝 히트맵 일치율 75%. 조현우(울산 HD)과 플레이 패턴 80% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "pohang":  "수비 전환 속도 3.4초 (K1 평균 3.8초 대비 -0.4초). 포항 스틸러스 포지셔닝 히트맵 일치율 72%. 조현우(울산 HD)과 플레이 패턴 80% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
        },
    },
    {
        "id": 32, "name": "장현도", "number": 3,
        "birth_year": 2004, "age": 22,
        "club": "연세대학교", "league": "U리그",
        "pos": "CB", "emoji": "🛡️", "color": "1e40af",
        "speed": {"overall": 3.5, "press": 2.2, "cover": 4.4, "line": 4.1, "sprint": 5.1},
        "heat_score": {"ulsan": 74, "jeonbuk": 72, "pohang": 70},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 76},
            {"name": "임채민",  "club": "울산 HD",   "score": 74},
            {"name": "김영빈",  "club": "광주",       "score": 72},
            {"name": "불투이",  "club": "전북 현대", "score": 73},
        ],
        "weekly_hearts": 1900, "total_hearts": 11400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 2, "last": "2026-05-18"},
        ],
        "verdict_type": "caution", "change": 14.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 울산 HD 포지셔닝 히트맵 일치율 74%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "jeonbuk": "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 전북 현대 포지셔닝 히트맵 일치율 72%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "pohang":  "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 포항 스틸러스 포지셔닝 히트맵 일치율 70%. 홍정호(전북 현대)과 플레이 패턴 76% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
        },
    },
    {
        "id": 33, "name": "이승민", "number": 5,
        "birth_year": 2003, "age": 23,
        "club": "연세대학교", "league": "U리그",
        "pos": "LB", "emoji": "↙️", "color": "1e40af",
        "speed": {"overall": 3.1, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 82, "jeonbuk": 80, "pohang": 78},
        "sim": [
            {"name": "이용",    "club": "전북 현대", "score": 82},
            {"name": "설영우",  "club": "울산 HD",   "score": 79},
            {"name": "황현수",  "club": "전북 현대", "score": 78},
            {"name": "이기혁",  "club": "강원",       "score": 76},
        ],
        "weekly_hearts": 3200, "total_hearts": 22400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 3, "last": "2026-05-26"},
            {"club": "전북현대", "count": 2, "last": "2026-05-20"},
        ],
        "verdict_type": "safe", "change": 22.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 울산 HD 포지셔닝 히트맵 일치율 82%. 이용(전북 현대)과 플레이 패턴 82% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "jeonbuk": "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 전북 현대 포지셔닝 히트맵 일치율 80%. 이용(전북 현대)과 플레이 패턴 82% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "pohang":  "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 78%. 이용(전북 현대)과 플레이 패턴 82% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
        },
    },
    {
        "id": 34, "name": "최지웅", "number": 8,
        "birth_year": 2004, "age": 22,
        "club": "연세대학교", "league": "U리그",
        "pos": "CAM", "emoji": "⚡", "color": "1e40af",
        "speed": {"overall": 3.0, "press": 1.8, "cover": 3.9, "line": 3.6, "sprint": 4.4},
        "heat_score": {"ulsan": 88, "jeonbuk": 85, "pohang": 83},
        "sim": [
            {"name": "이동경",  "club": "울산 HD",   "score": 89},
            {"name": "강성진",  "club": "전북 현대", "score": 86},
            {"name": "오현규",  "club": "전북 현대", "score": 83},
            {"name": "엄원상",  "club": "울산 HD",   "score": 80},
        ],
        "weekly_hearts": 4000, "total_hearts": 32000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",       "count": 4, "last": "2026-05-30"},
            {"club": "인천유나이티드", "count": 2, "last": "2026-05-22"},
        ],
        "verdict_type": "safe", "change": 31.5,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 울산 HD 포지셔닝 히트맵 일치율 88%. 이동경(울산 HD)과 플레이 패턴 89% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "jeonbuk": "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 전북 현대 포지셔닝 히트맵 일치율 85%. 이동경(울산 HD)과 플레이 패턴 89% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "pohang":  "수비 전환 속도 3.0초 (K1 평균 3.8초 대비 -0.8초). 포항 스틸러스 포지셔닝 히트맵 일치율 83%. 이동경(울산 HD)과 플레이 패턴 89% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
        },
    },
    {
        "id": 35, "name": "장현빈", "number": 9,
        "birth_year": 2004, "age": 22,
        "club": "연세대학교", "league": "U리그",
        "pos": "ST", "emoji": "⚽", "color": "1e40af",
        "speed": {"overall": 3.2, "press": 2.0, "cover": 4.1, "line": 3.8, "sprint": 4.7},
        "heat_score": {"ulsan": 76, "jeonbuk": 74, "pohang": 72},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 78},
            {"name": "오세훈",    "club": "서울",       "score": 76},
            {"name": "조규성",    "club": "전북 현대", "score": 74},
            {"name": "일류첸코",  "club": "포항",       "score": 72},
        ],
        "weekly_hearts": 2800, "total_hearts": 19600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대",   "count": 3, "last": "2026-05-25"},
            {"club": "포항스틸러스", "count": 2, "last": "2026-05-14"},
        ],
        "verdict_type": "caution", "change": 19.7,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 울산 HD 포지셔닝 히트맵 일치율 76%. 주민규(전북 현대)과 플레이 패턴 78% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "jeonbuk": "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 전북 현대 포지셔닝 히트맵 일치율 74%. 주민규(전북 현대)과 플레이 패턴 78% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
            "pohang":  "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 72%. 주민규(전북 현대)과 플레이 패턴 78% 유사. U리그 최강권 출신으로 즉시 전력화 가능성이 높습니다.",
        },
    },

    # ── 고려대학교 ────────────────────────────────────────────────────────────
    {
        "id": 36, "name": "김정훈", "number": 1,
        "birth_year": 2004, "age": 22,
        "club": "고려대학교", "league": "U리그",
        "pos": "GK", "emoji": "🧤", "color": "991b1b",
        "speed": {"overall": 3.5, "press": 2.1, "cover": 4.2, "line": 3.9, "sprint": 4.7},
        "heat_score": {"ulsan": 72, "jeonbuk": 70, "pohang": 68},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 74},
            {"name": "양한빈",  "club": "전북 현대", "score": 72},
            {"name": "이창근",  "club": "대전",       "score": 70},
            {"name": "구성윤",  "club": "포항",       "score": 71},
        ],
        "weekly_hearts": 1800, "total_hearts": 10800,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD", "count": 2, "last": "2026-05-20"},
        ],
        "verdict_type": "caution", "change": 15.1,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 울산 HD 포지셔닝 히트맵 일치율 72%. 조현우(울산 HD)과 플레이 패턴 74% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "jeonbuk": "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 전북 현대 포지셔닝 히트맵 일치율 70%. 조현우(울산 HD)과 플레이 패턴 74% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "pohang":  "수비 전환 속도 3.5초 (K1 평균 3.8초 대비 -0.3초). 포항 스틸러스 포지셔닝 히트맵 일치율 68%. 조현우(울산 HD)과 플레이 패턴 74% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
        },
    },
    {
        "id": 37, "name": "조예성", "number": 5,
        "birth_year": 2004, "age": 22,
        "club": "고려대학교", "league": "U리그",
        "pos": "CB", "emoji": "🛡️", "color": "991b1b",
        "speed": {"overall": 3.6, "press": 2.2, "cover": 4.4, "line": 4.1, "sprint": 5.1},
        "heat_score": {"ulsan": 70, "jeonbuk": 68, "pohang": 65},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 72},
            {"name": "임채민",  "club": "울산 HD",   "score": 70},
            {"name": "김영빈",  "club": "광주",       "score": 68},
            {"name": "불투이",  "club": "전북 현대", "score": 70},
        ],
        "weekly_hearts": 1600, "total_hearts": 9600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대", "count": 1, "last": "2026-05-16"},
        ],
        "verdict_type": "caution", "change": 13.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 울산 HD 포지셔닝 히트맵 일치율 70%. 홍정호(전북 현대)과 플레이 패턴 72% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "jeonbuk": "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 전북 현대 포지셔닝 히트맵 일치율 68%. 홍정호(전북 현대)과 플레이 패턴 72% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "pohang":  "수비 전환 속도 3.6초 (K1 평균 3.8초 대비 -0.2초). 포항 스틸러스 포지셔닝 히트맵 일치율 65%. 홍정호(전북 현대)과 플레이 패턴 72% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
        },
    },
    {
        "id": 38, "name": "동재민", "number": 6,
        "birth_year": 2004, "age": 22,
        "club": "고려대학교", "league": "U리그",
        "pos": "CM", "emoji": "🎯", "color": "991b1b",
        "speed": {"overall": 3.2, "press": 2.0, "cover": 4.1, "line": 3.8, "sprint": 4.6},
        "heat_score": {"ulsan": 82, "jeonbuk": 80, "pohang": 78},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 84},
            {"name": "이명재",  "club": "울산 HD",   "score": 82},
            {"name": "정우영",  "club": "전북 현대", "score": 80},
            {"name": "김동현",  "club": "서울",       "score": 78},
        ],
        "weekly_hearts": 3500, "total_hearts": 24500,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",   "count": 3, "last": "2026-05-28"},
            {"club": "전북현대", "count": 3, "last": "2026-05-21"},
        ],
        "verdict_type": "safe", "change": 27.4,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 울산 HD 포지셔닝 히트맵 일치율 82%. 박진섭(전북 현대)과 플레이 패턴 84% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "jeonbuk": "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 전북 현대 포지셔닝 히트맵 일치율 80%. 박진섭(전북 현대)과 플레이 패턴 84% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "pohang":  "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 78%. 박진섭(전북 현대)과 플레이 패턴 84% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
        },
    },
    {
        "id": 39, "name": "김지원", "number": 9,
        "birth_year": 2004, "age": 22,
        "club": "고려대학교", "league": "U리그",
        "pos": "CAM", "emoji": "⚡", "color": "991b1b",
        "speed": {"overall": 3.1, "press": 1.9, "cover": 3.9, "line": 3.6, "sprint": 4.4},
        "heat_score": {"ulsan": 86, "jeonbuk": 83, "pohang": 81},
        "sim": [
            {"name": "이동경",  "club": "울산 HD",   "score": 88},
            {"name": "강성진",  "club": "전북 현대", "score": 85},
            {"name": "오현규",  "club": "전북 현대", "score": 82},
            {"name": "엄원상",  "club": "울산 HD",   "score": 80},
        ],
        "weekly_hearts": 3800, "total_hearts": 30400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",       "count": 3, "last": "2026-05-29"},
            {"club": "인천유나이티드", "count": 2, "last": "2026-05-18"},
        ],
        "verdict_type": "safe", "change": 30.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 울산 HD 포지셔닝 히트맵 일치율 86%. 이동경(울산 HD)과 플레이 패턴 88% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "jeonbuk": "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 전북 현대 포지셔닝 히트맵 일치율 83%. 이동경(울산 HD)과 플레이 패턴 88% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "pohang":  "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 81%. 이동경(울산 HD)과 플레이 패턴 88% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
        },
    },
    {
        "id": 40, "name": "박찬이", "number": 11,
        "birth_year": 2005, "age": 21,
        "club": "고려대학교", "league": "U리그",
        "pos": "ST", "emoji": "⚽", "color": "991b1b",
        "speed": {"overall": 3.3, "press": 2.0, "cover": 4.1, "line": 3.8, "sprint": 4.7},
        "heat_score": {"ulsan": 76, "jeonbuk": 74, "pohang": 72},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 77},
            {"name": "오세훈",    "club": "서울",       "score": 75},
            {"name": "조규성",    "club": "전북 현대", "score": 74},
            {"name": "일류첸코",  "club": "포항",       "score": 72},
        ],
        "weekly_hearts": 2800, "total_hearts": 19600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대",   "count": 2, "last": "2026-05-24"},
            {"club": "포항스틸러스", "count": 1, "last": "2026-05-12"},
        ],
        "verdict_type": "caution", "change": 18.6,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 울산 HD 포지셔닝 히트맵 일치율 76%. 주민규(전북 현대)과 플레이 패턴 77% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "jeonbuk": "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 전북 현대 포지셔닝 히트맵 일치율 74%. 주민규(전북 현대)과 플레이 패턴 77% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
            "pohang":  "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 포항 스틸러스 포지셔닝 히트맵 일치율 72%. 주민규(전북 현대)과 플레이 패턴 77% 유사. 고려대 핵심 자원으로 프로 적응력이 검증된 선수입니다.",
        },
    },

    # ── 한남대학교 ────────────────────────────────────────────────────────────
    {
        "id": 41, "name": "김용범", "number": 1,
        "birth_year": 2003, "age": 23,
        "club": "한남대학교", "league": "U리그",
        "pos": "GK", "emoji": "🧤", "color": "b45309",
        "speed": {"overall": 3.2, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.5},
        "heat_score": {"ulsan": 80, "jeonbuk": 78, "pohang": 76},
        "sim": [
            {"name": "조현우",  "club": "울산 HD",   "score": 80},
            {"name": "양한빈",  "club": "전북 현대", "score": 78},
            {"name": "이창근",  "club": "대전",       "score": 76},
            {"name": "구성윤",  "club": "포항",       "score": 74},
        ],
        "weekly_hearts": 3200, "total_hearts": 22400,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",     "count": 3, "last": "2026-05-28"},
            {"club": "전북현대",   "count": 2, "last": "2026-05-20"},
            {"club": "포항스틸러스", "count": 2, "last": "2026-05-10"},
        ],
        "verdict_type": "caution", "change": 22.4,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 울산 HD 포지셔닝 히트맵 일치율 80%. 조현우(울산 HD)과 플레이 패턴 80% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "jeonbuk": "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 전북 현대 포지셔닝 히트맵 일치율 78%. 조현우(울산 HD)과 플레이 패턴 80% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "pohang":  "수비 전환 속도 3.2초 (K1 평균 3.8초 대비 -0.6초). 포항 스틸러스 포지셔닝 히트맵 일치율 76%. 조현우(울산 HD)과 플레이 패턴 80% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
        },
    },
    {
        "id": 42, "name": "오준서", "number": 2,
        "birth_year": 2004, "age": 22,
        "club": "한남대학교", "league": "U리그",
        "pos": "CB", "emoji": "🛡️", "color": "b45309",
        "speed": {"overall": 3.3, "press": 2.0, "cover": 4.1, "line": 3.8, "sprint": 4.8},
        "heat_score": {"ulsan": 84, "jeonbuk": 82, "pohang": 80},
        "sim": [
            {"name": "홍정호",  "club": "전북 현대", "score": 84},
            {"name": "임채민",  "club": "울산 HD",   "score": 82},
            {"name": "김영빈",  "club": "광주",       "score": 80},
            {"name": "불투이",  "club": "전북 현대", "score": 78},
        ],
        "weekly_hearts": 2800, "total_hearts": 19600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "전북현대",   "count": 4, "last": "2026-05-27"},
            {"club": "울산HD",     "count": 3, "last": "2026-05-19"},
            {"club": "포항스틸러스", "count": 2, "last": "2026-05-09"},
        ],
        "verdict_type": "safe", "change": 20.8,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 울산 HD 포지셔닝 히트맵 일치율 84%. 홍정호(전북 현대)과 플레이 패턴 84% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "jeonbuk": "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 전북 현대 포지셔닝 히트맵 일치율 82%. 홍정호(전북 현대)과 플레이 패턴 84% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "pohang":  "수비 전환 속도 3.3초 (K1 평균 3.8초 대비 -0.5초). 포항 스틸러스 포지셔닝 히트맵 일치율 80%. 홍정호(전북 현대)과 플레이 패턴 84% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
        },
    },
    {
        "id": 43, "name": "조현준", "number": 8,
        "birth_year": 2004, "age": 22,
        "club": "한남대학교", "league": "U리그",
        "pos": "CM", "emoji": "🎯", "color": "b45309",
        "speed": {"overall": 2.9, "press": 1.8, "cover": 3.8, "line": 3.5, "sprint": 4.3},
        "heat_score": {"ulsan": 88, "jeonbuk": 86, "pohang": 84},
        "sim": [
            {"name": "박진섭",  "club": "전북 현대", "score": 90},
            {"name": "이명재",  "club": "울산 HD",   "score": 88},
            {"name": "정우영",  "club": "전북 현대", "score": 86},
            {"name": "김동현",  "club": "서울",       "score": 84},
        ],
        "weekly_hearts": 4500, "total_hearts": 36000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",     "count": 5, "last": "2026-06-01"},
            {"club": "전북현대",   "count": 4, "last": "2026-05-25"},
            {"club": "포항스틸러스", "count": 3, "last": "2026-05-15"},
        ],
        "verdict_type": "safe", "change": 32.7,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 울산 HD 포지셔닝 히트맵 일치율 88%. 박진섭(전북 현대)과 플레이 패턴 90% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "jeonbuk": "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 전북 현대 포지셔닝 히트맵 일치율 86%. 박진섭(전북 현대)과 플레이 패턴 90% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "pohang":  "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 포항 스틸러스 포지셔닝 히트맵 일치율 84%. 박진섭(전북 현대)과 플레이 패턴 90% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
        },
    },
    {
        "id": 44, "name": "김민재", "number": 10,
        "birth_year": 2004, "age": 22,
        "club": "한남대학교", "league": "U리그",
        "pos": "CAM", "emoji": "⚡", "color": "b45309",
        "speed": {"overall": 2.9, "press": 1.7, "cover": 3.8, "line": 3.5, "sprint": 4.2},
        "heat_score": {"ulsan": 92, "jeonbuk": 90, "pohang": 88},
        "sim": [
            {"name": "이동경",  "club": "울산 HD",   "score": 91},
            {"name": "강성진",  "club": "전북 현대", "score": 89},
            {"name": "오현규",  "club": "전북 현대", "score": 87},
            {"name": "엄원상",  "club": "울산 HD",   "score": 85},
        ],
        "weekly_hearts": 5000, "total_hearts": 40000,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",     "count": 5, "last": "2026-06-02"},
            {"club": "전북현대",   "count": 5, "last": "2026-05-27"},
            {"club": "포항스틸러스", "count": 3, "last": "2026-05-17"},
        ],
        "verdict_type": "safe", "change": 34.2,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 울산 HD 포지셔닝 히트맵 일치율 92%. 이동경(울산 HD)과 플레이 패턴 91% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "jeonbuk": "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 전북 현대 포지셔닝 히트맵 일치율 90%. 이동경(울산 HD)과 플레이 패턴 91% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "pohang":  "수비 전환 속도 2.9초 (K1 평균 3.8초 대비 -0.9초). 포항 스틸러스 포지셔닝 히트맵 일치율 88%. 이동경(울산 HD)과 플레이 패턴 91% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
        },
    },
    {
        "id": 45, "name": "이호영", "number": 17,
        "birth_year": 2005, "age": 21,
        "club": "한남대학교", "league": "U리그",
        "pos": "ST", "emoji": "⚽", "color": "b45309",
        "speed": {"overall": 3.1, "press": 1.9, "cover": 4.0, "line": 3.7, "sprint": 4.6},
        "heat_score": {"ulsan": 84, "jeonbuk": 82, "pohang": 80},
        "sim": [
            {"name": "주민규",    "club": "전북 현대", "score": 85},
            {"name": "오세훈",    "club": "서울",       "score": 83},
            {"name": "조규성",    "club": "전북 현대", "score": 81},
            {"name": "일류첸코",  "club": "포항",       "score": 79},
        ],
        "weekly_hearts": 4200, "total_hearts": 33600,
        "is_liked": False, "my_hearts": 0,
        "scouts": [
            {"club": "울산HD",     "count": 4, "last": "2026-05-31"},
            {"club": "전북현대",   "count": 3, "last": "2026-05-24"},
            {"club": "제주유나이티드", "count": 2, "last": "2026-05-14"},
        ],
        "verdict_type": "caution", "change": 28.9,
        "ai_verdict": {
            "ulsan":   "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 울산 HD 포지셔닝 히트맵 일치율 84%. 주민규(전북 현대)과 플레이 패턴 85% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "jeonbuk": "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 전북 현대 포지셔닝 히트맵 일치율 82%. 주민규(전북 현대)과 플레이 패턴 85% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
            "pohang":  "수비 전환 속도 3.1초 (K1 평균 3.8초 대비 -0.7초). 포항 스틸러스 포지셔닝 히트맵 일치율 80%. 주민규(전북 현대)과 플레이 패턴 85% 유사. 대학 최강 한남대 핵심 자원으로 다수 K1 구단이 주목하고 있습니다.",
        },
    },
])


# ── 실제 영상 분석 데이터 동적 반영 ──────────────────────────────────────────
# 시흥(1~5) · 연세대(31~35) · 한남대(41~45) 대상
_REAL_DATA_IDS = set(range(1, 6)) | set(range(31, 36)) | set(range(41, 46))

for _p in PLAYERS:
    if _p["id"] in _REAL_DATA_IDS:
        _real_speed, _method = get_real_speed(_p["id"])
        if _real_speed:
            _p["speed"]           = _real_speed
            _p["data_source"]     = "실제 영상 분석"
            _p["analysis_method"] = _method
        else:
            _p["data_source"]     = "AI 추정값"
            _p["analysis_method"] = "estimated"

        _real_heat = get_real_heatmap(_p["id"])
        if _real_heat:
            _p["real_heatmap"] = _real_heat
    else:
        _p["data_source"]     = "AI 추정값"
        _p["analysis_method"] = "estimated"


def get_players_by_league(league: str) -> list:
    return [p for p in PLAYERS if p["league"] == league]


def get_players_by_club(club: str) -> list:
    return [p for p in PLAYERS if p["club"] == club]


def get_player_by_id(pid: int) -> dict:
    return next((p for p in PLAYERS if p["id"] == pid), None)


def get_top_by_hearts(n: int = 10) -> list:
    return sorted(PLAYERS, key=lambda p: p["weekly_hearts"], reverse=True)[:n]


def get_verdict_color(verdict_type: str) -> str:
    return {"safe": "#10b981", "caution": "#f5a623"}.get(verdict_type, "#64748b")


def get_speed_color(speed: float, avg: float = 3.8) -> str:
    diff = speed - avg
    if diff <= -0.3:
        return "#10b981"
    elif diff >= 0.5:
        return "#ef4444"
    return "#f5a623"


def get_players_by_pos(pos: str) -> list:
    return [p for p in PLAYERS if p["pos"] == pos]


def search_players(query: str) -> list:
    q = query.lower()
    return [p for p in PLAYERS if
            q in p["name"].lower() or
            q in p["club"].lower() or
            q in p["pos"].lower() or
            q in p["league"].lower()]


if __name__ == "__main__":
    print(f"총 선수 수: {len(PLAYERS)}명")
    for league in ["K3", "K4", "U리그"]:
        count = len(get_players_by_league(league))
        print(f"{league}: {count}명")
