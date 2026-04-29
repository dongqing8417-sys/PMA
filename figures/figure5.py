# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.lines import Line2D
# from matplotlib.colors import LinearSegmentedColormap
#
# # =========================================================
# # Global style
# # =========================================================
# mpl.rcParams.update({
#     "font.family": "DejaVu Sans",
#     "font.size": 9.0,
#     "axes.titlesize": 10.2,
#     "axes.labelsize": 9.5,
#     "xtick.labelsize": 8.4,
#     "ytick.labelsize": 8.4,
#     "legend.fontsize": 7.8,
#     "axes.linewidth": 1.0,
#     "pdf.fonttype": 42,
#     "ps.fonttype": 42,
# })
#
# # =========================================================
# # Colours
# # =========================================================
# model_colors = {
#     "Human":  "#222222",
#     "Base":   "#B7B7B7",
#     "Affect": "#D6A15D",
#     "Self":   "#8F73B8",
#     "Sim":    "#4CA9A7",
#     "Core":   "#3B84C0",
#     "PMA":    "#C9426E",
# }
#
# models_main = ["Human", "Base", "Core", "PMA"]
# models_all = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]
#
# # =========================================================
# # Data
# # =========================================================
#
# # Foot-in-the-door
# fid_conditions = ["Performance", "Agree-only", "Familiarization", "One-contact"]
#
# fid_rates = {
#     "Human": [52, 35, 25, 0],
#     "Base":  [6, 7, 6.5, 2],
#     "Core":  [57.5, 41.5, 18, 6.5],
#     "PMA":   [59, 39.5, 20, 5],
# }
#
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
# # Social ostracism
# so_need_profile = {
#     "Human": [5.0, 1.0],
#     "Base":  [4.5, 4.4],
#     "Core":  [5.0, 1.8],
#     "PMA":   [5.1, 1.1],
# }
#
# so_manip_profile = {
#     "Human": [5.0, 1.4],
#     "Base":  [4.2, 4.25],
#     "Core":  [4.9, 2.0],
#     "PMA":   [5.0, 1.6],
# }
#
# so_need_drop = {
#     "Base": 0.10,
#     "Affect": 0.38,
#     "Self": 3.95,
#     "Sim": 0.65,
#     "Core": 3.20,
#     "PMA": 4.03,
# }
#
# so_manip_drop = {
#     "Base": -0.05,
#     "Affect": 0.31,
#     "Self": 3.20,
#     "Sim": -0.07,
#     "Core": 2.92,
#     "PMA": 3.40,
# }
#
# # Diffusion of responsibility
# group_sizes = [1, 3, 6]
#
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
# human_dor = np.array(dor_rates["Human"])
#
# dor_slope = {}
# dor_mae = {}
#
# for m in models_all:
#     vals = np.array(dor_rates[m])
#     slope = np.polyfit(group_sizes, vals, 1)[0]
#     dor_slope[m] = -slope
#     dor_mae[m] = np.mean(np.abs(vals - human_dor))
#
# # =========================================================
# # Helper functions
# # =========================================================
# def style_axes(ax, grid_axis="y"):
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     if grid_axis is not None:
#         ax.grid(axis=grid_axis, linestyle="--", linewidth=0.65, alpha=0.32)
#     return ax
#
# def add_panel_label(ax, txt, x=-0.12, y=1.03):
#     ax.text(
#         x, y, txt,
#         transform=ax.transAxes,
#         ha="left", va="bottom",
#         fontsize=14,
#         fontweight="bold"
#     )
#
# # =========================================================
# # Canvas
# # =========================================================
# fig = plt.figure(figsize=(15.8, 9.1))
# gs = fig.add_gridspec(
#     2, 3,
#     width_ratios=[1.10, 1.00, 1.05],
#     height_ratios=[1.0, 1.0],
#     left=0.055, right=0.98, top=0.96, bottom=0.085,
#     wspace=0.40, hspace=0.42
# )
#
# # =========================================================
# # a. Foot-in-the-door compliance heatmap
# # representative models
# # =========================================================
# ax_a = fig.add_subplot(gs[0, 0])
#
# fid_matrix = np.array([fid_rates[m] for m in models_main])
# heat_cmap = LinearSegmentedColormap.from_list(
#     "fid_heat",
#     ["#F3F3F3", "#DCE9F5", "#8FB7DD", "#3B84C0", "#C9426E"]
# )
#
# im = ax_a.imshow(fid_matrix, aspect="auto", cmap=heat_cmap, vmin=0, vmax=75)
#
# ax_a.set_xticks(np.arange(len(fid_conditions)))
# ax_a.set_xticklabels(["Perf.", "Agree", "Fam.", "One"])
# ax_a.set_yticks(np.arange(len(models_main)))
# ax_a.set_yticklabels(models_main)
# ax_a.set_ylabel("Representative models")
# ax_a.set_title("Foot-in-the-door compliance", loc="left", fontweight="bold", pad=6)
#
# for i in range(fid_matrix.shape[0]):
#     for j in range(fid_matrix.shape[1]):
#         val = fid_matrix[i, j]
#         txt_color = "white" if val >= 45 else "black"
#         ax_a.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=8.5, color=txt_color)
#
# ax_a.add_patch(
#     plt.Rectangle(
#         (-0.5, -0.5),
#         1,
#         len(models_main),
#         fill=False,
#         ec="#666666",
#         lw=1.2
#     )
# )
#
# for s in ax_a.spines.values():
#     s.set_visible(False)
#
# ax_a.tick_params(length=0)
#
# for x in np.arange(-0.5, len(fid_conditions), 1):
#     ax_a.axvline(x, color="white", lw=1.4)
# for y in np.arange(-0.5, len(models_main), 1):
#     ax_a.axhline(y, color="white", lw=1.4)
#
# add_panel_label(ax_a, "a")
#
# # =========================================================
# # b. Foot-in-the-door contrasts
# # all variants
# # =========================================================
# ax_b = fig.add_subplot(gs[0, 1])
#
# contrast_names = ["P  One-contact", "P  Agree-only", "P  Familiarization"]
# contrast_colors = {
#     "P  One-contact": "#5B84B1",
#     "P  Agree-only": "#59A14F",
#     "P  Familiarization": "#E07A5F",
# }
# contrast_markers = {
#     "P  One-contact": "o",
#     "P  Agree-only": "s",
#     "P  Familiarization": "^",
# }
# offsets = {
#     "P  One-contact": -0.18,
#     "P  Agree-only": 0.0,
#     "P  Familiarization": 0.18,
# }
#
# y = np.arange(len(models_all))
#
# for c in contrast_names:
#     vals = [fid_contrasts[m][c] for m in models_all]
#     ys = y + offsets[c]
#
#     for i, v in enumerate(vals):
#         ax_b.hlines(
#             ys[i],
#             0,
#             v,
#             color=contrast_colors[c],
#             linewidth=1.6,
#             alpha=0.38,
#             zorder=1
#         )
#
#     ax_b.scatter(
#         vals,
#         ys,
#         s=64,
#         marker=contrast_markers[c],
#         color=contrast_colors[c],
#         edgecolor="white",
#         linewidth=0.8,
#         zorder=3,
#         label=c
#     )
#
# ax_b.axvline(0, color="black", lw=0.8)
# ax_b.set_yticks(y)
# ax_b.set_yticklabels(models_all)
# ax_b.invert_yaxis()
# ax_b.set_xlim(-5, 58)
# ax_b.set_xlabel("Compliance contrast (%)")
# ax_b.set_ylabel("All variants")
# ax_b.set_title("Foot-in-the-door contrasts", loc="left", fontweight="bold", pad=6)
# style_axes(ax_b, "x")
# ax_b.spines["left"].set_visible(False)
# ax_b.tick_params(axis="y", length=0)
# ax_b.legend(frameon=False, loc="upper right", fontsize=7.5, handlelength=1.1)
#
# add_panel_label(ax_b, "b")
#
# # =========================================================
# # c. Social ostracism dumbbell plots
# # representative models
# # =========================================================
# sub_c = gs[0, 2].subgridspec(1, 2, wspace=0.28)
# ax_c1 = fig.add_subplot(sub_c[0, 0])
# ax_c2 = fig.add_subplot(sub_c[0, 1], sharey=ax_c1)
#
# rows = np.arange(len(models_main))
# incl_color = "#4E79A7"
# ostr_color = "#E15759"
#
# def dumbbell(ax, prof, title):
#     for i, m in enumerate(models_main):
#         incl, ostr = prof[m]
#         ax.plot([ostr, incl], [i, i], color="#B8B8B8", lw=1.7, zorder=1)
#         ax.scatter(ostr, i, s=54, color=ostr_color, edgecolor="white", linewidth=0.8, zorder=3)
#         ax.scatter(incl, i, s=54, color=incl_color, edgecolor="white", linewidth=0.8, zorder=3)
#
#     ax.set_yticks(rows)
#     ax.set_yticklabels(models_main)
#     ax.invert_yaxis()
#     ax.set_xlim(0, 5.6)
#     ax.set_xlabel("Rating")
#     ax.set_title(title, loc="left", fontweight="bold", pad=6)
#     style_axes(ax, "x")
#     ax.spines["left"].set_visible(False)
#     ax.tick_params(axis="y", length=0)
#
# dumbbell(ax_c1, so_need_profile, "Need threat")
# dumbbell(ax_c2, so_manip_profile, "Manipulation check")
# ax_c1.set_ylabel("Representative models")
# ax_c2.tick_params(axis="y", labelleft=False)
#
# legend_handles = [
#     Line2D([0], [0], marker='o', color='none', markerfacecolor=incl_color,
#            markeredgecolor='white', markersize=7, label="Inclusion"),
#     Line2D([0], [0], marker='o', color='none', markerfacecolor=ostr_color,
#            markeredgecolor='white', markersize=7, label="Ostracism"),
# ]
#
# ax_c2.legend(handles=legend_handles, frameon=False, loc="upper right", fontsize=7.4)
#
# add_panel_label(ax_c1, "c", x=-0.28, y=1.03)
#
# # =========================================================
# # d. Social ostracism effect summary
# # all variants
# # =========================================================
# ax_d = fig.add_subplot(gs[1, 0])
#
# y = np.arange(len(models_all))
# h = 0.33
#
# need_vals = [so_need_drop[m] for m in models_all]
# manip_vals = [so_manip_drop[m] for m in models_all]
#
# ax_d.barh(
#     y - h/2,
#     need_vals,
#     height=h,
#     color="#4E79A7",
#     alpha=0.90,
#     label="Need-threat drop"
# )
# ax_d.barh(
#     y + h/2,
#     manip_vals,
#     height=h,
#     color="#9CC3E6",
#     alpha=0.95,
#     label="Manipulation-check drop"
# )
#
# ax_d.axvline(0, color="black", lw=0.8)
# ax_d.set_yticks(y)
# ax_d.set_yticklabels(models_all)
# ax_d.invert_yaxis()
# ax_d.set_xlabel("Drop score (Inclusion  Ostracism)")
# ax_d.set_ylabel("All variants")
# ax_d.set_title("Social ostracism effect summary", loc="left", fontweight="bold", pad=6)
# style_axes(ax_d, "x")
# ax_d.legend(frameon=False, loc="upper right", fontsize=7.5)
#
# add_panel_label(ax_d, "d")
#
# # =========================================================
# # e. Diffusion of responsibility profile
# # representative models
# # =========================================================
# ax_e = fig.add_subplot(gs[1, 1])
#
# for m in models_main:
#     vals = dor_rates[m]
#     ax_e.plot(
#         group_sizes,
#         vals,
#         marker="o",
#         markersize=4.6,
#         linewidth=2.2 if m in ["Human", "PMA"] else 1.8,
#         color=model_colors[m],
#         label=m
#     )
#
# ax_e.set_xticks(group_sizes)
# ax_e.set_xlabel("Group size")
# ax_e.set_ylabel("Responsibility rate (%)")
# ax_e.set_ylim(0, 105)
# ax_e.set_title("Diffusion of responsibility", loc="left", fontweight="bold", pad=6)
# style_axes(ax_e, "y")
# ax_e.legend(frameon=False, loc="upper right", fontsize=7.5)
#
# add_panel_label(ax_e, "e")
#
# # =========================================================
# # f. Diffusion summary
# # all variants
# # =========================================================
# sub_f = gs[1, 2].subgridspec(1, 2, wspace=0.28)
# ax_f1 = fig.add_subplot(sub_f[0, 0])
# ax_f2 = fig.add_subplot(sub_f[0, 1], sharey=ax_f1)
#
# y = np.arange(len(models_all))
#
# for i, m in enumerate(models_all):
#     v = dor_slope[m]
#     ax_f1.hlines(i, 0, v, color=model_colors[m], lw=1.7, alpha=0.38)
#     ax_f1.scatter(v, i, s=72, color=model_colors[m], edgecolor="white", linewidth=0.8, zorder=3)
#
# ax_f1.set_yticks(y)
# ax_f1.set_yticklabels(models_all)
# ax_f1.invert_yaxis()
# ax_f1.set_xlim(0, 15)
# ax_f1.set_xlabel("Decline slope")
# ax_f1.set_ylabel("All variants")
# ax_f1.set_title("Responsibility decline", loc="left", fontweight="bold", pad=6)
# style_axes(ax_f1, "x")
# ax_f1.spines["left"].set_visible(False)
# ax_f1.tick_params(axis="y", length=0)
#
# for i, m in enumerate(models_all):
#     v = dor_mae[m]
#     ax_f2.hlines(i, 0, v, color=model_colors[m], lw=1.7, alpha=0.38)
#     ax_f2.scatter(v, i, s=72, color=model_colors[m], edgecolor="white", linewidth=0.8, zorder=3)
#
# ax_f2.set_xlim(0, 42)
# ax_f2.set_xlabel("MAE to human")
# ax_f2.set_title("Human-alignment error", loc="left", fontweight="bold", pad=6)
# style_axes(ax_f2, "x")
# ax_f2.spines["left"].set_visible(False)
# ax_f2.tick_params(axis="y", labelleft=False, length=0)
#
# add_panel_label(ax_f1, "f", x=-0.28, y=1.03)
#
# plt.show()
#
# # Optional save:
# fig.savefig("outputs/Figure5.pdf", bbox_inches="tight")
# # fig.savefig("Figure4_redesigned_consistent_logic.png", dpi=400, bbox_inches="tight")


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap

