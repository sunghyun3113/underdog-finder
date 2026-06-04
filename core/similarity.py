import numpy as np
import pandas as pd
from core.players import get_all_players


_FEATURE_COLS = [
    "goals", "assists", "pass_accuracy",
    "dribble_success", "transition_speed", "heatmap_match",
]

_PRO_PLAYERS = [
    {"name": "황인범", "position": "MF", "team": "올림피크 리옹", "league": "Ligue 1",
     "goals": 8, "assists": 14, "pass_accuracy": 88.0, "dribble_success": 64.0,
     "transition_speed": 4.8, "heatmap_match": 90.0},
    {"name": "김민재", "position": "DF", "team": "바이에른 뮌헨", "league": "Bundesliga",
     "goals": 3, "assists": 2, "pass_accuracy": 91.0, "dribble_success": 52.0,
     "transition_speed": 3.4, "heatmap_match": 94.0},
    {"name": "조규성", "position": "FW", "team": "미트윌란", "league": "Superliga",
     "goals": 18, "assists": 4, "pass_accuracy": 72.0, "dribble_success": 70.0,
     "transition_speed": 3.6, "heatmap_match": 80.0},
    {"name": "손준호", "position": "MF", "team": "알카디시야", "league": "Saudi Pro League",
     "goals": 5, "assists": 10, "pass_accuracy": 84.0, "dribble_success": 62.0,
     "transition_speed": 4.5, "heatmap_match": 86.0},
    {"name": "이재성", "position": "MF", "team": "마인츠 05", "league": "Bundesliga",
     "goals": 9, "assists": 11, "pass_accuracy": 82.0, "dribble_success": 74.0,
     "transition_speed": 3.9, "heatmap_match": 83.0},
    {"name": "조현우", "position": "GK", "team": "울산 HD", "league": "K리그1",
     "goals": 0, "assists": 0, "pass_accuracy": 78.0, "dribble_success": 0.0,
     "transition_speed": 2.7, "heatmap_match": 96.0},
    {"name": "김진수", "position": "DF", "team": "전북 현대", "league": "K리그1",
     "goals": 2, "assists": 8, "pass_accuracy": 87.0, "dribble_success": 57.0,
     "transition_speed": 3.8, "heatmap_match": 89.0},
]


def _normalise(df: pd.DataFrame) -> np.ndarray:
    arr = df[_FEATURE_COLS].values.astype(float)
    col_max = arr.max(axis=0)
    col_max[col_max == 0] = 1
    return arr / col_max


def find_similar_players(player_id: int, top_n: int = 3) -> list[dict]:
    prospects = get_all_players()
    target = prospects[prospects["id"] == player_id]
    if target.empty:
        return []

    pros_df = pd.DataFrame(_PRO_PLAYERS)
    combined = pd.concat([target[_FEATURE_COLS], pros_df[_FEATURE_COLS]], ignore_index=True)
    normed = _normalise(combined)

    target_vec = normed[0]
    pro_vecs = normed[1:]

    cos_sims = []
    for vec in pro_vecs:
        denom = np.linalg.norm(target_vec) * np.linalg.norm(vec)
        sim = float(np.dot(target_vec, vec) / denom) if denom > 0 else 0.0
        cos_sims.append(round(sim * 100, 1))

    results = []
    for i, sim in enumerate(cos_sims):
        results.append({**_PRO_PLAYERS[i], "similarity": sim})

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_n]


def similarity_radar_data(player_id: int) -> dict:
    """레이더 차트용 정규화 수치 반환."""
    prospects = get_all_players()
    row = prospects[prospects["id"] == player_id]
    if row.empty:
        return {}
    r = row.iloc[0]
    return {
        "득점력": min(r["goals"] / 20 * 100, 100),
        "창의성": min(r["assists"] / 15 * 100, 100),
        "패스": r["pass_accuracy"],
        "드리블": r["dribble_success"],
        "전환속도": min(r["transition_speed"] / 6 * 100, 100),
        "히트맵": r["heatmap_match"],
    }
