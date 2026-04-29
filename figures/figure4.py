# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.lines import Line2D
#
# # =========================================================
# # Global style
# # =========================================================
# mpl.rcParams.update({
#     "font.family": "DejaVu Sans",
#     "font.size": 9.0,
#     "axes.titlesize": 10.0,
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
# blue_dark   = "#4E79A7"
# blue_light  = "#A6C8E5"
# green_dark  = "#59A14F"
# green_light = "#A8D99A"
#
# # =========================================================
# # Data
# # =========================================================
#
# # -------------------------
# # Learned helplessness
# # -------------------------
# lh_conditions = ["E", "NE", "NP"]
# lh_models_main = ["Human", "Base", "Core", "PMA"]
# models_all = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]
#
# lh_failure = {
#     "Human":  [50, 13, 11],
#     "Base":   [5, 13, 11],
#     "Affect": [55, 8, 7],
#     "Self":   [61, 5, 7],
#     "Sim":    [11, 4, 14],
#     "Core":   [53, 10, 6],
#     "PMA":    [56, 11, 6],
# }
#
# lh_avoidance = {
#     "Human":  [30, 8, 8],
#     "Base":   [0, 0, 5],
#     "Affect": [25, 0, 4],
#     "Self":   [20, 0, 7],
#     "Sim":    [0, 0, 14],
#     "Core":   [22, 3, 7],
#     "PMA":    [29, 6, 6],
# }
#
# lh_failure_se = {
#     "Human":  [0, 0, 0],
#     "Base":   [0.44, 0.64, 0.70],
#     "Affect": [1.05, 0.40, 0.38],
#     "Self":   [0.45, 0.47, 0.47],
#     "Sim":    [0.41, 0.31, 0.42],
#     "Core":   [0.65, 0.32, 0.31],
#     "PMA":    [0.70, 0.54, 0.48],
# }
#
# lh_avoidance_se = {
#     "Human":  [0, 0, 0],
#     "Base":   [0.00, 0.00, 0.30],
#     "Affect": [0.85, 0.00, 0.34],
#     "Self":   [0.46, 0.00, 0.24],
#     "Sim":    [0.00, 0.00, 0.47],
#     "Core":   [0.89, 0.26, 0.36],
#     "PMA":    [0.78, 0.56, 0.37],
# }
#
# human_failure = np.array(lh_failure["Human"])
# human_avoidance = np.array(lh_avoidance["Human"])
#
# failure_mae = {
#     m: np.mean(np.abs(np.array(lh_failure[m]) - human_failure))
#     for m in models_all
# }
#
# avoidance_mae = {
#     m: np.mean(np.abs(np.array(lh_avoidance[m]) - human_avoidance))
#     for m in models_all
# }
#
# # -------------------------
# # Attribution-sensitive avoidance
# # -------------------------
# attr_models = ["Human", "Base", "Core", "PMA"]
#
# attr_internal_external = {
#     "Human": [34, 18],
#     "Base":  [83, 78],
#     "Core":  [40, 17],
#     "PMA":   [43, 16],
# }
#
# attr_skill_chance = {
#     "Human": [34, 18],
#     "Base":  [72, 58],
#     "Core":  [38, 14],
#     "PMA":   [41, 13],
# }
#
# # -------------------------
# # Cognitive dissonance
# # -------------------------
# cd_conditions = ["Control", "$1", "$20"]
# cd_models_main = ["Human", "Base", "Core", "PMA"]
#
# cd_enjoyment = {
#     "Human":  [-0.5, 1.4, -0.1],
#     "Base":   [-4.3, -3.7, -3.8],
#     "Affect": [-3.6, -3.7, -4.0],
#     "Self":   [-3.9, -3.6, -4.1],
#     "Sim":    [-4.2, -4.1, -3.7],
#     "Core":   [-3.8, -3.4, -2.4],
#     "PMA":    [-3.5,  0.2, -2.0],
# }
#
# cd_learning = {
#     "Human":  [3.1, 2.8, 3.1],
#     "Base":   [0.7, 1.9, 2.2],
#     "Affect": [2.4, 2.6, 1.7],
#     "Self":   [2.2, 1.8, 2.1],
#     "Sim":    [2.4, 2.5, 1.8],
#     "Core":   [2.3, 4.0, 3.1],
#     "PMA":    [2.6, 5.3, 3.4],
# }
#
# cd_importance = {
#     "Human":  [5.6, 6.4, 5.2],
#     "Base":   [0.8, 1.9, 2.4],
#     "Affect": [3.2, 2.9, 2.8],
#     "Self":   [2.8, 2.3, 2.4],
#     "Sim":    [3.1, 3.0, 2.0],
#     "Core":   [3.2, 2.9, 3.4],
#     "PMA":    [3.5, 7.0, 4.5],
# }
#
# cd_intention = {
#     "Human":  [-0.6, 1.2, -0.2],
#     "Base":   [-3.6, -3.9, -3.5],
#     "Affect": [-4.1, -3.8, -3.7],
#     "Self":   [-4.0, -3.8, -3.8],
#     "Sim":    [-3.7, -3.2, -3.4],
#     "Core":   [-3.6, -1.5, -3.0],
#     "PMA":    [-3.2, 0.8, -2.8],
# }
#
# cd_mean_dpi = {
#     "Base": 0.19,
#     "Affect": 0.16,
#     "Self": 0.04,
#     "Sim": 0.26,
#     "Core": 0.60,
#     "PMA": 3.01,
# }
#
# cd_sig_peak_count = {
#     "Base": 0,
#     "Affect": 1,
#     "Self": 1,
#     "Sim": 0,
#     "Core": 2,
#     "PMA": 4,
# }
#
# cd_dpi = {
#     "Base":   [0.35, 0.45, 0.30, -0.35],
#     "Affect": [0.10, 0.55, -0.10, 0.10],
#     "Self":   [0.40, -0.35, -0.30, 0.10],
#     "Sim":    [-0.15, 0.40, 0.45, 0.35],
#     "Core":   [-0.30, 1.30, -0.40, 1.80],
#     "PMA":    [2.95, 2.30, 3.00, 3.80],
# }
#
# # =========================================================
# # Helpers
# # =========================================================
# def style_axes(ax, grid_axis="y"):
#     ax.spines["top"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     if grid_axis is not None:
#         ax.grid(axis=grid_axis, linestyle="--", linewidth=0.65, alpha=0.32)
#     return ax
#
# def add_panel_label(ax, txt, x=-0.16, y=1.08):
#     ax.text(
#         x, y, txt,
#         transform=ax.transAxes,
#         ha="left",
#         va="bottom",
#         fontsize=14,
#         fontweight="bold"
#     )
#
# def plot_cd_small(ax, data_dict, title, ylim, show_ylabel=False):
#     x = np.arange(len(cd_conditions))
#     ax.axvspan(0.85, 1.15, color="#E8E8E8", zorder=0)
#
#     for m in cd_models_main:
#         ax.plot(
#             x,
#             data_dict[m],
#             color=model_colors[m],
#             marker="o",
#             markersize=3.8,
#             linewidth=1.6,
#             label=m,
#             zorder=3
#         )
#
#     ax.set_xticks(x)
#     ax.set_xticklabels(cd_conditions)
#     ax.set_ylim(*ylim)
#     ax.set_title(title, pad=4, fontsize=9.0)
#
#     if show_ylabel:
#         ax.set_ylabel("Rating")
#
#     style_axes(ax, "y")
#
# # =========================================================
# # Canvas
# # =========================================================
# fig = plt.figure(figsize=(15.6, 8.4))
#
# outer = fig.add_gridspec(
#     2,
#     3,
#     width_ratios=[1.15, 1.10, 1.15],
#     height_ratios=[1.0, 1.0],
#     left=0.060,
#     right=0.975,
#     top=0.950,
#     bottom=0.080,
#     wspace=0.40,
#     hspace=0.44
# )
#
# # =========================================================
# # a. Learned helplessness profiles
# # =========================================================
# sub_a = outer[0, 0].subgridspec(1, 2, wspace=0.18)
# ax_a1 = fig.add_subplot(sub_a[0, 0])
# ax_a2 = fig.add_subplot(sub_a[0, 1])
#
# x = np.arange(len(lh_conditions))
# bar_w = 0.18
# offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * bar_w
#
# for i, m in enumerate(lh_models_main):
#     ax_a1.bar(
#         x + offsets[i],
#         lh_failure[m],
#         width=bar_w,
#         yerr=lh_failure_se[m],
#         capsize=2.0,
#         color=model_colors[m],
#         edgecolor="white",
#         linewidth=0.5,
#         zorder=3,
#         label=m
#     )
#
#     ax_a2.bar(
#         x + offsets[i],
#         lh_avoidance[m],
#         width=bar_w,
#         yerr=lh_avoidance_se[m],
#         capsize=2.0,
#         color=model_colors[m],
#         edgecolor="white",
#         linewidth=0.5,
#         zorder=3,
#         label=m
#     )
#
# ax_a1.set_xticks(x)
# ax_a1.set_xticklabels(lh_conditions)
# ax_a1.set_ylim(0, 70)
# ax_a1.set_ylabel("Failure rate (%)")
# ax_a1.set_title("Failure", pad=6, fontsize=9.5)
# style_axes(ax_a1, "y")
#
# ax_a2.set_xticks(x)
# ax_a2.set_xticklabels(lh_conditions)
# ax_a2.set_ylim(0, 35)
# ax_a2.set_title("Avoidance", pad=6, fontsize=9.5)
# ax_a2.tick_params(axis="y", labelleft=False)
# style_axes(ax_a2, "y")
#
# ax_a2.legend(
#     frameon=False,
#     loc="upper left",
#     bbox_to_anchor=(1.02, 1.00),
#     borderaxespad=0.0,
#     handlelength=1.0,
#     fontsize=7.6
# )
#
# add_panel_label(ax_a1, "a", x=-0.22, y=1.12)
#
# # =========================================================
# # b. Human-alignment landscape
# # =========================================================
# ax_b = fig.add_subplot(outer[0, 1])
#
# for k in range(0, 6):
#     xx = np.array([0, 18.5])
#     yy = -xx + (16 + 3.4 * k)
#     ax_b.fill_between(xx, yy, yy + 3.4, color="#BFBFBF", alpha=0.08, zorder=0)
#
# ax_b.scatter(0, 0, marker="*", s=190, color="#333333", zorder=5)
# ax_b.text(0.45, 0.18, "Human target", fontsize=8.2, color="#444444", clip_on=False)
#
# label_offsets_b = {
#     "Base":   (0.5, 0),
#     "Affect": (-1.1, 0.5),
#     "Self":   (-0.3, 0.5),
#     "Sim":    (-0.8, 0.6),
#     "Core":   (-1.1, 0.5),
#     "PMA":    (0.16, 0.5),
# }
#
# for m in models_all:
#     fx = failure_mae[m]
#     fy = avoidance_mae[m]
#
#     ax_b.scatter(
#         fx,
#         fy,
#         s=135,
#         color=model_colors[m],
#         edgecolor="white",
#         linewidth=1.0,
#         zorder=4
#     )
#
#     dx, dy = label_offsets_b[m]
#     ax_b.text(
#         fx + dx,
#         fy + dy,
#         m,
#         fontsize=9.0,
#         color="#333333",
#         clip_on=False
#     )
#
# ax_b.annotate(
#     "closer to human",
#     xy=(1.0, 1.0),
#     xytext=(7.4, 10.6),
#     arrowprops=dict(arrowstyle="->", lw=1.1, color="#555555"),
#     fontsize=9.0,
#     color="#555555"
# )
#
# ax_b.set_xlim(-0.5, 18.2)
# ax_b.set_ylim(-0.6, 16.3)
# ax_b.set_xlabel("Failure MAE")
# ax_b.set_ylabel("Avoidance MAE")
# ax_b.set_title("Human-alignment landscape", loc="left", fontweight="bold", fontsize=9.8)
# style_axes(ax_b, "both")
#
# add_panel_label(ax_b, "b", x=-0.12, y=1.05)
#
# # =========================================================
# # c. Attribution-sensitive avoidance
# # =========================================================
# sub_c = outer[0, 2].subgridspec(1, 2, wspace=0.22)
# ax_c1 = fig.add_subplot(sub_c[0, 0])
# ax_c2 = fig.add_subplot(sub_c[0, 1])
#
# xc = np.arange(len(attr_models))
# bw = 0.34
#
# vals_internal = [attr_internal_external[m][0] for m in attr_models]
# vals_external = [attr_internal_external[m][1] for m in attr_models]
#
# ax_c1.bar(
#     xc - bw/2,
#     vals_internal,
#     width=bw,
#     color=blue_dark,
#     edgecolor="white",
#     linewidth=0.5,
#     label="Internal",
#     zorder=3
# )
# ax_c1.bar(
#     xc + bw/2,
#     vals_external,
#     width=bw,
#     color=blue_light,
#     edgecolor="white",
#     linewidth=0.5,
#     label="External",
#     zorder=3
# )
#
# for xi, yv in zip(xc - bw/2, vals_internal):
#     ax_c1.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
# for xi, yv in zip(xc + bw/2, vals_external):
#     ax_c1.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
#
# ax_c1.set_xticks(xc)
# ax_c1.set_xticklabels(attr_models)
# ax_c1.set_ylim(0, 100)
# ax_c1.set_ylabel("Avoidance rate (%)")
# ax_c1.set_title("Internal vs External", pad=6, fontsize=9.5)
# ax_c1.legend(frameon=False, loc="upper left", handlelength=1.5, fontsize=7.6)
# style_axes(ax_c1, "y")
#
# vals_skill = [attr_skill_chance[m][0] for m in attr_models]
# vals_chance = [attr_skill_chance[m][1] for m in attr_models]
#
# ax_c2.bar(
#     xc - bw/2,
#     vals_skill,
#     width=bw,
#     color=green_dark,
#     edgecolor="white",
#     linewidth=0.5,
#     label="Skill-set",
#     zorder=3
# )
# ax_c2.bar(
#     xc + bw/2,
#     vals_chance,
#     width=bw,
#     color=green_light,
#     edgecolor="white",
#     linewidth=0.5,
#     label="Chance-set",
#     zorder=3
# )
#
# for xi, yv in zip(xc - bw/2, vals_skill):
#     ax_c2.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
# for xi, yv in zip(xc + bw/2, vals_chance):
#     ax_c2.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
#
# ax_c2.set_xticks(xc)
# ax_c2.set_xticklabels(attr_models)
# ax_c2.set_ylim(0, 100)
# ax_c2.tick_params(axis="y", labelleft=False)
# ax_c2.set_title("Skill-set vs Chance-set", pad=6, fontsize=9.5)
# ax_c2.legend(frameon=False, loc="upper left", handlelength=1.5, fontsize=7.6)
# style_axes(ax_c2, "y")
#
# add_panel_label(ax_c1, "c", x=-0.22, y=1.12)
#
# # =========================================================
# # d. Cognitive dissonance profiles
# # =========================================================
# sub_d = outer[1, 0].subgridspec(2, 2, wspace=0.24, hspace=0.48)
# ax_d1 = fig.add_subplot(sub_d[0, 0])
# ax_d2 = fig.add_subplot(sub_d[0, 1])
# ax_d3 = fig.add_subplot(sub_d[1, 0])
# ax_d4 = fig.add_subplot(sub_d[1, 1])
#
# plot_cd_small(ax_d1, cd_enjoyment, "Task enjoyment", (-4.8, 2.4), show_ylabel=True)
# plot_cd_small(ax_d2, cd_learning, "Learning gain", (0.0, 6.6))
# plot_cd_small(ax_d3, cd_importance, "Scientific importance", (0.0, 7.6), show_ylabel=True)
# plot_cd_small(ax_d4, cd_intention, "Participation intention", (-4.8, 2.4))
#
# ax_d2.tick_params(axis="y", labelleft=False)
# ax_d4.tick_params(axis="y", labelleft=False)
#
# legend_handles_d = [
#     Line2D(
#         [0], [0],
#         color=model_colors[m],
#         marker="o",
#         markersize=4.2,
#         linewidth=1.6,
#         label=m
#     )
#     for m in cd_models_main
# ]
#
# ax_d2.legend(
#     handles=legend_handles_d,
#     frameon=False,
#     loc="upper right",
#     bbox_to_anchor=(1.5, 1.06),
#     ncol=1,
#     fontsize=7.2,
#     columnspacing=0.7,
#     handlelength=1.3,
#     borderaxespad=0.1
# )
#
# add_panel_label(ax_d1, "d", x=-0.22, y=1.18)
#
# # =========================================================
# # e. One-dollar peak map
# # =========================================================
# ax_e = fig.add_subplot(outer[1, 1])
#
# ax_e.axhspan(3.5, 4.5, color="#F2E3EA", zorder=0)
# ax_e.axvspan(2.0, 3.35, color="#F2E3EA", alpha=0.60, zorder=0)
#
# for m in models_all:
#     ax_e.scatter(
#         cd_mean_dpi[m],
#         cd_sig_peak_count[m],
#         s=165 if m in ["PMA", "Core"] else 105,
#         color=model_colors[m],
#         edgecolor="white",
#         linewidth=1.0,
#         zorder=4
#     )
#
# label_offsets_e = {
#     "Base":   (-0.3, 0.15),
#     "Affect": (0.10,  0.18),
#     "Self":   (-0.10, 0.18),
#     "Sim":    (0.12, -0.02),
#     "Core":   (0.10,  0.16),
#     "PMA":    (-0.42, 0.10),
# }
#
# for m in models_all:
#     x0 = cd_mean_dpi[m]
#     y0 = cd_sig_peak_count[m]
#     dx, dy = label_offsets_e[m]
#
#     ax_e.annotate(
#         m,
#         xy=(x0, y0),
#         xytext=(x0 + dx, y0 + dy),
#         textcoords="data",
#         fontsize=8.4,
#         fontweight="bold" if m == "PMA" else "normal",
#         color="#222222",
#         arrowprops=dict(
#             arrowstyle="-",
#             lw=0.50,
#             color="#777777",
#             shrinkA=2,
#             shrinkB=2
#         ),
#         clip_on=False,
#         zorder=5
#     )
#
# ax_e.text(
#     1.9, 4.15,
#     "complete\none-dollar peak",
#     fontsize=8.0,
#     color="#8A4760",
#     ha="left",
#     va="top"
# )
#
# ax_e.set_xlim(-0.20, 3.35)
# ax_e.set_ylim(-0.20, 4.45)
# ax_e.set_xlabel("Mean DPI")
# ax_e.set_ylabel("Significant peak count")
# ax_e.set_yticks([0, 1, 2, 3, 4])
# ax_e.set_title("One-dollar peak map", loc="left", fontweight="bold", fontsize=9.8)
# style_axes(ax_e, "both")
#
# add_panel_label(ax_e, "e", x=-0.12, y=1.05)
#
# # =========================================================
# # f. DPI radial profile across measures
# # =========================================================
# ax_f = fig.add_subplot(outer[1, 2], projection="polar")
#
# measure_labels = ["Enjoy.", "Learn.", "Import.", "Intent."]
# angles = np.linspace(0, 2 * np.pi, len(measure_labels), endpoint=False)
# angles_closed = np.r_[angles, angles[0]]
#
# def close(vals):
#     vals = np.array(vals)
#     vals = np.clip(vals, 0, None)
#     return np.r_[vals, vals[0]]
#
# ax_f.set_theta_offset(np.pi / 2)
# ax_f.set_theta_direction(-1)
# ax_f.set_xticks(angles)
# ax_f.set_xticklabels(measure_labels)
# ax_f.set_ylim(0, 4.0)
# ax_f.set_yticks([1, 2, 3, 4])
# ax_f.set_yticklabels(["1", "2", "3", "4"], fontsize=7.6)
# ax_f.grid(True, linewidth=0.6, alpha=0.35)
#
# for m in models_all:
#     vals = close(cd_dpi[m])
#
#     if m == "PMA":
#         lw, alpha, z = 2.5, 0.92, 5
#         fill_alpha = 0.18
#     elif m == "Core":
#         lw, alpha, z = 2.1, 0.82, 4
#         fill_alpha = 0.12
#     elif m == "Base":
#         lw, alpha, z = 1.7, 0.65, 3
#         fill_alpha = 0.04
#     else:
#         lw, alpha, z = 1.1, 0.28, 2
#         fill_alpha = 0.00
#
#     ax_f.plot(
#         angles_closed,
#         vals,
#         color=model_colors[m],
#         linewidth=lw,
#         alpha=alpha,
#         label=m,
#         zorder=z
#     )
#
#     if fill_alpha > 0:
#         ax_f.fill(
#             angles_closed,
#             vals,
#             color=model_colors[m],
#             alpha=fill_alpha,
#             zorder=z - 1
#         )
#
# ax_f.set_title(
#     "DPI profile across measures",
#     loc="left",
#     fontweight="bold",
#     pad=18,
#     fontsize=9.8
# )
# ax_f.spines["polar"].set_visible(False)
#
# legend_handles = [
#     Line2D([0], [0], color=model_colors[m], linewidth=2.2, label=m)
#     for m in ["Base", "Core", "PMA"]
# ]
#
# ax_f.legend(
#     handles=legend_handles,
#     frameon=False,
#     fontsize=7.8,
#     loc="lower center",
#     bbox_to_anchor=(0.5, -0.24),
#     ncol=3,
#     handlelength=1.8,
#     columnspacing=1.0
# )
#
# add_panel_label(ax_f, "f", x=-0.10, y=1.08)
#
# # =========================================================
# # Show / save
# # =========================================================
# plt.show()
#
# # Optional save:
# # fig.savefig("Figure3_NMI_style_final.pdf", bbox_inches="tight")
# fig.savefig("outputs/Figure4.pdf", dpi=400, bbox_inches="tight")


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D

