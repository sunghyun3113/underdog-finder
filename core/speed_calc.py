import numpy as np
import pandas as pd


def calc_transition_speed(player_id: int | None = None) -> dict:
    """
    수비→공격 전환 속도 지표를 계산한다.
    실제 환경에서는 영상 분석 결과를 사용하며, 여기서는 시뮬레이션 데이터를 반환한다.
    """
    rng = np.random.default_rng(seed=player_id or 42)

    reaction_ms = float(rng.normal(loc=380, scale=40))   # 반응 시간 (ms)
    sprint_to_pos = float(rng.normal(loc=4.1, scale=0.6)) # 포지션 복귀 시간 (초)
    ball_recovery = float(rng.normal(loc=2.8, scale=0.4)) # 볼 탈취→전진 (초)

    score = max(0.0, min(10.0,
        10 - (reaction_ms - 300) / 60
        - (sprint_to_pos - 3.0) / 1.5
        - (ball_recovery - 2.0) / 1.0
    ))

    return {
        "reaction_ms": round(reaction_ms, 1),
        "sprint_to_pos_sec": round(sprint_to_pos, 2),
        "ball_recovery_sec": round(ball_recovery, 2),
        "transition_score": round(score, 2),
        "grade": _grade(score),
    }


def batch_transition_scores(player_ids: list[int]) -> pd.DataFrame:
    rows = []
    for pid in player_ids:
        r = calc_transition_speed(pid)
        r["player_id"] = pid
        rows.append(r)
    return pd.DataFrame(rows).set_index("player_id")


def _grade(score: float) -> str:
    if score >= 8.5:
        return "S"
    if score >= 7.0:
        return "A"
    if score >= 5.5:
        return "B"
    if score >= 4.0:
        return "C"
    return "D"
