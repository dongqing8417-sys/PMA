import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# =========================================================
# Global style
# =========================================================
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.titlesize": 12.5,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "figure.dpi": 150
})

# =========================================================
# Data
# =========================================================
models = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]
paradigms = ["LH", "CD", "FID", "SO", "DR"]

# Replication classes from your finalized Figure 2 / Figure 5
# F = failed, P = partial, S = strong
replication_class = {
    "Base":   ["F", "F", "F", "F", "F"],
    "Affect": ["P", "P", "F", "P", "F"],
    "Self":   ["P", "P", "P", "S", "P"],
    "Sim":    ["F", "P", "P", "P", "P"],
    "Core":   ["S", "P", "S", "S", "S"],
    "PMA":    ["S", "S", "S", "S", "S"],
}

# Numeric mapping
score_map = {"F": 0, "P": 1, "S": 2}
loss_map  = {"F": 2, "P": 1, "S": 0}

score_matrix = np.array([[score_map[x] for x in replication_class[m]] for m in models])
loss_matrix  = np.array([[loss_map[x]  for x in replication_class[m]] for m in models])

mean_score = score_matrix.mean(axis=1)
mean_loss = loss_matrix.mean(axis=1)
strong_count = (score_matrix == 2).sum(axis=1)

# Contribution vs Base
base_scores = score_matrix[0]
gain_matrix = score_matrix - base_scores

# Model colors
model_colors = {
    "Base":   "#b5b5b5",
    "Affect": "#d5a053",
    "Self":   "#8f73b9",
    "Sim":    "#53b0ad",
    "Core":   "#3b84c4",
    "PMA":    "#cc4a78",
}

# =========================================================
# Figure layout
# =========================================================
fig = plt.figure(figsize=(14.2, 8.2))
gs = fig.add_gridspec(
    2, 3,
    width_ratios=[1.15, 1.0, 1.0],
    height_ratios=[1.0, 1.0],
    left=0.055, right=0.985, top=0.965, bottom=0.085,
    wspace=0.40, hspace=0.42
)

# =========================================================
# a. Replication-state heatmap
# =========================================================
ax1 = fig.add_subplot(gs[0, 0])

heat_cmap = ListedColormap(["#d9d9d9", "#9ecae1", "#3182bd"])
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], heat_cmap.N)

im = ax1.imshow(score_matrix, cmap=heat_cmap, norm=norm, aspect="auto")

ax1.set_xticks(np.arange(len(paradigms)))
ax1.set_xticklabels(paradigms)
ax1.set_yticks(np.arange(len(models)))
ax1.set_yticklabels(models)

for i in range(score_matrix.shape[0]):
    for j in range(score_matrix.shape[1]):
        label = replication_class[models[i]][j]
        val = score_matrix[i, j]
        txt_color = "white" if val == 2 else "black"
        ax1.text(j, i, label, ha="center", va="center",
                 fontsize=11.5, fontweight="bold", color=txt_color)

# cell borders
for i in range(score_matrix.shape[0] + 1):
    ax1.axhline(i - 0.5, color="white", lw=1.2)
for j in range(score_matrix.shape[1] + 1):
    ax1.axvline(j - 0.5, color="white", lw=1.2)

ax1.set_title("a  Cross-paradigm replication class", loc="left", pad=2)

legend_handles = [
    Patch(facecolor="#3182bd", edgecolor="none", label="Strong"),
    Patch(facecolor="#9ecae1", edgecolor="none", label="Partial"),
    Patch(facecolor="#d9d9d9", edgecolor="none", label="Failed"),
]
ax1.legend(
    handles=legend_handles,
    frameon=False,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.23),
    ncol=3,
    handlelength=1.0,
    columnspacing=1.4
)

# =========================================================
# b. Mean replication score
# =========================================================
ax2 = fig.add_subplot(gs[0, 1])

ypos = np.arange(len(models))
bar_colors = [model_colors[m] for m in models]
ax2.barh(ypos, mean_score, color=bar_colors, height=0.62)

for y, v in zip(ypos, mean_score):
    ax2.text(v + 0.04, y, f"{v:.1f}", va="center", ha="left", fontsize=10)

for x in [0.5, 1.0, 1.5]:
    ax2.axvline(x, color="#aaaaaa", lw=0.8, ls="--", alpha=0.7, zorder=0)

ax2.set_yticks(ypos)
ax2.set_yticklabels(models)
ax2.invert_yaxis()
ax2.set_xlim(0, 2.05)
ax2.set_xlabel("Mean replication score")
ax2.set_title("b  Ablation-level gain", loc="left", pad=2)

# =========================================================
# c. Error distribution across paradigms
# =========================================================
ax3 = fig.add_subplot(gs[0, 2])

x = np.arange(len(models))
rng = np.random.default_rng(2)

for i, m in enumerate(models):
    vals = loss_matrix[i]
    jitter = np.linspace(-0.08, 0.08, len(vals))
    ax3.scatter(
        np.full(len(vals), i) + jitter,
        vals,
        s=52,
        color=model_colors[m],
        edgecolor="white",
        linewidth=0.8,
        zorder=3
    )
    mu = vals.mean()
    sd = vals.std(ddof=1) if len(vals) > 1 else 0
    ax3.errorbar(i, mu, yerr=sd, color="black", fmt="_",
                 markersize=18, elinewidth=1.1, capsize=3, zorder=4)

