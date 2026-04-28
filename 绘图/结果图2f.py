import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

# =========================
# 1. Data
# =========================
models = [
    "Base-Agent",
    "PMA-Affect",
    "PMA-Self",
    "PMA-Sim",
    "PMA-Core",
    "PMA"
]

experiments = [
    "Learned\nhelplessness",
    "Cognitive\ndissonance",
    "Foot-in-the-\ndoor",
    "Social\nostracism",
    "Diffusion of\nresponsibility"
]

# Replication score:
# 0 = Failed
# 1 = Partial
# 2 = Strong
#
# Based on the conclusions we summarized earlier:
# Base-Agent:       F, F, F, F, F
# PMA-Affect:       P, P, F, P, F
# PMA-Self:         P, P, P, S, P
# PMA-Sim:          F, P, P, P, P
# PMA-Core:         S, P, S, S, S
# PMA:              S, S, S, S, S

replication_matrix = np.array([
    [0, 0, 0, 0, 0],  # Base-Agent
    [1, 1, 0, 1, 0],  # PMA-Affect
    [1, 1, 1, 2, 1],  # PMA-Self
    [0, 1, 1, 1, 1],  # PMA-Sim
    [2, 1, 2, 2, 2],  # PMA-Core
    [2, 2, 2, 2, 2],  # PMA
])

# Count Strong / Partial / Failed for Panel b
failed_counts = np.sum(replication_matrix == 0, axis=1)
partial_counts = np.sum(replication_matrix == 1, axis=1)
strong_counts = np.sum(replication_matrix == 2, axis=1)

# =========================
# 2. Figure setup
# =========================
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.linewidth": 1.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
})

fig = plt.figure(figsize=(13.5, 6.8))
gs = fig.add_gridspec(
    nrows=1, ncols=2,
    width_ratios=[3.4, 1.5],
    wspace=0.30
)

# =========================
# 3. Panel a: heatmap
# =========================
ax1 = fig.add_subplot(gs[0, 0])

# Nature-like restrained palette
# Failed -> light gray
# Partial -> light blue
# Strong -> darker blue
cmap = ListedColormap(["#e6e6e6", "#9ecae1", "#3182bd"])
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

im = ax1.imshow(replication_matrix, cmap=cmap, norm=norm, aspect="auto")

ax1.set_xticks(np.arange(len(experiments)))
ax1.set_xticklabels(experiments)
ax1.set_yticks(np.arange(len(models)))
ax1.set_yticklabels(models)

# Minor grid to make each cell crisp
ax1.set_xticks(np.arange(-0.5, len(experiments), 1), minor=True)
ax1.set_yticks(np.arange(-0.5, len(models), 1), minor=True)
ax1.grid(which="minor", color="white", linestyle="-", linewidth=2)
ax1.tick_params(which="minor", bottom=False, left=False)

# Put letter labels in each cell
score_to_label = {0: "F", 1: "P", 2: "S"}
for i in range(replication_matrix.shape[0]):
    for j in range(replication_matrix.shape[1]):
        val = replication_matrix[i, j]
        txt_color = "black" if val in [0, 1] else "white"
        ax1.text(
            j, i, score_to_label[val],
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            color=txt_color
        )

# Axis styling
ax1.set_title("a  Replication fidelity across psychological paradigms",
              loc="left", fontweight="bold", pad=12)
ax1.tick_params(axis='x', rotation=0, length=0)
ax1.tick_params(axis='y', length=0)

for spine in ax1.spines.values():
    spine.set_visible(False)

# Legend
legend_elements = [
    Patch(facecolor="#3182bd", edgecolor="none", label="Strong"),
    Patch(facecolor="#9ecae1", edgecolor="none", label="Partial"),
    Patch(facecolor="#e6e6e6", edgecolor="none", label="Failed"),
]
ax1.legend(
    handles=legend_elements,
    frameon=False,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=3,
    columnspacing=1.8,
    handlelength=1.5
)

# =========================
# 4. Panel b: summary stacked bar chart
# =========================
ax2 = fig.add_subplot(gs[0, 1])

y_pos = np.arange(len(models))

# Horizontal stacked bars
ax2.barh(y_pos, strong_counts, color="#3182bd", edgecolor="none", label="Strong")
ax2.barh(y_pos, partial_counts, left=strong_counts, color="#9ecae1", edgecolor="none", label="Partial")
ax2.barh(y_pos, failed_counts, left=strong_counts + partial_counts, color="#e6e6e6", edgecolor="none", label="Failed")

ax2.set_yticks(y_pos)
ax2.set_yticklabels(models)
ax2.invert_yaxis()  # align visual order with heatmap top-to-bottom

ax2.set_xlim(0, 5)
ax2.set_xticks(np.arange(0, 6, 1))
ax2.set_xlabel("Number of paradigms")
ax2.set_title("b  Summary across paradigms",
              loc="left", fontweight="bold", pad=12)

# Add text annotations inside / next to bars
for i in range(len(models)):
    s = strong_counts[i]
    p = partial_counts[i]
    f = failed_counts[i]

    if s > 0:
        ax2.text(s / 2, i, str(s), ha="center", va="center",
                 fontsize=10, color="white", fontweight="bold")
    if p > 0:
        ax2.text(s + p / 2, i, str(p), ha="center", va="center",
                 fontsize=10, color="black", fontweight="bold")
    if f > 0:
        ax2.text(s + p + f / 2, i, str(f), ha="center", va="center",
                 fontsize=10, color="black", fontweight="bold")

# Style
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(axis='y', length=0)
ax2.grid(axis="x", linestyle="--", linewidth=0.7, alpha=0.4)

# =========================
# 5. Overall title and layout
# =========================
fig.suptitle(
    "Cross-paradigm replication performance of PMA and its ablated variants",
    fontsize=14, fontweight="bold", y=0.98
)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()