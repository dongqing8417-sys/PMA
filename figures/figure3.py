# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
#
# # =========================================================
# # Global style
# # =========================================================
# plt.rcParams.update({
#     "font.family": "DejaVu Sans",
#     "font.size": 9.5,
#     "axes.titlesize": 11.5,
#     "axes.labelsize": 10,
#     "xtick.labelsize": 9,
#     "ytick.labelsize": 9,
#     "axes.linewidth": 0.9,
#     "xtick.major.width": 0.9,
#     "ytick.major.width": 0.9,
# })
#
# # =========================================================
# # Model labels
# # =========================================================
# models_short = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]
#
# model_colors = {
#     "Human": "#222222",
#     "Base": "#bdbdbd",
#     "Affect": "#d9a66b",
#     "Self": "#8c6bb1",
#     "Sim": "#4aa6a6",
#     "Core": "#3182bd",
#     "PMA": "#c23b63",
# }
#
# # =========================================================
# # Panel a: Learned helplessness
# # =========================================================
# lh_mae = {
#     "Base": 14.33,
#     "Affect": 5.17,
#     "Self": 7.00,
#     "Sim": 15.00,
#     "Core": 4.17,
#     "PMA": 3.00,
# }
#
# # =========================================================
# # Panel b: Cognitive dissonance
# # =========================================================
# cd_dpi = {
#     "Base":   [0.35, 0.45, 0.30, -0.35],
#     "Affect": [0.10, 0.55, -0.10, 0.10],
#     "Self":   [0.40, -0.35, -0.30, 0.10],
#     "Sim":    [-0.15, 0.40, 0.45, 0.35],
#     "Core":   [-0.30, 1.30, -0.40, 1.80],
#     "PMA":    [2.95, 2.30, 3.00, 3.80],
# }
# cd_mean = {m: np.mean(vals) for m, vals in cd_dpi.items()}
#
# measure_names = ["Enjoyment", "Learning", "Importance", "Intention"]
# measure_markers = ["o", "s", "^", "D"]
#
# # =========================================================
# # Panel c: Foot-in-the-door
# # =========================================================
# fid_contrasts = {
#     "Base": {
#         "P  One-contact": 4.0,
#         "P  Agree-only": -1.0,
#         "P  Familiarization": -0.5,
#     },
#     "Affect": {
#         "P  One-contact": 2.0,
#         "P  Agree-only": 0.0,
#         "P  Familiarization": 1.5,
#     },
#     "Self": {
#         "P  One-contact": 28.0,
#         "P  Agree-only": 0.0,
#         "P  Familiarization": 17.0,
#     },
#     "Sim": {
#         "P  One-contact": 25.5,
#         "P  Agree-only": 5.0,
#         "P  Familiarization": 9.5,
#     },
#     "Core": {
#         "P  One-contact": 51.0,
#         "P  Agree-only": 16.0,
#         "P  Familiarization": 39.5,
#     },
#     "PMA": {
#         "P  One-contact": 52.5,
#         "P  Agree-only": 18.0,
#         "P  Familiarization": 37.5,
#     },
# }
#
# contrast_names = ["P  One-contact", "P  Agree-only", "P  Familiarization"]
#
# contrast_colors = {
#     "P  One-contact": "#5DA5DA",
#     "P  Agree-only": "#60BD68",
#     "P  Familiarization": "#F17C79",
# }
#
# contrast_markers = {
#     "P  One-contact": "o",
#     "P  Agree-only": "s",
#     "P  Familiarization": "^",
# }
#
# # =========================================================
# # Panel d: Social ostracism
# # =========================================================
# so_need_drop = {
#     "Base": 0.10,
#     "Affect": 0.38,
#     "Self": 3.95,
#     "Sim": 0.65,
#     "Core": 3.20,
#     "PMA": 4.03,
# }
# so_manip_drop = {
#     "Base": -0.05,
#     "Affect": 0.31,
#     "Self": 3.20,
#     "Sim": -0.07,
#     "Core": 2.92,
#     "PMA": 3.40,
# }
#
# # =========================================================
# # Panel e: Diffusion of responsibility
# # =========================================================
# group_sizes = [1, 3, 6]
# dor_rates = {
#     "Human":  [85, 62, 31],
#     "Base":   [100, 96, 100],
#     "Affect": [92, 88, 88],
#     "Self":   [92, 85, 77],
#     "Sim":    [100, 62, 38],
#     "Core":   [92, 69, 31],
#     "PMA":    [90, 65, 28],
# }
#
# # =========================================================
# # Panel f: Summary data
# # 0 = Failed, 1 = Partial, 2 = Strong
# # =========================================================
# summary_experiments_short = ["LH", "CD", "FID", "SO", "DR"]
# summary_matrix = np.array([
#     [0, 0, 0, 0, 0],  # Base
#     [1, 1, 0, 1, 0],  # Affect
#     [1, 1, 1, 2, 1],  # Self
#     [0, 1, 1, 1, 1],  # Sim
#     [2, 1, 2, 2, 2],  # Core
#     [2, 2, 2, 2, 2],  # PMA
# ])
# summary_label = {0: "F", 1: "P", 2: "S"}
# overall_replication_score = summary_matrix.mean(axis=1)
#
# # =========================================================
# # Figure
# # =========================================================
# fig = plt.figure(figsize=(16, 10))
# gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.35)
#
# # =========================================================
# # Panel a: Learned helplessness
# # =========================================================
# ax1 = fig.add_subplot(gs[0, 0])
#
# y = np.arange(len(models_short))
# for i, m in enumerate(models_short):
#     ax1.hlines(i, 0, lh_mae[m], color="#d0d0d0", linewidth=1.8, zorder=1)
#     ax1.scatter(
#         lh_mae[m], i,
#         s=90,
#         color=model_colors[m],
#         edgecolor="white",
#         linewidth=0.8,
#         zorder=3
#     )
#     ax1.text(
#         lh_mae[m] + 0.35,
#         i,
#         f"{lh_mae[m]:.2f}",
#         va="center",
#         ha="left",
#         fontsize=9
#     )
#
# ax1.set_yticks(y)
# ax1.set_yticklabels(models_short)
# ax1.invert_yaxis()
# ax1.set_xlim(0, 16.8)
# ax1.set_xlabel("MAE to human pattern (lower is better)")
# ax1.set_title("a  Learned helplessness", loc="left", fontweight="bold")
# ax1.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
# ax1.spines["top"].set_visible(False)
# ax1.spines["right"].set_visible(False)
# ax1.spines["left"].set_visible(False)
# ax1.tick_params(axis="y", length=0)
#
# # =========================================================
# # Panel b: Cognitive dissonance
# # =========================================================
# ax2 = fig.add_subplot(gs[0, 1])
#
# x = np.arange(len(models_short))
# jitter = np.array([-0.18, -0.06, 0.06, 0.18])
#
# for i, m in enumerate(models_short):
#     vals = cd_dpi[m]
#
#     for j, val in enumerate(vals):
#         ax2.scatter(
#             x[i] + jitter[j],
#             val,
#             s=58,
#             marker=measure_markers[j],
#             facecolor="white",
#             edgecolor=model_colors[m],
#             linewidth=1.3,
#             zorder=3
#         )
#
#     ax2.scatter(
#         x[i],
#         cd_mean[m],
#         s=98,
#         marker="o",
#         color=model_colors[m],
#         edgecolor="black",
#         linewidth=0.6,
#         zorder=4
#     )
#
#     ax2.hlines(
#         cd_mean[m],
#         x[i] - 0.24,
#         x[i] + 0.24,
#         color="black",
#         linewidth=1.0,
#         zorder=4
#     )
#
# ax2.axhline(0, color="black", linewidth=0.9)
# ax2.set_xticks(x)
# ax2.set_xticklabels(models_short)
# ax2.set_ylabel("Dissonance Peak Index")
# ax2.set_title("b  Cognitive dissonance", loc="left", fontweight="bold")
# ax2.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
# ax2.spines["top"].set_visible(False)
# ax2.spines["right"].set_visible(False)
#
# measure_handles = [
#     Line2D(
#         [0], [0],
#         marker=measure_markers[i],
#         color="none",
#         markerfacecolor="white",
#         markeredgecolor="black",
#         markersize=7,
#         label=measure_names[i]
#     )
#     for i in range(4)
# ]
#
# mean_handle = Line2D(
#     [0], [0],
#     marker="o",
#     color="none",
#     markerfacecolor="#555555",
#     markeredgecolor="black",
#     markersize=7,
#     label="Mean"
# )
#
# ax2.legend(
#     handles=measure_handles + [mean_handle],
#     frameon=False,
#     fontsize=8,
#     loc="upper left",
#     handletextpad=0.5,
#     borderpad=0.2,
#     labelspacing=0.35
# )
#
# # =========================================================
# # Panel c: Foot-in-the-door
# # =========================================================
# ax3 = fig.add_subplot(gs[0, 2])
#
# y_pos = np.arange(len(models_short))
# contrast_offsets = {
#     "P  One-contact": -0.18,
#     "P  Agree-only": 0.00,
#     "P  Familiarization": 0.18,
# }
#
# for cname in contrast_names:
#     vals = [fid_contrasts[m][cname] for m in models_short]
#     y_shifted = y_pos + contrast_offsets[cname]
#
#     ax3.scatter(
#         vals,
#         y_shifted,
#         s=88,
#         marker=contrast_markers[cname],
#         color=contrast_colors[cname],
#         edgecolor="white",
#         linewidth=0.7,
#         alpha=0.95,
#         label=cname,
#         zorder=3
#     )
#
# ax3.axvline(0, color="black", linewidth=0.9)
# ax3.set_yticks(y_pos)
# ax3.set_yticklabels(models_short)
# ax3.invert_yaxis()
# ax3.set_xlabel("Contrast in compliance rate (%)")
# ax3.set_title("c  Foot-in-the-door", loc="left", fontweight="bold")
# ax3.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
# ax3.spines["top"].set_visible(False)
# ax3.spines["right"].set_visible(False)
# ax3.spines["left"].set_visible(False)
# ax3.tick_params(axis="y", length=0)
# ax3.legend(
#     frameon=False,
#     fontsize=8.5,
#     loc="upper right",
#     handletextpad=0.5,
#     borderpad=0.2,
#     labelspacing=0.3
# )
#
# # =========================================================
# # Panel d: Social ostracism
# # Dot plot
# # =========================================================
# ax4 = fig.add_subplot(gs[1, 0])
#
# y = np.arange(len(models_short))
#
# need_vals = np.array([so_need_drop[m] for m in models_short])
# manip_vals = np.array([so_manip_drop[m] for m in models_short])
#
# offset = 0.13
#
# for i in range(len(models_short)):
#     ax4.hlines(
#         y=i - offset,
#         xmin=0,
#         xmax=need_vals[i],
#         color="#3182bd",
#         linewidth=2.0,
#         alpha=0.55,
#         zorder=1
#     )
#     ax4.hlines(
#         y=i + offset,
#         xmin=0,
#         xmax=manip_vals[i],
#         color="#9ecae1",
#         linewidth=2.0,
#         alpha=0.65,
#         zorder=1
#     )
#
# ax4.scatter(
#     need_vals,
#     y - offset,
#     s=72,
#     color="#3182bd",
#     edgecolor="white",
#     linewidth=0.8,
#     label="Need-threat drop",
#     zorder=3
# )
#
# ax4.scatter(
#     manip_vals,
#     y + offset,
#     s=72,
#     color="#9ecae1",
#     edgecolor="white",
#     linewidth=0.8,
#     label="Manipulation-check drop",
#     zorder=3
# )
#
# ax4.axvline(0, color="black", linewidth=0.9)
# ax4.set_yticks(y)
# ax4.set_yticklabels(models_short)
# ax4.invert_yaxis()
# ax4.set_xlim(-0.35, 4.35)
# ax4.set_xlabel("Drop score (Inclusion  Ostracism)")
# ax4.set_title("d  Social ostracism", loc="left", fontweight="bold")
# ax4.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
# ax4.spines["top"].set_visible(False)
# ax4.spines["right"].set_visible(False)
# ax4.spines["left"].set_visible(False)
# ax4.tick_params(axis="y", length=0)
# ax4.legend(
#     frameon=False,
#     fontsize=8.5,
#     loc="upper right",
#     handletextpad=0.5,
#     borderpad=0.2,
#     labelspacing=0.3
# )
#
# # =========================================================
# # Panel e: Diffusion of responsibility
# # =========================================================
# ax5 = fig.add_subplot(gs[1, 1])
#
# highlight_models = ["Human", "Base", "Core", "PMA"]
#
# for name, vals in dor_rates.items():
#     if name in highlight_models:
#         lw = 2.6 if name in ["Human", "PMA"] else 2.2
#         alpha = 1.0
#         z = 4
#         ms = 6.5
#     else:
#         lw = 1.3
#         alpha = 0.45
#         z = 2
#         ms = 5.0
#
#     ax5.plot(
#         group_sizes,
#         vals,
#         marker="o",
#         linewidth=lw,
#         markersize=ms,
#         color=model_colors[name],
#         alpha=alpha,
#         label=name,
#         zorder=z
#     )
#
# ax5.set_xticks(group_sizes)
# ax5.set_xlabel("Group size")
# ax5.set_ylabel("Responsibility rate (%)")
# ax5.set_ylim(0, 105)
# ax5.set_title("e  Diffusion of responsibility", loc="left", fontweight="bold")
# ax5.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
# ax5.spines["top"].set_visible(False)
# ax5.spines["right"].set_visible(False)
#
# handles, labels = ax5.get_legend_handles_labels()
# legend_keep = ["Human", "Base", "Core", "PMA"]
# ordered_handles = [handles[labels.index(o)] for o in legend_keep]
# ordered_labels = legend_keep
# ax5.legend(
#     ordered_handles,
#     ordered_labels,
#     frameon=False,
#     fontsize=8.2,
#     loc="lower left",
#     handletextpad=0.5,
#     borderpad=0.2,
#     labelspacing=0.3
# )
#
# # =========================================================
# # Panel f: Summary of replication
# # Bubble matrix + mean replication score
# # =========================================================
# subgs_f = gs[1, 2].subgridspec(1, 2, width_ratios=[4.3, 1.45], wspace=0.16)
# ax6 = fig.add_subplot(subgs_f[0, 0])
# ax6b = fig.add_subplot(subgs_f[0, 1], sharey=ax6)
#
# # ---- Left: bubble matrix ----
# n_rows, n_cols = summary_matrix.shape
# ax6.set_xlim(-0.5, n_cols - 0.5)
# ax6.set_ylim(n_rows - 0.5, -0.5)
#
# for i in range(n_rows):
#     for j in range(n_cols):
#         rect = plt.Rectangle(
#             (j - 0.5, i - 0.5),
#             1,
#             1,
#             facecolor="#f7f7f7",
#             edgecolor="white",
#             linewidth=2
#         )
#         ax6.add_patch(rect)
#
# bubble_color = {
#     0: "#d9d9d9",
#     1: "#9ecae1",
#     2: "#3182bd"
# }
#
# bubble_size = {
#     0: 520,
#     1: 860,
#     2: 1230
# }
#
# for i in range(n_rows):
#     for j in range(n_cols):
#         val = int(summary_matrix[i, j])
#         ax6.scatter(
#             j,
#             i,
#             s=bubble_size[val],
#             color=bubble_color[val],
#             edgecolor="white",
#             linewidth=1.2,
#             zorder=3
#         )
#         ax6.text(
#             j,
#             i,
#             summary_label[val],
#             ha="center",
#             va="center",
#             fontsize=10.8,
#             fontweight="bold",
#             color="black" if val < 2 else "white",
#             zorder=4
#         )
#
# ax6.set_xticks(np.arange(n_cols))
# ax6.set_xticklabels(summary_experiments_short)
# ax6.set_yticks(np.arange(n_rows))
# ax6.set_yticklabels(models_short)
# ax6.set_title("f  Summary of replication", loc="left", fontweight="bold", pad=8)
# ax6.tick_params(axis="x", length=0)
# ax6.tick_params(axis="y", length=0)
#
# for spine in ax6.spines.values():
#     spine.set_visible(False)
#
# bubble_handles = [
#     Line2D(
#         [0], [0],
#         marker="o",
#         color="none",
#         markerfacecolor="#3182bd",
#         markeredgecolor="white",
#         markersize=10,
#         label="Strong"
#     ),
#     Line2D(
#         [0], [0],
#         marker="o",
#         color="none",
#         markerfacecolor="#9ecae1",
#         markeredgecolor="white",
#         markersize=9,
#         label="Partial"
#     ),
#     Line2D(
#         [0], [0],
#         marker="o",
#         color="none",
#         markerfacecolor="#d9d9d9",
#         markeredgecolor="white",
#         markersize=8,
#         label="Failed"
#     ),
# ]
#
# ax6.legend(
#     handles=bubble_handles,
#     frameon=False,
#     fontsize=8.4,
#     loc="upper center",
#     bbox_to_anchor=(0.5, -0.12),
#     ncol=3,
#     handletextpad=0.4,
#     columnspacing=1.0
# )
#
# # ---- Right: mean replication score ----
# y = np.arange(n_rows)
# bar_colors = ["#d9d9d9", "#b8d7e8", "#8cbdd8", "#9cc7df", "#4b94ca", "#3182bd"]
#
# ax6b.barh(
#     y,
#     overall_replication_score,
#     color=bar_colors,
#     edgecolor="none",
#     height=0.62
# )
#
# for i, v in enumerate(overall_replication_score):
#     ax6b.text(
#         v + 0.04,
#         i,
#         f"{v:.1f}",
#         va="center",
#         ha="left",
#         fontsize=8.5
#     )
#
# ax6b.set_xlim(0, 2.18)
# ax6b.set_xticks([0, 1, 2])
# ax6b.set_xlabel("Mean replication score")
# ax6b.set_title("Score", fontsize=9.2, pad=8)
# ax6b.tick_params(axis="y", left=False, labelleft=False)
# ax6b.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
# ax6b.spines["top"].set_visible(False)
# ax6b.spines["right"].set_visible(False)
# ax6b.spines["left"].set_visible(False)
#
# # =========================================================
# # Title
# # =========================================================
# fig.suptitle(
#     "Cross-paradigm behavioural replication by PMA and its ablated variants",
#     fontsize=15,
#     fontweight="bold",
#     y=0.985
# )
#
# plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.955])
# plt.show()
#
# # Optional save:
# # fig.savefig("Figure2_PMA_main_results_final.png", dpi=600, bbox_inches="tight")
# fig.savefig("outputs/Figure3.pdf", bbox_inches="tight")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# =========================================================
# Global style
# =========================================================
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "axes.titlesize": 11.5,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.linewidth": 0.9,
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
})