ax3.text(0.02, 0.97, "lower is better", transform=ax3.transAxes,
         ha="left", va="top", fontsize=9, color="#666666")

ax3.set_xticks(x)
ax3.set_xticklabels(models, rotation=35, ha="right")
ax3.set_ylabel("Fidelity loss")
ax3.set_ylim(-0.1, 2.15)
ax3.set_yticks([0, 1, 2])
ax3.grid(axis="y", linestyle="--", alpha=0.35)
ax3.set_title("c  Error distribution across paradigms", loc="left", pad=2)

# =========================================================
# d. Paradigm-wise robustness (selected models)
# =========================================================
ax4 = fig.add_subplot(gs[1, 0])

selected = ["Base", "Core", "PMA"]
x_par = np.arange(len(paradigms))

for m in selected:
    vals = [score_map[s] for s in replication_class[m]]
    ax4.plot(
        x_par, vals,
        marker="o",
        ms=5.5,
        lw=2.0,
        color=model_colors[m],
        label=m
    )

ax4.set_xticks(x_par)
ax4.set_xticklabels(paradigms)
ax4.set_yticks([0, 1, 2])
ax4.set_yticklabels(["Failed", "Partial", "Strong"])
ax4.set_ylim(-0.1, 2.15)
ax4.grid(axis="y", linestyle="--", alpha=0.35)
ax4.set_ylabel("Replication level")
ax4.set_title("d  Paradigm-wise robustness", loc="left", pad=2)
ax4.legend(frameon=False, loc="lower right")

# =========================================================
# e. Component-effect contribution
# =========================================================
ax5 = fig.add_subplot(gs[1, 1])

# bubble sizes for gain
size_map = {0: 26, 1: 120, 2: 230}
color_map = {0: "#d0d0d0", 1: "#9ecae1", 2: "#3182bd"}

for i, m in enumerate(models):
    for j, p in enumerate(paradigms):
        g = int(gain_matrix[i, j])
        ax5.scatter(
            j, i,
            s=size_map[g],
            color=color_map[g],
            edgecolor="white",
            linewidth=0.8,
            zorder=3
        )
        txt = f"+{g}"
        txt_color = "white" if g == 2 else "black"
        ax5.text(j, i, txt, ha="center", va="center",
                 fontsize=8.5, fontweight="bold", color=txt_color)

ax5.set_xticks(np.arange(len(paradigms)))
ax5.set_xticklabels(paradigms)
ax5.set_yticks(np.arange(len(models)))
ax5.set_yticklabels(models)
ax5.invert_yaxis()
ax5.set_xlim(-0.5, len(paradigms) - 0.5)
ax5.set_ylim(len(models) - 0.5, -0.5)

# grid
for i in range(len(models) + 1):
    ax5.axhline(i - 0.5, color="#e5e5e5", lw=0.8, zorder=0)
for j in range(len(paradigms) + 1):
    ax5.axvline(j - 0.5, color="#e5e5e5", lw=0.8, zorder=0)

ax5.set_title("e  Component-effect contribution", loc="left", pad=2)

legend_handles = [
    plt.scatter([], [], s=size_map[0], color=color_map[0], label="+0"),
    plt.scatter([], [], s=size_map[1], color=color_map[1], label="+1"),
    plt.scatter([], [], s=size_map[2], color=color_map[2], label="+2"),
]
ax5.legend(
    handles=legend_handles,
    title="Gain vs Base",
    frameon=False,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),
    ncol=3,
    columnspacing=1.2,
    handletextpad=0.6
)

# =========================================================
# f. Summary landscape
# =========================================================
ax6 = fig.add_subplot(gs[1, 2])

# desirable region: many strong replications + low loss
ax6.axvspan(4, 5.25, color="#f3dce6", alpha=0.65, zorder=0)
ax6.axhspan(0, 0.45, color="#f3dce6", alpha=0.30, zorder=0)
ax6.text(4.12, 0.07, "best\nregion", fontsize=9.5, color="#8b4f67")

for m in models:
    i = models.index(m)
    ax6.scatter(
        strong_count[i], mean_loss[i],
        s=140,
        color=model_colors[m],
        edgecolor="white",
        linewidth=0.9,
        zorder=3
    )

# label offsets to reduce overlap
offsets = {
    "Base": (0.10, 0.05),
    "Affect": (0.10, 0.05),
    "Self": (0.10, 0.03),
    "Sim": (0.10, 0.03),
    "Core": (0.10, 0.02),
    "PMA": (-0.25, 0.03),
}

for m in models:
    i = models.index(m)
    dx, dy = offsets[m]
    ax6.text(strong_count[i] + dx, mean_loss[i] + dy, m, fontsize=10)

ax6.set_xlim(-0.3, 5.3)
ax6.set_ylim(-0.05, 2.1)
ax6.set_xlabel("Number of strong replications")
ax6.set_ylabel("Mean fidelity loss")
ax6.grid(True, linestyle="--", alpha=0.35)
ax6.set_title("f  Summary landscape", loc="left", pad=2)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
fig.savefig(OUTPUT_DIR / "Figure6.pdf", bbox_inches="tight")
plt.show()