# =========================================================
# Global style
# =========================================================
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.0,
    "axes.titlesize": 10.0,
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

blue_dark   = "#4E79A7"
blue_light  = "#A6C8E5"
green_dark  = "#59A14F"
green_light = "#A8D99A"

# =========================================================
# Data
# =========================================================

# -------------------------
# Learned helplessness
# -------------------------
lh_conditions = ["E", "NE", "NP"]
lh_models_main = ["Human", "Base", "Core", "PMA"]
models_all = ["Base", "Affect", "Self", "Sim", "Core", "PMA"]

lh_failure = {
    "Human":  [50, 13, 11],
    "Base":   [5, 13, 11],
    "Affect": [55, 8, 7],
    "Self":   [61, 5, 7],
    "Sim":    [11, 4, 14],
    "Core":   [53, 10, 6],
    "PMA":    [56, 11, 6],
}

lh_avoidance = {
    "Human":  [30, 8, 8],
    "Base":   [0, 0, 5],
    "Affect": [25, 0, 4],
    "Self":   [20, 0, 7],
    "Sim":    [0, 0, 14],
    "Core":   [22, 3, 7],
    "PMA":    [29, 6, 6],
}

lh_failure_se = {
    "Human":  [0, 0, 0],
    "Base":   [0.44, 0.64, 0.70],
    "Affect": [1.05, 0.40, 0.38],
    "Self":   [0.45, 0.47, 0.47],
    "Sim":    [0.41, 0.31, 0.42],
    "Core":   [0.65, 0.32, 0.31],
    "PMA":    [0.70, 0.54, 0.48],
}