# =========================================================
# Global style
# =========================================================
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.0,
    "axes.titlesize": 10.2,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.4,
    "ytick.labelsize": 8.4,
    "legend.fontsize": 7.8,
    "axes.linewidth": 1.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# =========================================================
# Colours
# =========================================================
model_colors = {
    "Human":  "#222222",
    "Base":   "#B7B7B7",
    "Affect": "#D6A15D",
    "Self":   "#8F73B8",
    "Sim":    "#4CA9A7",
    "Core":   "#3B84C0",
    "PMA":    "#C9426E",
}

models_main = ["Human", "Base", "Core", "PMA"]
models_all = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]

# =========================================================
# Data
# =========================================================

# Foot-in-the-door
fid_conditions = ["Performance", "Agree-only", "Familiarization", "One-contact"]

fid_rates = {
    "Human": [52, 35, 25, 0],
    "Base":  [6, 7, 6.5, 2],
    "Core":  [57.5, 41.5, 18, 6.5],
    "PMA":   [57.5, 39.5, 20, 5],
}

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

# Social ostracism
so_models_main = ["Base", "Core", "PMA"]

so_need_profile = {
    "Base":  [7.53, 7.42],
    "Core":  [7.45, 4.25],
    "PMA":   [7.58, 3.55],
}