# =========================================================
# Model labels
# =========================================================
models_short = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]

model_colors = {
    "Human": "#222222",
    "Base": "#bdbdbd",
    "Affect": "#d9a66b",
    "Self": "#8c6bb1",
    "Sim": "#4aa6a6",
    "Core": "#3182bd",
    "PMA": "#c23b63",
}

# =========================================================
# Panel a: Learned helplessness
# =========================================================
lh_mae = {
    "Base": 14.33,
    "Affect": 5.17,
    "Self": 7.00,
    "Sim": 15.00,
    "Core": 4.17,
    "PMA": 3.00,
}

# =========================================================
# Panel b: Cognitive dissonance
# =========================================================
cd_dpi = {
    "Base":   [0.35, 0.45, 0.30, -0.35],
    "Affect": [0.10, 0.55, -0.10, 0.10],
    "Self":   [0.40, -0.35, -0.30, 0.10],
    "Sim":    [-0.15, 0.40, 0.45, 0.35],
    "Core":   [-0.30, 1.30, -0.40, 1.80],
    "PMA":    [2.95, 2.30, 3.00, 3.80],
}
cd_mean = {m: np.mean(vals) for m, vals in cd_dpi.items()}

measure_names = ["Enjoyment", "Learning", "Importance", "Intention"]
measure_markers = ["o", "s", "^", "D"]