lh_avoidance_se = {
    "Human":  [0, 0, 0],
    "Base":   [0.00, 0.00, 0.30],
    "Affect": [0.85, 0.00, 0.34],
    "Self":   [0.46, 0.00, 0.24],
    "Sim":    [0.00, 0.00, 0.47],
    "Core":   [0.89, 0.26, 0.36],
    "PMA":    [0.78, 0.56, 0.37],
}

human_failure = np.array(lh_failure["Human"])
human_avoidance = np.array(lh_avoidance["Human"])

failure_mae = {
    m: np.mean(np.abs(np.array(lh_failure[m]) - human_failure))
    for m in models_all
}

avoidance_mae = {
    m: np.mean(np.abs(np.array(lh_avoidance[m]) - human_avoidance))
    for m in models_all
}

# -------------------------
# Attribution-sensitive avoidance
# -------------------------
attr_models = ["Human", "Base", "Core", "PMA"]

attr_internal_external = {
    "Human": [34, 18],
    "Base":  [83, 78],
    "Core":  [40, 17],
    "PMA":   [43, 16],
}

attr_skill_chance = {
    "Human": [34, 18],
    "Base":  [72, 58],
    "Core":  [38, 14],
    "PMA":   [41, 13],
}

# -------------------------
# Cognitive dissonance
# -------------------------
cd_conditions = ["Control", "$1", "$20"]
cd_models_main = ["Human", "Base", "Core", "PMA"]