so_manip_profile = {
    "Base":  [5.42, 5.48],
    "Core":  [5.60, 2.68],
    "PMA":   [5.71, 2.31],
}

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

# Diffusion of responsibility
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

human_dor = np.array(dor_rates["Human"])

dor_slope = {}
dor_mae = {}

for m in models_all:
    vals = np.array(dor_rates[m])
    slope = np.polyfit(group_sizes, vals, 1)[0]
    dor_slope[m] = -slope
    dor_mae[m] = np.mean(np.abs(vals - human_dor))

# =========================================================
# Helper functions
# =========================================================
def style_axes(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis is not None:
        ax.grid(axis=grid_axis, linestyle="--", linewidth=0.65, alpha=0.32)
    return ax

def add_panel_label(ax, txt, x=-0.12, y=1.03):
    ax.text(
        x, y, txt,
        transform=ax.transAxes,
        ha="left", va="bottom",
        fontsize=14,
        fontweight="bold"
    )

# =========================================================
# Canvas
# =========================================================
fig = plt.figure(figsize=(15.8, 9.1))
gs = fig.add_gridspec(
    2, 3,
    width_ratios=[1.10, 1.00, 1.05],
    height_ratios=[1.0, 1.0],
    left=0.055, right=0.98, top=0.96, bottom=0.085,
    wspace=0.40, hspace=0.42
)

# =========================================================
# a. Foot-in-the-door compliance heatmap
# representative models
# =========================================================
ax_a = fig.add_subplot(gs[0, 0])

fid_matrix = np.array([fid_rates[m] for m in models_main])
heat_cmap = LinearSegmentedColormap.from_list(
    "fid_heat",
    ["#F3F3F3", "#DCE9F5", "#8FB7DD", "#3B84C0", "#C9426E"]
)

im = ax_a.imshow(fid_matrix, aspect="auto", cmap=heat_cmap, vmin=0, vmax=75)

ax_a.set_xticks(np.arange(len(fid_conditions)))
ax_a.set_xticklabels(["Perf.", "Agree", "Fam.", "One"])
ax_a.set_yticks(np.arange(len(models_main)))
ax_a.set_yticklabels(models_main)
ax_a.set_ylabel("Representative models")
ax_a.set_title("Foot-in-the-door compliance", loc="left", fontweight="bold", pad=6)

for i in range(fid_matrix.shape[0]):
    for j in range(fid_matrix.shape[1]):
        val = fid_matrix[i, j]
        txt_color = "white" if val >= 45 else "black"
        ax_a.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=8.5, color=txt_color)