# =========================================================
# Panel c: Foot-in-the-door
# =========================================================
fid_contrasts = {
    "Base": {
        "P  One-contact": 4.0,
        "P  Agree-only": -1.0,
        "P  Familiarization": -0.5,
    },
    "Affect": {
        "P  One-contact": 2.0,
        "P  Agree-only": 0.0,
        "P  Familiarization": 1.5,
    },
    "Self": {
        "P  One-contact": 28.0,
        "P  Agree-only": 0.0,
        "P  Familiarization": 17.0,
    },
    "Sim": {
        "P  One-contact": 25.5,
        "P  Agree-only": 5.0,
        "P  Familiarization": 9.5,
    },
    "Core": {
        "P  One-contact": 51.0,
        "P  Agree-only": 16.0,
        "P  Familiarization": 39.5,
    },
    "PMA": {
        "P  One-contact": 52.5,
        "P  Agree-only": 18.0,
        "P  Familiarization": 37.5,
    },
}

contrast_names = ["P  One-contact", "P  Agree-only", "P  Familiarization"]

contrast_colors = {
    "P  One-contact": "#5DA5DA",
    "P  Agree-only": "#60BD68",
    "P  Familiarization": "#F17C79",
}

contrast_markers = {
    "P  One-contact": "o",
    "P  Agree-only": "s",
    "P  Familiarization": "^",
}