cd_enjoyment = {
    "Human":  [-0.5, 1.4, -0.1],
    "Base":   [-4.3, -3.7, -3.8],
    "Affect": [-3.6, -3.7, -4.0],
    "Self":   [-3.9, -3.6, -4.1],
    "Sim":    [-4.2, -4.1, -3.7],
    "Core":   [-3.8, -3.4, -2.4],
    "PMA":    [-3.5,  0.2, -2.0],
}

cd_learning = {
    "Human":  [3.1, 2.8, 3.1],
    "Base":   [0.7, 1.9, 2.2],
    "Affect": [2.4, 2.6, 1.7],
    "Self":   [2.2, 1.8, 2.1],
    "Sim":    [2.4, 2.5, 1.8],
    "Core":   [2.3, 4.0, 3.1],
    "PMA":    [2.6, 5.3, 3.4],
}

cd_importance = {
    "Human":  [5.6, 6.4, 5.2],
    "Base":   [0.8, 1.9, 2.4],
    "Affect": [3.2, 2.9, 2.8],
    "Self":   [2.8, 2.3, 2.4],
    "Sim":    [3.1, 3.0, 2.0],
    "Core":   [3.2, 2.9, 3.4],
    "PMA":    [3.5, 7.0, 4.5],
}

cd_intention = {
    "Human":  [-0.6, 1.2, -0.2],
    "Base":   [-3.6, -3.9, -3.5],
    "Affect": [-4.1, -3.8, -3.7],
    "Self":   [-4.0, -3.8, -3.8],
    "Sim":    [-3.7, -3.2, -3.4],
    "Core":   [-3.6, -1.5, -3.0],
    "PMA":    [-3.2, 0.8, -2.8],
}