ax_a.add_patch(
    plt.Rectangle(
        (-0.5, -0.5),
        1,
        len(models_main),
        fill=False,
        ec="#666666",
        lw=1.2
    )
)

for s in ax_a.spines.values():
    s.set_visible(False)

ax_a.tick_params(length=0)

for x in np.arange(-0.5, len(fid_conditions), 1):
    ax_a.axvline(x, color="white", lw=1.4)
for y in np.arange(-0.5, len(models_main), 1):
    ax_a.axhline(y, color="white", lw=1.4)

add_panel_label(ax_a, "a")

# =========================================================
# b. Foot-in-the-door contrasts
# all variants
# =========================================================
ax_b = fig.add_subplot(gs[0, 1])

contrast_names = ["P  One-contact", "P  Agree-only", "P  Familiarization"]
contrast_colors = {
    "P  One-contact": "#5B84B1",
    "P  Agree-only": "#59A14F",
    "P  Familiarization": "#E07A5F",
}
contrast_markers = {
    "P  One-contact": "o",
    "P  Agree-only": "s",
    "P  Familiarization": "^",
}
offsets = {
    "P  One-contact": -0.18,
    "P  Agree-only": 0.0,
    "P  Familiarization": 0.18,
}

y = np.arange(len(models_all))

for c in contrast_names:
    vals = [fid_contrasts[m][c] for m in models_all]
    ys = y + offsets[c]

    for i, v in enumerate(vals):
        ax_b.hlines(
            ys[i],
            0,
            v,
            color=contrast_colors[c],
            linewidth=1.6,
            alpha=0.38,
            zorder=1
        )

    ax_b.scatter(
        vals,
        ys,
        s=64,
        marker=contrast_markers[c],
        color=contrast_colors[c],
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
        label=c
    )