# =========================================================
# Panel d: Social ostracism
# =========================================================
so_need_drop = {
    "Base": 0.10,
    "Affect": 0.38,
    "Self": 3.95,
    "Sim": 0.65,
    "Core": 3.20,
    "PMA": 4.03,
}
so_manip_drop = {
    "Base": -0.05,
    "Affect": 0.31,
    "Self": 3.20,
    "Sim": -0.07,
    "Core": 2.92,
    "PMA": 3.40,
}

# =========================================================
# Panel e: Diffusion of responsibility
# =========================================================
group_sizes = [1, 3, 6]
dor_rates = {
    "Human":  [85, 62, 31],
    "Base":   [100, 96, 100],
    "Affect": [92, 88, 88],
    "Self":   [92, 85, 77],
    "Sim":    [100, 62, 38],
    "Core":   [92, 69, 31],
    "PMA":    [90, 65, 28],
}

# =========================================================
# Panel f: Summary data
# 0 = Failed, 1 = Partial, 2 = Strong
# =========================================================
summary_experiments_short = ["LH", "CD", "FID", "SO", "DR"]
summary_matrix = np.array([
    [0, 0, 0, 0, 0],  # Base
    [1, 0, 0, 1, 0],  # Affect (CD treated as failed under strict peak criterion)
    [1, 1, 1, 2, 1],  # Self
    [0, 1, 1, 1, 1],  # Sim
    [2, 1, 2, 2, 2],  # Core
    [2, 2, 2, 2, 2],  # PMA
])
summary_label = {0: "F", 1: "P", 2: "S"}
overall_replication_score = summary_matrix.mean(axis=1)