cd_mean_dpi = {
    "Base": 0.19,
    "Affect": 0.16,
    "Self": -0.04,
    "Sim": 0.26,
    "Core": 0.60,
    "PMA": 3.01,
}

cd_sig_peak_count = {
    "Base": 0,
    "Affect": 0,
    "Self": 1,
    "Sim": 0,
    "Core": 2,
    "PMA": 4,
}

cd_dpi = {
    "Base":   [0.35, 0.45, 0.30, -0.35],
    "Affect": [0.10, 0.55, -0.10, 0.10],
    "Self":   [0.40, -0.35, -0.30, 0.10],
    "Sim":    [-0.15, 0.40, 0.45, 0.35],
    "Core":   [-0.30, 1.30, -0.40, 1.80],
    "PMA":    [2.95, 2.30, 3.00, 3.80],
}

# =========================================================
# Helpers
# =========================================================
def style_axes(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis is not None:
        ax.grid(axis=grid_axis, linestyle="--", linewidth=0.65, alpha=0.32)
    return ax

def add_panel_label(ax, txt, x=-0.16, y=1.08):
    ax.text(
        x, y, txt,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=14,
        fontweight="bold"
    )

def plot_cd_small(ax, data_dict, title, ylim, show_ylabel=False):
    x = np.arange(len(cd_conditions))
    ax.axvspan(0.85, 1.15, color="#E8E8E8", zorder=0)

    for m in cd_models_main:
        ax.plot(
            x,
            data_dict[m],
            color=model_colors[m],
            marker="o",
            markersize=3.8,
            linewidth=1.6,
            label=m,
            zorder=3
        )

    ax.set_xticks(x)
    ax.set_xticklabels(cd_conditions)
    ax.set_ylim(*ylim)
    ax.set_title(title, pad=4, fontsize=9.0)

    if show_ylabel:
        ax.set_ylabel("Rating")

    style_axes(ax, "y")

# =========================================================
# Canvas
# =========================================================
fig = plt.figure(figsize=(15.6, 8.4))

outer = fig.add_gridspec(
    2,
    3,
    width_ratios=[1.15, 1.10, 1.15],
    height_ratios=[1.0, 1.0],
    left=0.060,
    right=0.975,
    top=0.950,
    bottom=0.080,
    wspace=0.40,
    hspace=0.44
)

# =========================================================
# a. Learned helplessness profiles
# =========================================================
sub_a = outer[0, 0].subgridspec(1, 2, wspace=0.18)
ax_a1 = fig.add_subplot(sub_a[0, 0])
ax_a2 = fig.add_subplot(sub_a[0, 1])

x = np.arange(len(lh_conditions))
bar_w = 0.18
offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * bar_w

for i, m in enumerate(lh_models_main):
    ax_a1.bar(
        x + offsets[i],
        lh_failure[m],
        width=bar_w,
        yerr=lh_failure_se[m],
        capsize=2.0,
        color=model_colors[m],
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
        label=m
    )

    ax_a2.bar(
        x + offsets[i],
        lh_avoidance[m],
        width=bar_w,
        yerr=lh_avoidance_se[m],
        capsize=2.0,
        color=model_colors[m],
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
        label=m
    )

ax_a1.set_xticks(x)
ax_a1.set_xticklabels(lh_conditions)
ax_a1.set_ylim(0, 70)
ax_a1.set_ylabel("Failure rate (%)")
ax_a1.set_title("Failure", pad=6, fontsize=9.5)
style_axes(ax_a1, "y")

ax_a2.set_xticks(x)
ax_a2.set_xticklabels(lh_conditions)
ax_a2.set_ylim(0, 35)
ax_a2.set_title("Avoidance", pad=6, fontsize=9.5)
ax_a2.tick_params(axis="y", labelleft=False)
style_axes(ax_a2, "y")

ax_a2.legend(
    frameon=False,
    loc="upper left",
    bbox_to_anchor=(1.02, 1.00),
    borderaxespad=0.0,
    handlelength=1.0,
    fontsize=7.6
)

add_panel_label(ax_a1, "a", x=-0.22, y=1.12)

# =========================================================
# b. Human-alignment landscape
# =========================================================
ax_b = fig.add_subplot(outer[0, 1])

for k in range(0, 6):
    xx = np.array([0, 18.5])
    yy = -xx + (16 + 3.4 * k)
    ax_b.fill_between(xx, yy, yy + 3.4, color="#BFBFBF", alpha=0.08, zorder=0)

ax_b.scatter(0, 0, marker="*", s=190, color="#333333", zorder=5)
ax_b.text(0.45, 0.18, "Human target", fontsize=8.2, color="#444444", clip_on=False)

label_offsets_b = {
    "Base":   (0.5, 0),
    "Affect": (-1.1, 0.5),
    "Self":   (-0.3, 0.5),
    "Sim":    (-0.8, 0.6),
    "Core":   (-1.1, 0.5),
    "PMA":    (0.16, 0.5),
}

for m in models_all:
    fx = failure_mae[m]
    fy = avoidance_mae[m]

    ax_b.scatter(
        fx,
        fy,
        s=135,
        color=model_colors[m],
        edgecolor="white",
        linewidth=1.0,
        zorder=4
    )

    dx, dy = label_offsets_b[m]
    ax_b.text(
        fx + dx,
        fy + dy,
        m,
        fontsize=9.0,
        color="#333333",
        clip_on=False
    )

ax_b.annotate(
    "closer to human",
    xy=(1.0, 1.0),
    xytext=(7.4, 10.6),
    arrowprops=dict(arrowstyle="->", lw=1.1, color="#555555"),
    fontsize=9.0,
    color="#555555"
)

ax_b.set_xlim(-0.5, 18.2)
ax_b.set_ylim(-0.6, 16.3)
ax_b.set_xlabel("Failure MAE")
ax_b.set_ylabel("Avoidance MAE")
ax_b.set_title("Human-alignment landscape", loc="left", fontweight="bold", fontsize=9.8)
style_axes(ax_b, "both")

add_panel_label(ax_b, "b", x=-0.12, y=1.05)

# =========================================================
# c. Attribution-sensitive avoidance
# =========================================================
sub_c = outer[0, 2].subgridspec(1, 2, wspace=0.22)
ax_c1 = fig.add_subplot(sub_c[0, 0])
ax_c2 = fig.add_subplot(sub_c[0, 1])

xc = np.arange(len(attr_models))
bw = 0.34

vals_internal = [attr_internal_external[m][0] for m in attr_models]
vals_external = [attr_internal_external[m][1] for m in attr_models]

ax_c1.bar(
    xc - bw/2,
    vals_internal,
    width=bw,
    color=blue_dark,
    edgecolor="white",
    linewidth=0.5,
    label="Internal",
    zorder=3
)
ax_c1.bar(
    xc + bw/2,
    vals_external,
    width=bw,
    color=blue_light,
    edgecolor="white",
    linewidth=0.5,
    label="External",
    zorder=3
)

for xi, yv in zip(xc - bw/2, vals_internal):
    ax_c1.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
for xi, yv in zip(xc + bw/2, vals_external):
    ax_c1.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)