ax_b.axvline(0, color="black", lw=0.8)
ax_b.set_yticks(y)
ax_b.set_yticklabels(models_all)
ax_b.invert_yaxis()
ax_b.set_xlim(-5, 58)
ax_b.set_xlabel("Compliance contrast (%)")
ax_b.set_ylabel("All variants")
ax_b.set_title("Foot-in-the-door contrasts", loc="left", fontweight="bold", pad=6)
style_axes(ax_b, "x")
ax_b.spines["left"].set_visible(False)
ax_b.tick_params(axis="y", length=0)
ax_b.legend(frameon=False, loc="upper right", fontsize=7.5, handlelength=1.1)

add_panel_label(ax_b, "b")

# =========================================================
# c. Social ostracism dumbbell plots
# representative models
# =========================================================
sub_c = gs[0, 2].subgridspec(1, 2, wspace=0.28)
ax_c1 = fig.add_subplot(sub_c[0, 0])
ax_c2 = fig.add_subplot(sub_c[0, 1], sharey=ax_c1)

rows = np.arange(len(so_models_main))
incl_color = "#4E79A7"
ostr_color = "#E15759"

def dumbbell(ax, prof, title):
    for i, m in enumerate(so_models_main):
        incl, ostr = prof[m]
        ax.plot([ostr, incl], [i, i], color="#B8B8B8", lw=1.7, zorder=1)
        ax.scatter(ostr, i, s=54, color=ostr_color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.scatter(incl, i, s=54, color=incl_color, edgecolor="white", linewidth=0.8, zorder=3)

    ax.set_yticks(rows)
    ax.set_yticklabels(so_models_main)
    ax.invert_yaxis()
    ax.set_xlim(0, 8.2)
    ax.set_xlabel("Rating")
    ax.set_title(title, loc="left", fontweight="bold", pad=6)
    style_axes(ax, "x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

dumbbell(ax_c1, so_need_profile, "Need threat")
dumbbell(ax_c2, so_manip_profile, "Manipulation check")
ax_c1.set_ylabel("Representative models")
ax_c2.tick_params(axis="y", labelleft=False)

legend_handles = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=incl_color,
           markeredgecolor='white', markersize=7, label="Inclusion"),
    Line2D([0], [0], marker='o', color='none', markerfacecolor=ostr_color,
           markeredgecolor='white', markersize=7, label="Ostracism"),
]