# =========================================================
# Figure
# =========================================================
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.35)

# =========================================================
# Panel a: Learned helplessness
# =========================================================
ax1 = fig.add_subplot(gs[0, 0])

y = np.arange(len(models_short))
for i, m in enumerate(models_short):
    ax1.hlines(i, 0, lh_mae[m], color="#d0d0d0", linewidth=1.8, zorder=1)
    ax1.scatter(
        lh_mae[m], i,
        s=90,
        color=model_colors[m],
        edgecolor="white",
        linewidth=0.8,
        zorder=3
    )
    ax1.text(
        lh_mae[m] + 0.35,
        i,
        f"{lh_mae[m]:.2f}",
        va="center",
        ha="left",
        fontsize=9
    )

ax1.set_yticks(y)
ax1.set_yticklabels(models_short)
ax1.invert_yaxis()
ax1.set_xlim(0, 16.8)
ax1.set_xlabel("MAE to human pattern (lower is better)")
ax1.set_title("a  Learned helplessness", loc="left", fontweight="bold")
ax1.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.tick_params(axis="y", length=0)

# =========================================================
# Panel b: Cognitive dissonance
# =========================================================
ax2 = fig.add_subplot(gs[0, 1])

x = np.arange(len(models_short))
jitter = np.array([-0.18, -0.06, 0.06, 0.18])