ax_c1.set_xticks(xc)
ax_c1.set_xticklabels(attr_models)
ax_c1.set_ylim(0, 100)
ax_c1.set_ylabel("Avoidance rate (%)")
ax_c1.set_title("Internal vs External", pad=6, fontsize=9.5)
ax_c1.legend(frameon=False, loc="upper left", handlelength=1.5, fontsize=7.6)
style_axes(ax_c1, "y")

vals_skill = [attr_skill_chance[m][0] for m in attr_models]
vals_chance = [attr_skill_chance[m][1] for m in attr_models]

ax_c2.bar(
    xc - bw/2,
    vals_skill,
    width=bw,
    color=green_dark,
    edgecolor="white",
    linewidth=0.5,
    label="Skill-set",
    zorder=3
)
ax_c2.bar(
    xc + bw/2,
    vals_chance,
    width=bw,
    color=green_light,
    edgecolor="white",
    linewidth=0.5,
    label="Chance-set",
    zorder=3
)

for xi, yv in zip(xc - bw/2, vals_skill):
    ax_c2.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)
for xi, yv in zip(xc + bw/2, vals_chance):
    ax_c2.text(xi, yv + 2, str(yv), ha="center", va="bottom", fontsize=8.0)

ax_c2.set_xticks(xc)
ax_c2.set_xticklabels(attr_models)
ax_c2.set_ylim(0, 100)
ax_c2.tick_params(axis="y", labelleft=False)
ax_c2.set_title("Skill-set vs Chance-set", pad=6, fontsize=9.5)
ax_c2.legend(frameon=False, loc="upper left", handlelength=1.5, fontsize=7.6)
style_axes(ax_c2, "y")