ax_c2.legend(handles=legend_handles, frameon=False, loc="upper right", fontsize=7.4)

add_panel_label(ax_c1, "c", x=-0.28, y=1.03)

# =========================================================
# d. Social ostracism effect summary
# all variants
# =========================================================
ax_d = fig.add_subplot(gs[1, 0])

y = np.arange(len(models_all))
h = 0.33

need_vals = [so_need_drop[m] for m in models_all]
manip_vals = [so_manip_drop[m] for m in models_all]

ax_d.barh(
    y - h/2,
    need_vals,
    height=h,
    color="#4E79A7",
    alpha=0.90,
    label="Need-threat drop"
)
ax_d.barh(
    y + h/2,
    manip_vals,
    height=h,
    color="#9CC3E6",
    alpha=0.95,
    label="Manipulation-check drop"
)

ax_d.axvline(0, color="black", lw=0.8)
ax_d.set_yticks(y)
ax_d.set_yticklabels(models_all)
ax_d.invert_yaxis()
ax_d.set_xlabel("Drop score (Inclusion  Ostracism)")
ax_d.set_ylabel("All variants")
ax_d.set_title("Social ostracism effect summary", loc="left", fontweight="bold", pad=6)
style_axes(ax_d, "x")
ax_d.legend(frameon=False, loc="upper right", fontsize=7.5)

