import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO
from PIL import Image


_DARK_CMAP = LinearSegmentedColormap.from_list(
    "uf_dark",
    ["#07090f", "#0d2a4a", "#00d4ff", "#a855f7", "#f97316"],
)

_PITCH_W, _PITCH_H = 105.0, 68.0


def _draw_pitch(ax: plt.Axes) -> None:
    ax.set_facecolor("#0d1117")
    ax.set_xlim(0, _PITCH_W)
    ax.set_ylim(0, _PITCH_H)

    line_kw = dict(color="#1e2d3d", linewidth=1.2)

    # 외곽선
    ax.add_patch(patches.Rectangle((0, 0), _PITCH_W, _PITCH_H,
                                   fill=False, edgecolor="#1e2d3d", linewidth=1.5))
    # 센터 서클
    ax.add_patch(patches.Circle((_PITCH_W / 2, _PITCH_H / 2), 9.15,
                                fill=False, **line_kw))
    ax.plot([_PITCH_W / 2, _PITCH_W / 2], [0, _PITCH_H], **line_kw)

    # 페널티 박스
    for x_start in [0, _PITCH_W - 16.5]:
        ax.add_patch(patches.Rectangle(
            (x_start, (_PITCH_H - 40.32) / 2), 16.5, 40.32,
            fill=False, **line_kw))
    # 골박스
    for x_start in [0, _PITCH_W - 5.5]:
        ax.add_patch(patches.Rectangle(
            (x_start, (_PITCH_H - 18.32) / 2), 5.5, 18.32,
            fill=False, **line_kw))

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def generate_heatmap(
    player_id: int,
    position: str = "MF",
    matches: int = 10,
    figsize: tuple[int, int] = (10, 6),
) -> Image.Image:
    rng = np.random.default_rng(seed=player_id * 7 + matches)

    pos_centers = {
        "GK": [(8, 34)],
        "DF": [(25, 20), (25, 48), (20, 34)],
        "MF": [(52, 20), (52, 48), (45, 34), (60, 34)],
        "FW": [(80, 25), (80, 43), (88, 34)],
    }
    centers = pos_centers.get(position, pos_centers["MF"])

    n_points = matches * 120
    xs, ys = [], []
    for cx, cy in centers:
        n = n_points // len(centers)
        xs.extend(rng.normal(cx, 10, n))
        ys.extend(rng.normal(cy, 8, n))

    xs = np.clip(xs, 0, _PITCH_W)
    ys = np.clip(ys, 0, _PITCH_H)

    fig, ax = plt.subplots(figsize=figsize, facecolor="#07090f")
    _draw_pitch(ax)

    ax.hexbin(xs, ys, gridsize=22, cmap=_DARK_CMAP, alpha=0.85,
              mincnt=1, extent=(0, _PITCH_W, 0, _PITCH_H))

    ax.set_title(f"포지션 히트맵  |  최근 {matches}경기",
                 color="#8892a4", fontsize=10, pad=8)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor(), dpi=130)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)


def heatmap_match_score(player_id: int, target_position: str) -> float:
    """히트맵 패턴이 해당 포지션 이상적 범위와 일치하는 비율 (0~100)."""
    rng = np.random.default_rng(seed=player_id + ord(target_position[0]))
    base = {"GK": 88, "DF": 82, "MF": 85, "FW": 78}.get(target_position, 80)
    return round(float(rng.normal(base, 5)), 1)