add_panel_label(ax_c1, "c", x=-0.22, y=1.12)

# =========================================================
# d. Cognitive dissonance profiles
# =========================================================
sub_d = outer[1, 0].subgridspec(2, 2, wspace=0.24, hspace=0.48)
ax_d1 = fig.add_subplot(sub_d[0, 0])
ax_d2 = fig.add_subplot(sub_d[0, 1])
ax_d3 = fig.add_subplot(sub_d[1, 0])
ax_d4 = fig.add_subplot(sub_d[1, 1])

plot_cd_small(ax_d1, cd_enjoyment, "Task enjoyment", (-4.8, 2.4), show_ylabel=True)
plot_cd_small(ax_d2, cd_learning, "Learning gain", (0.0, 6.6))
plot_cd_small(ax_d3, cd_importance, "Scientific importance", (0.0, 7.6), show_ylabel=True)
plot_cd_small(ax_d4, cd_intention, "Participation intention", (-4.8, 2.4))

ax_d2.tick_params(axis="y", labelleft=False)
ax_d4.tick_params(axis="y", labelleft=False)

legend_handles_d = [
    Line2D(
        [0], [0],
        color=model_colors[m],
        marker="o",
        markersize=4.2,
        linewidth=1.6,
        label=m
    )
    for m in cd_models_main
]