add_panel_label(ax_d, "d")

# =========================================================
# e. Diffusion of responsibility profile
# representative models
# =========================================================
ax_e = fig.add_subplot(gs[1, 1])

for m in models_main:
    vals = dor_rates[m]
    ax_e.plot(
        group_sizes,
        vals,
        marker="o",
        markersize=4.6,
        linewidth=2.2 if m in ["Human", "PMA"] else 1.8,
        color=model_colors[m],
        label=m
    )

ax_e.set_xticks(group_sizes)
ax_e.set_xlabel("Group size")
ax_e.set_ylabel("Responsibility rate (%)")
ax_e.set_ylim(0, 105)
ax_e.set_title("Diffusion of responsibility", loc="left", fontweight="bold", pad=6)
style_axes(ax_e, "y")
ax_e.legend(frameon=False, loc="upper right", fontsize=7.5)

add_panel_label(ax_e, "e")

# =========================================================
# f. Diffusion summary
# all variants
# =========================================================
sub_f = gs[1, 2].subgridspec(1, 2, wspace=0.28)
ax_f1 = fig.add_subplot(sub_f[0, 0])
ax_f2 = fig.add_subplot(sub_f[0, 1], sharey=ax_f1)

y = np.arange(len(models_all))

for i, m in enumerate(models_all):
    v = dor_slope[m]
    ax_f1.hlines(i, 0, v, color=model_colors[m], lw=1.7, alpha=0.38)
    ax_f1.scatter(v, i, s=72, color=model_colors[m], edgecolor="white", linewidth=0.8, zorder=3)

ax_f1.set_yticks(y)
ax_f1.set_yticklabels(models_all)
ax_f1.invert_yaxis()
ax_f1.set_xlim(0, 15)
ax_f1.set_xlabel("Decline slope")
ax_f1.set_ylabel("All variants")
ax_f1.set_title("Responsibility decline", loc="left", fontweight="bold", pad=6)
style_axes(ax_f1, "x")
ax_f1.spines["left"].set_visible(False)
ax_f1.tick_params(axis="y", length=0)

for i, m in enumerate(models_all):
    v = dor_mae[m]
    ax_f2.hlines(i, 0, v, color=model_colors[m], lw=1.7, alpha=0.38)
    ax_f2.scatter(v, i, s=72, color=model_colors[m], edgecolor="white", linewidth=0.8, zorder=3)

ax_f2.set_xlim(0, 42)
ax_f2.set_xlabel("MAE to human")
ax_f2.set_title("Human-alignment error", loc="left", fontweight="bold", pad=6)
style_axes(ax_f2, "x")
ax_f2.spines["left"].set_visible(False)
ax_f2.tick_params(axis="y", labelleft=False, length=0)

add_panel_label(ax_f1, "f", x=-0.28, y=1.03)

plt.show()

# Optional save:
# fig.savefig("outputs/Figure5_revised.pdf", bbox_inches="tight", pad_inches=0.10)
# fig.savefig("Figure4_redesigned_consistent_logic.png", dpi=400, bbox_inches="tight")