for i, m in enumerate(models_short):
    vals = cd_dpi[m]

    for j, val in enumerate(vals):
        ax2.scatter(
            x[i] + jitter[j],
            val,
            s=58,
            marker=measure_markers[j],
            facecolor="white",
            edgecolor=model_colors[m],
            linewidth=1.3,
            zorder=3
        )

    ax2.scatter(
        x[i],
        cd_mean[m],
        s=98,
        marker="o",
        color=model_colors[m],
        edgecolor="black",
        linewidth=0.6,
        zorder=4
    )

    ax2.hlines(
        cd_mean[m],
        x[i] - 0.24,
        x[i] + 0.24,
        color="black",
        linewidth=1.0,
        zorder=4
    )

ax2.axhline(0, color="black", linewidth=0.9)
ax2.set_xticks(x)
ax2.set_xticklabels(models_short)
ax2.set_ylabel("Dissonance Peak Index")
ax2.set_title("b  Cognitive dissonance", loc="left", fontweight="bold")
ax2.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

measure_handles = [
    Line2D(
        [0], [0],
        marker=measure_markers[i],
        color="none",
        markerfacecolor="white",
        markeredgecolor="black",
        markersize=7,
        label=measure_names[i]
    )
    for i in range(4)
]

mean_handle = Line2D(
    [0], [0],
    marker="o",
    color="none",
    markerfacecolor="#555555",
    markeredgecolor="black",
    markersize=7,
    label="Mean"
)