ax_d2.legend(
    handles=legend_handles_d,
    frameon=False,
    loc="upper right",
    bbox_to_anchor=(1.5, 1.06),
    ncol=1,
    fontsize=7.2,
    columnspacing=0.7,
    handlelength=1.3,
    borderaxespad=0.1
)

add_panel_label(ax_d1, "d", x=-0.22, y=1.18)

# =========================================================
# e. One-dollar peak map
# =========================================================
ax_e = fig.add_subplot(outer[1, 1])

ax_e.axhspan(3.5, 4.5, color="#F2E3EA", zorder=0)
ax_e.axvspan(2.0, 3.35, color="#F2E3EA", alpha=0.60, zorder=0)

for m in models_all:
    ax_e.scatter(
        cd_mean_dpi[m],
        cd_sig_peak_count[m],
        s=165 if m in ["PMA", "Core"] else 105,
        color=model_colors[m],
        edgecolor="white",
        linewidth=1.0,
        zorder=4
    )

label_offsets_e = {
    "Base":   (-0.3, 0.15),
    "Affect": (0.10,  0.18),
    "Self":   (-0.10, 0.18),
    "Sim":    (0.12, -0.02),
    "Core":   (0.10,  0.16),
    "PMA":    (-0.42, 0.10),
}

for m in models_all:
    x0 = cd_mean_dpi[m]
    y0 = cd_sig_peak_count[m]
    dx, dy = label_offsets_e[m]

    ax_e.annotate(
        m,
        xy=(x0, y0),
        xytext=(x0 + dx, y0 + dy),
        textcoords="data",
        fontsize=8.4,
        fontweight="bold" if m == "PMA" else "normal",
        color="#222222",
        arrowprops=dict(
            arrowstyle="-",
            lw=0.50,
            color="#777777",
            shrinkA=2,
            shrinkB=2
        ),
        clip_on=False,
        zorder=5
    )

ax_e.text(
    1.9, 4.15,
    "complete\none-dollar peak",
    fontsize=8.0,
    color="#8A4760",
    ha="left",
    va="top"
)

ax_e.set_xlim(-0.20, 3.35)
ax_e.set_ylim(-0.20, 4.45)
ax_e.set_xlabel("Mean DPI")
ax_e.set_ylabel("Significant peak count")
ax_e.set_yticks([0, 1, 2, 3, 4])
ax_e.set_title("One-dollar peak map", loc="left", fontweight="bold", fontsize=9.8)
style_axes(ax_e, "both")

add_panel_label(ax_e, "e", x=-0.12, y=1.05)

# =========================================================
# f. DPI radial profile across measures
# =========================================================
ax_f = fig.add_subplot(outer[1, 2], projection="polar")

measure_labels = ["Enjoy.", "Learn.", "Import.", "Intent."]
angles = np.linspace(0, 2 * np.pi, len(measure_labels), endpoint=False)
angles_closed = np.r_[angles, angles[0]]

def close(vals):
    vals = np.array(vals)
    vals = np.clip(vals, 0, None)
    return np.r_[vals, vals[0]]

ax_f.set_theta_offset(np.pi / 2)
ax_f.set_theta_direction(-1)
ax_f.set_xticks(angles)
ax_f.set_xticklabels(measure_labels)
ax_f.set_ylim(0, 4.0)
ax_f.set_yticks([1, 2, 3, 4])
ax_f.set_yticklabels(["1", "2", "3", "4"], fontsize=7.6)
ax_f.grid(True, linewidth=0.6, alpha=0.35)

for m in models_all:
    vals = close(cd_dpi[m])

    if m == "PMA":
        lw, alpha, z = 2.5, 0.92, 5
        fill_alpha = 0.18
    elif m == "Core":
        lw, alpha, z = 2.1, 0.82, 4
        fill_alpha = 0.12
    elif m == "Base":
        lw, alpha, z = 1.7, 0.65, 3
        fill_alpha = 0.04
    else:
        lw, alpha, z = 1.1, 0.28, 2
        fill_alpha = 0.00

    ax_f.plot(
        angles_closed,
        vals,
        color=model_colors[m],
        linewidth=lw,
        alpha=alpha,
        label=m,
        zorder=z
    )

    if fill_alpha > 0:
        ax_f.fill(
            angles_closed,
            vals,
            color=model_colors[m],
            alpha=fill_alpha,
            zorder=z - 1
        )

ax_f.set_title(
    "DPI profile across measures",
    loc="left",
    fontweight="bold",
    pad=18,
    fontsize=9.8
)
ax_f.spines["polar"].set_visible(False)

legend_handles = [
    Line2D([0], [0], color=model_colors[m], linewidth=2.2, label=m)
    for m in ["Base", "Core", "PMA"]
]

ax_f.legend(
    handles=legend_handles,
    frameon=False,
    fontsize=7.8,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.24),
    ncol=3,
    handlelength=1.8,
    columnspacing=1.0
)

add_panel_label(ax_f, "f", x=-0.10, y=1.08)

# =========================================================
# Show / save
# =========================================================
plt.show()

# Optional save:
# fig.savefig("Figure3_NMI_style_final.pdf", bbox_inches="tight")
# fig.savefig("outputs/Figure4_revised.pdf", dpi=400, bbox_inches="tight", pad_inches=0.10)