ax2.legend(
    handles=measure_handles + [mean_handle],
    frameon=False,
    fontsize=8,
    loc="upper left",
    handletextpad=0.5,
    borderpad=0.2,
    labelspacing=0.35
)

# =========================================================
# Panel c: Foot-in-the-door
# =========================================================
ax3 = fig.add_subplot(gs[0, 2])

y_pos = np.arange(len(models_short))
contrast_offsets = {
    "P  One-contact": -0.18,
    "P  Agree-only": 0.00,
    "P  Familiarization": 0.18,
}

for cname in contrast_names:
    vals = [fid_contrasts[m][cname] for m in models_short]
    y_shifted = y_pos + contrast_offsets[cname]

    ax3.scatter(
        vals,
        y_shifted,
        s=88,
        marker=contrast_markers[cname],
        color=contrast_colors[cname],
        edgecolor="white",
        linewidth=0.7,
        alpha=0.95,
        label=cname,
        zorder=3
    )

ax3.axvline(0, color="black", linewidth=0.9)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(models_short)
ax3.invert_yaxis()
ax3.set_xlabel("Contrast in compliance rate (%)")
ax3.set_title("c  Foot-in-the-door", loc="left", fontweight="bold")
ax3.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_visible(False)
ax3.tick_params(axis="y", length=0)
ax3.legend(
    frameon=False,
    fontsize=8.5,
    loc="upper right",
    handletextpad=0.5,
    borderpad=0.2,
    labelspacing=0.3
)

# =========================================================
# Panel d: Social ostracism
# Dot plot
# =========================================================
ax4 = fig.add_subplot(gs[1, 0])

y = np.arange(len(models_short))

need_vals = np.array([so_need_drop[m] for m in models_short])
manip_vals = np.array([so_manip_drop[m] for m in models_short])

offset = 0.13

for i in range(len(models_short)):
    ax4.hlines(
        y=i - offset,
        xmin=0,
        xmax=need_vals[i],
        color="#3182bd",
        linewidth=2.0,
        alpha=0.55,
        zorder=1
    )
    ax4.hlines(
        y=i + offset,
        xmin=0,
        xmax=manip_vals[i],
        color="#9ecae1",
        linewidth=2.0,
        alpha=0.65,
        zorder=1
    )

ax4.scatter(
    need_vals,
    y - offset,
    s=72,
    color="#3182bd",
    edgecolor="white",
    linewidth=0.8,
    label="Need-threat drop",
    zorder=3
)

ax4.scatter(
    manip_vals,
    y + offset,
    s=72,
    color="#9ecae1",
    edgecolor="white",
    linewidth=0.8,
    label="Manipulation-check drop",
    zorder=3
)

ax4.axvline(0, color="black", linewidth=0.9)
ax4.set_yticks(y)
ax4.set_yticklabels(models_short)
ax4.invert_yaxis()
ax4.set_xlim(-0.35, 4.35)
ax4.set_xlabel("Drop score (Inclusion  Ostracism)")
ax4.set_title("d  Social ostracism", loc="left", fontweight="bold")
ax4.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["left"].set_visible(False)
ax4.tick_params(axis="y", length=0)
ax4.legend(
    frameon=False,
    fontsize=8.5,
    loc="upper right",
    handletextpad=0.5,
    borderpad=0.2,
    labelspacing=0.3
)

# =========================================================
# Panel e: Diffusion of responsibility
# =========================================================
ax5 = fig.add_subplot(gs[1, 1])

highlight_models = ["Human", "Base", "Core", "PMA"]

for name, vals in dor_rates.items():
    if name in highlight_models:
        lw = 2.6 if name in ["Human", "PMA"] else 2.2
        alpha = 1.0
        z = 4
        ms = 6.5
    else:
        lw = 1.3
        alpha = 0.45
        z = 2
        ms = 5.0

    ax5.plot(
        group_sizes,
        vals,
        marker="o",
        linewidth=lw,
        markersize=ms,
        color=model_colors[name],
        alpha=alpha,
        label=name,
        zorder=z
    )

ax5.set_xticks(group_sizes)
ax5.set_xlabel("Group size")
ax5.set_ylabel("Responsibility rate (%)")
ax5.set_ylim(0, 105)
ax5.set_title("e  Diffusion of responsibility", loc="left", fontweight="bold")
ax5.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)

handles, labels = ax5.get_legend_handles_labels()
legend_keep = ["Human", "Base", "Core", "PMA"]
ordered_handles = [handles[labels.index(o)] for o in legend_keep]
ordered_labels = legend_keep
ax5.legend(
    ordered_handles,
    ordered_labels,
    frameon=False,
    fontsize=8.2,
    loc="lower left",
    handletextpad=0.5,
    borderpad=0.2,
    labelspacing=0.3
)

# =========================================================
# Panel f: Summary of replication
# Bubble matrix + mean replication score
# =========================================================
subgs_f = gs[1, 2].subgridspec(1, 2, width_ratios=[4.3, 1.45], wspace=0.16)
ax6 = fig.add_subplot(subgs_f[0, 0])
ax6b = fig.add_subplot(subgs_f[0, 1], sharey=ax6)

# ---- Left: bubble matrix ----
n_rows, n_cols = summary_matrix.shape
ax6.set_xlim(-0.5, n_cols - 0.5)
ax6.set_ylim(n_rows - 0.5, -0.5)

for i in range(n_rows):
    for j in range(n_cols):
        rect = plt.Rectangle(
            (j - 0.5, i - 0.5),
            1,
            1,
            facecolor="#f7f7f7",
            edgecolor="white",
            linewidth=2
        )
        ax6.add_patch(rect)

bubble_color = {
    0: "#d9d9d9",
    1: "#9ecae1",
    2: "#3182bd"
}

bubble_size = {
    0: 520,
    1: 860,
    2: 1230
}

for i in range(n_rows):
    for j in range(n_cols):
        val = int(summary_matrix[i, j])
        ax6.scatter(
            j,
            i,
            s=bubble_size[val],
            color=bubble_color[val],
            edgecolor="white",
            linewidth=1.2,
            zorder=3
        )
        ax6.text(
            j,
            i,
            summary_label[val],
            ha="center",
            va="center",
            fontsize=10.8,
            fontweight="bold",
            color="black" if val < 2 else "white",
            zorder=4
        )

ax6.set_xticks(np.arange(n_cols))
ax6.set_xticklabels(summary_experiments_short)
ax6.set_yticks(np.arange(n_rows))
ax6.set_yticklabels(models_short)
ax6.set_title("f  Summary of replication", loc="left", fontweight="bold", pad=8)
ax6.tick_params(axis="x", length=0)
ax6.tick_params(axis="y", length=0)

for spine in ax6.spines.values():
    spine.set_visible(False)

bubble_handles = [
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor="#3182bd",
        markeredgecolor="white",
        markersize=10,
        label="Strong"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor="#9ecae1",
        markeredgecolor="white",
        markersize=9,
        label="Partial"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor="#d9d9d9",
        markeredgecolor="white",
        markersize=8,
        label="Failed"
    ),
]

ax6.legend(
    handles=bubble_handles,
    frameon=False,
    fontsize=8.4,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=3,
    handletextpad=0.4,
    columnspacing=1.0
)

# ---- Right: mean replication score ----
y = np.arange(n_rows)
bar_colors = ["#d9d9d9", "#b8d7e8", "#8cbdd8", "#9cc7df", "#4b94ca", "#3182bd"]

ax6b.barh(
    y,
    overall_replication_score,
    color=bar_colors,
    edgecolor="none",
    height=0.62
)

for i, v in enumerate(overall_replication_score):
    ax6b.text(
        v + 0.04,
        i,
        f"{v:.1f}",
        va="center",
        ha="left",
        fontsize=8.5
    )

ax6b.set_xlim(0, 2.18)
ax6b.set_xticks([0, 1, 2])
ax6b.set_xlabel("Mean replication score")
ax6b.set_title("Score", fontsize=9.2, pad=8)
ax6b.tick_params(axis="y", left=False, labelleft=False)
ax6b.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
ax6b.spines["top"].set_visible(False)
ax6b.spines["right"].set_visible(False)
ax6b.spines["left"].set_visible(False)

# =========================================================
# Title
# =========================================================
fig.suptitle(
    "Cross-paradigm behavioural replication by PMA and its ablated variants",
    fontsize=15,
    fontweight="bold",
    y=0.975
)

plt.tight_layout(rect=[0.02, 0.035, 0.98, 0.94])
plt.show()

# Optional save:
# fig.savefig("Figure2_PMA_main_results_final.png", dpi=600, bbox_inches="tight")
#fig.savefig("outputs/Figure3_revised.pdf", bbox_inches="tight", pad_inches=0.20)