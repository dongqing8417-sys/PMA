# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
# from matplotlib.patches import Rectangle
# from matplotlib.lines import Line2D
# from matplotlib.colors import LinearSegmentedColormap
#
# # =========================================================
# # Basic style
# # =========================================================
# plt.rcParams.update({
#     "font.family": "DejaVu Sans",
#     "font.size": 10,
#     "axes.spines.top": False,
#     "axes.spines.right": False,
#     "axes.linewidth": 1.0,
#     "axes.labelsize": 10.5,
#     "axes.titlesize": 11.5,
#     "xtick.labelsize": 9,
#     "ytick.labelsize": 9,
#     "legend.fontsize": 8,
#     "figure.facecolor": "white",
#     "savefig.facecolor": "white",
#     "pdf.fonttype": 42,
#     "ps.fonttype": 42,
# })
#
# # =========================================================
# # Model names and colours
# # =========================================================
# model_order_all = [
#     "Base-Agent", "PMA-Affect", "PMA-Sim",
#     "PMA-Self", "PMA-Mind", "PMA-Core", "PMA"
# ]
#
# model_order_traj = [
#     "Base-Agent", "PMA-Sim", "PMA-Self",
#     "PMA-Mind", "PMA-Core", "PMA"
# ]
#
# model_short = {
#     "Base-Agent": "Base",
#     "PMA-Affect": "Affect",
#     "PMA-Sim": "Sim",
#     "PMA-Self": "Self",
#     "PMA-Mind": "Mind",
#     "PMA-Core": "Core",
#     "PMA": "PMA",
# }
#
# model_colors = {
#     "Base-Agent": "#B8B8B8",
#     "PMA-Affect": "#D8A15B",
#     "PMA-Sim": "#4FA7A6",
#     "PMA-Self": "#8E72B5",
#     "PMA-Mind": "#7FAE6B",
#     "PMA-Core": "#3B84C3",
#     "PMA": "#CC466E",
# }
#
# # =========================================================
# # Low-saturation functional colours
# # =========================================================
# # func_colors = {
# #     "Execution":   "#cee1a6",
# #     "Social":      "#e7f1d3",
# #     "Recovery":    "#f0a59f",
# #     "Feedback":    "#f8dc99",
# #     "Exploration": "#d0eae5",
# #     "Planning":    "#92d0c3",
# # }
#
# # func_colors = {
# #     "Execution":   "#e1d7e8",
# #     "Social":      "#f2e1ba",
# #     "Recovery":    "#c0d4eb",
# #     "Feedback":    "#c4d8c5",
# #     "Exploration": "#dfecf5",
# #     "Planning":    "#e9f1e8",
# # }
#
# func_colors = {
#     "Execution":   "#94cbc1",
#     "Social":      "#cce6e2",
#     "Recovery":    "#f6e2b7",
#     "Feedback":    "#c6aacc",
#     "Exploration": "#e2d6e7",
#     "Planning":    "#efbdb8",
# }
#
# # =========================================================
# # Latest rating data
# # mean, SE, SD across raters
# # =========================================================
# rating_data = {
#     "Base-Agent": {
#         "Emotion": (3.6444, 0.1461, 0.4620),
#         "Identity": (3.4607, 0.0369, 0.1168),
#         "Diversity": (4.1705, 0.0352, 0.1112),
#         "Plausibility": (4.9098, 0.0125, 0.0396),
#     },
#     "PMA-Affect": {
#         "Emotion": (4.3556, 0.0873, 0.2762),
#         "Identity": (3.6705, 0.0512, 0.1620),
#         "Diversity": (3.9000, 0.0504, 0.1594),
#         "Plausibility": (4.3705, 0.0322, 0.1017),
#     },
#     "PMA-Sim": {
#         "Emotion": (3.8222, 0.1150, 0.3636),
#         "Identity": (3.3295, 0.0557, 0.1761),
#         "Diversity": (3.5902, 0.0671, 0.2121),
#         "Plausibility": (4.4197, 0.0373, 0.1180),
#     },
#     "PMA-Self": {
#         "Emotion": (3.7000, 0.1315, 0.4159),
#         "Identity": (4.8295, 0.0143, 0.0452),
#         "Diversity": (3.5902, 0.0534, 0.1688),
#         "Plausibility": (4.4803, 0.0329, 0.1040),
#     },
#     "PMA-Mind": {
#         "Emotion": (3.7778, 0.0497, 0.1571),
#         "Identity": (3.5000, 0.0548, 0.1732),
#         "Diversity": (4.4607, 0.0436, 0.1379),
#         "Plausibility": (4.2705, 0.0500, 0.1582),
#     },
#     "PMA-Core": {
#         "Emotion": (4.4111, 0.0742, 0.2345),
#         "Identity": (4.8295, 0.0275, 0.0868),
#         "Diversity": (4.3197, 0.0482, 0.1525),
#         "Plausibility": (4.5705, 0.0315, 0.0995),
#     },
#     "PMA": {
#         "Emotion": (4.5556, 0.0845, 0.2671),
#         "Identity": (4.8500, 0.0200, 0.0633),
#         "Diversity": (3.5300, 0.0657, 0.2077),
#         "Plausibility": (4.7800, 0.0153, 0.0483),
#     },
# }
#
# metric_order = ["Emotion", "Identity", "Diversity", "Plausibility"]
# metric_long = {
#     "Emotion": "Emotional\nnaturalness",
#     "Identity": "Identity\nconsistency",
#     "Diversity": "Behavioural\ndiversity",
#     "Plausibility": "Behavioural\nplausibility",
# }
# metric_short = {
#     "Emotion": "Emotion",
#     "Identity": "Identity",
#     "Diversity": "Diversity",
#     "Plausibility": "Plausibility",
# }
#
# def get_mean(model, metric):
#     return rating_data[model][metric][0]
#
# def get_se(model, metric):
#     return rating_data[model][metric][1]
#
# def get_sd(model, metric):
#     return rating_data[model][metric][2]
#
# # =========================================================
# # ICC from framework-ratermean method
# # 
# # =========================================================
# icc_data = {
#     "Emotion": {
#         "ICC2_1_absolute_single": 0.567944,
#         "ICC2_k_absolute_average": 0.929304,
#     },
#     "Identity": {
#         "ICC2_1_absolute_single": 0.969870,
#         "ICC2_k_absolute_average": 0.996903,
#     },
#     "Diversity": {
#         "ICC2_1_absolute_single": 0.838524,
#         "ICC2_k_absolute_average": 0.981107,
#     },
#     "Plausibility": {
#         "ICC2_1_absolute_single": 0.829862,
#         "ICC2_k_absolute_average": 0.979910,
#     },
# }
#
# # =========================================================
# # Rater-level data
# # Each point in panel d is one rater's mean score
# # =========================================================
# rater_level = {
#     "Base-Agent": {
#         "Emotion": [3.3333, 2.5556, 3.3333, 3.6667, 3.8889, 4.0000, 3.7778, 3.8889, 3.8889, 4.1111],
#         "Identity": [3.2295, 3.3607, 3.4426, 3.5574, 3.5738, 3.4754, 3.3443, 3.5574, 3.5738, 3.4918],
#         "Diversity": [4.0492, 4.0656, 4.0820, 4.1967, 4.1967, 4.1967, 4.2131, 4.3279, 4.3443, 4.0328],
#         "Plausibility": [4.8852, 4.9836, 4.9344, 4.9180, 4.8852, 4.9180, 4.9508, 4.8689, 4.8525, 4.9016],
#     },
#     "PMA-Core": {
#         "Emotion": [4.4444, 4.3333, 4.0000, 4.5556, 4.4444, 4.0000, 4.5556, 4.6667, 4.5556, 4.5556],
#         "Identity": [4.8197, 4.9508, 4.9344, 4.9016, 4.8852, 4.7869, 4.8361, 4.7377, 4.7213, 4.7213],
#         "Diversity": [4.1803, 4.3443, 4.2787, 4.2623, 4.0984, 4.4426, 4.2623, 4.2951, 4.6557, 4.3770],
#         "Plausibility": [4.4426, 4.5574, 4.6066, 4.7049, 4.5246, 4.4426, 4.5574, 4.6230, 4.7377, 4.5082],
#     },
#     "PMA": {
#         "Emotion": [4.7778, 4.4444, 4.4444, 4.5556, 4.7778, 4.5556, 4.4444, 4.5556, 4.0000, 5.0000],
#         "Identity": [4.8000, 4.8000, 4.8167, 4.8833, 4.9000, 4.8167, 4.9167, 4.8333, 4.9667, 4.7667],
#         "Diversity": [3.5500, 3.2833, 3.4167, 3.4833, 3.2333, 3.8667, 3.6000, 3.8167, 3.6333, 3.4167],
#         "Plausibility": [4.7833, 4.7833, 4.8000, 4.7167, 4.8833, 4.7500, 4.7167, 4.8000, 4.8000, 4.7667],
#     },
# }
#
# # =========================================================
# # Functional composition
# # =========================================================
# functional_composition = {
#     "Base-Agent": {"Execution": 42.6, "Social": 26.2, "Recovery": 13.1, "Feedback": 13.1, "Exploration": 1.6, "Planning": 3.3},
#     "PMA-Sim": {"Execution": 34.4, "Social": 24.6, "Recovery": 21.3, "Feedback": 9.8, "Exploration": 4.9, "Planning": 4.9},
#     "PMA-Self": {"Execution": 44.3, "Social": 23.0, "Recovery": 9.8, "Feedback": 6.6, "Exploration": 16.4, "Planning": 0.0},
#     "PMA-Mind": {"Execution": 42.6, "Social": 9.8, "Recovery": 21.3, "Feedback": 4.9, "Exploration": 18.0, "Planning": 3.3},
#     "PMA-Core": {"Execution": 55.7, "Social": 11.5, "Recovery": 13.1, "Feedback": 9.8, "Exploration": 3.3, "Planning": 6.6},
#     "PMA": {"Execution": 32.8, "Social": 9.8, "Recovery": 19.7, "Feedback": 11.5, "Exploration": 0.0, "Planning": 26.2},
# }
#
# # =========================================================
# # Compact daily trajectory blocks
# # =========================================================
# time_blocks = [
#     "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
#     "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
#     "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
#     "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
#     "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"
# ]
#
# # trajectory_blocks = {
# #     "Base-Agent": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Execution", "Execution", "Execution", "Execution", "Recovery", "Recovery",
# #         "Execution", "Social", "Social", "Social", "Social", "Social",
# #         "Execution", "Execution", "Execution", "Execution", "Feedback", "Feedback",
# #         "Feedback", "Social", "Feedback", "Exploration", "Execution", "Execution"
# #     ],
# #     "PMA-Sim": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Social", "Recovery", "Execution", "Planning", "Recovery", "Execution",
# #         "Execution", "Exploration", "Planning", "Social", "Social", "Social",
# #         "Social", "Execution", "Execution", "Social", "Recovery", "Execution",
# #         "Feedback", "Feedback", "Execution", "Execution", "Execution", "Recovery"
# #     ],
# #     "PMA-Self": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Social", "Social", "Social", "Social", "Execution", "Social",
# #         "Execution", "Execution", "Execution", "Execution", "Exploration", "Execution",
# #         "Execution", "Execution", "Execution", "Execution", "Social", "Recovery",
# #         "Social", "Social", "Execution", "Execution", "Feedback", "Feedback"
# #     ],
# #     "PMA-Mind": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Execution", "Execution", "Execution", "Social", "Social", "Planning",
# #         "Recovery", "Recovery", "Exploration", "Exploration", "Exploration", "Exploration",
# #         "Recovery", "Feedback", "Social", "Feedback", "Execution", "Recovery",
# #         "Execution", "Execution", "Execution", "Exploration", "Exploration", "Execution"
# #     ],
# #     "PMA-Core": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Social", "Execution", "Feedback", "Recovery", "Recovery", "Social",
# #         "Execution", "Execution", "Exploration", "Social", "Execution", "Execution",
# #         "Execution", "Execution", "Execution", "Execution", "Recovery", "Social",
# #         "Feedback", "Feedback", "Execution", "Execution", "Planning", "Execution"
# #     ],
# #     "PMA": [
# #         "Execution", "Execution", "Execution", "Execution", "Execution", "Execution",
# #         "Feedback", "Execution", "Planning", "Planning", "Execution", "Planning",
# #         "Social", "Recovery", "Execution", "Feedback", "Planning", "Planning",
# #         "Planning", "Execution", "Planning", "Feedback", "Execution", "Feedback",
# #         "Feedback", "Planning", "Execution", "Execution", "Recovery", "Recovery"
# #     ],
# # }
#
# trajectory_blocks = {
#     "Base-Agent": [
#         "Execution", "Recovery", "Execution", "Execution", "Social", "Social",
#         "Execution", "Execution", "Execution", "Execution", "Recovery", "Recovery",
#         "Execution", "Social", "Social", "Social", "Social", "Social",
#         "Execution", "Execution", "Execution", "Execution", "Feedback", "Feedback",
#         "Feedback", "Social", "Feedback", "Exploration", "Execution", "Execution"
#     ],
#     "PMA-Sim": [
#         "Execution", "Recovery", "Recovery", "Exploration", "Execution", "Social",
#         "Social", "Recovery", "Execution", "Planning", "Recovery", "Execution",
#         "Execution", "Exploration", "Planning", "Social", "Social", "Social",
#         "Social", "Execution", "Execution", "Social", "Recovery", "Execution",
#         "Feedback", "Feedback", "Execution", "Execution", "Execution", "Recovery"
#     ],
#     "PMA-Self": [
#         "Execution", "Exploration", "Exploration", "Exploration", "Execution", "Execution",
#         "Social", "Social", "Social", "Social", "Execution", "Social",
#         "Execution", "Execution", "Execution", "Execution", "Exploration", "Execution",
#         "Execution", "Execution", "Execution", "Execution", "Social", "Recovery",
#         "Social", "Social", "Execution", "Execution", "Feedback", "Feedback"
#     ],
#     "PMA-Mind": [
#         "Execution", "Recovery", "Execution", "Execution", "Execution", "Execution",
#         "Execution", "Execution", "Execution", "Social", "Social", "Planning",
#         "Recovery", "Recovery", "Exploration", "Exploration", "Exploration", "Exploration",
#         "Recovery", "Feedback", "Social", "Feedback", "Execution", "Recovery",
#         "Execution", "Execution", "Execution", "Exploration", "Exploration", "Execution"
#     ],
#     "PMA-Core": [
#         "Execution", "Recovery", "Execution", "Execution", "Execution", "Execution",
#         "Social", "Execution", "Feedback", "Recovery", "Recovery", "Social",
#         "Execution", "Execution", "Exploration", "Social", "Execution", "Execution",
#         "Execution", "Execution", "Execution", "Execution", "Recovery", "Social",
#         "Feedback", "Feedback", "Execution", "Execution", "Planning", "Execution"
#     ],
#     "PMA": [
#         "Execution", "Recovery", "Recovery", "Execution", "Planning", "Social",
#         "Feedback", "Execution", "Planning", "Planning", "Execution", "Planning",
#         "Social", "Recovery", "Execution", "Feedback", "Planning", "Planning",
#         "Planning", "Execution", "Planning", "Feedback", "Execution", "Feedback",
#         "Feedback", "Planning", "Execution", "Execution", "Recovery", "Recovery"
#     ],
# }
#
# # =========================================================
# # Derived metrics
# # =========================================================
# coherence = {}
# diversity = {}
# for model in model_order_all:
#     coherence[model] = np.mean([
#         get_mean(model, "Emotion"),
#         get_mean(model, "Identity"),
#         get_mean(model, "Plausibility"),
#     ])
#     diversity[model] = get_mean(model, "Diversity")
#
# # =========================================================
# # Figure layout
# # =========================================================
# fig = plt.figure(figsize=(16.6, 10.0))
# gs = GridSpec(
#     2, 3,
#     figure=fig,
#     left=0.07,
#     right=0.985,
#     top=0.965,
#     bottom=0.11,
#     wspace=0.33,
#     hspace=0.42
# )
#
# ax_a = fig.add_subplot(gs[0, 0])
# ax_b = fig.add_subplot(gs[0, 1])
# ax_c = fig.add_subplot(gs[0, 2])
# ax_d = fig.add_subplot(gs[1, 0])
# ax_e = fig.add_subplot(gs[1, 1])
# ax_f = fig.add_subplot(gs[1, 2])
#
# # =========================================================
# # a. Daily-life behavioural trajectories
# # =========================================================
# bar_h = 0.76
# for i, model in enumerate(model_order_traj):
#     y = len(model_order_traj) - 1 - i
#     for j, category in enumerate(trajectory_blocks[model]):
#         ax_a.add_patch(Rectangle(
#             (j, y - bar_h / 2),
#             1,
#             bar_h,
#             facecolor=func_colors[category],
#             edgecolor="white",
#             linewidth=0.45
#         ))
#
# ax_a.set_xlim(0, len(time_blocks))
# ax_a.set_ylim(-0.6, len(model_order_traj) - 0.4)
# ax_a.set_yticks(range(len(model_order_traj)))
# ax_a.set_yticklabels([model_short[m] for m in model_order_traj[::-1]])
# tick_idx = np.arange(0, len(time_blocks), 4)
# ax_a.set_xticks(tick_idx + 0.5)
# ax_a.set_xticklabels([time_blocks[i] for i in tick_idx])
# ax_a.grid(axis="x", linestyle="--", alpha=0.20)
# ax_a.set_xlabel("Time of day")
# ax_a.set_title("a  Daily-life behavioural trajectories", loc="left", fontweight="bold", pad=6)
#
# # =========================================================
# # b. Functional composition
# # =========================================================
# left = np.zeros(len(model_order_traj))
# for cat in func_colors.keys():
#     vals = np.array([functional_composition[m][cat] for m in model_order_traj])
#     ax_b.barh(
#         [model_short[m] for m in model_order_traj],
#         vals,
#         left=left,
#         color=func_colors[cat],
#         edgecolor="white",
#         linewidth=0.7
#     )
#     left += vals
#
# ax_b.set_xlim(0, 100)
# ax_b.set_xlabel("Proportion of daily events (%)")
# ax_b.grid(axis="x", linestyle="--", alpha=0.20)
# ax_b.set_title("b  Functional composition of simulated behaviour", loc="left", fontweight="bold", pad=6)
#
# # =========================================================
# # c. Human evaluation heatmap
# # =========================================================
# rating_matrix = np.array([
#     [get_mean(m, metric) for metric in metric_order]
#     for m in model_order_all
# ])
#
# heat_cmap = LinearSegmentedColormap.from_list(
#     "eval_map",
#     ["#F2F2F2", "#D7E6F2", "#8FB6DA", "#CC466E"]
# )
#
# im = ax_c.imshow(
#     rating_matrix,
#     aspect="auto",
#     cmap=heat_cmap,
#     vmin=3.2,
#     vmax=5.0
# )
#
# ax_c.set_yticks(np.arange(len(model_order_all)))
# ax_c.set_yticklabels([model_short[m] for m in model_order_all])
# ax_c.set_xticks(np.arange(len(metric_order)))
# ax_c.set_xticklabels([metric_long[m] for m in metric_order])
#
# for i in range(rating_matrix.shape[0]):
#     for j in range(rating_matrix.shape[1]):
#         v = rating_matrix[i, j]
#         txt_color = "white" if v >= 4.50 else "black"
#         ax_c.text(
#             j, i, f"{v:.2f}",
#             ha="center", va="center",
#             fontsize=8.5,
#             color=txt_color
#         )
#
# for spine in ax_c.spines.values():
#     spine.set_visible(False)
# ax_c.tick_params(length=0)
#
# for x in np.arange(-0.5, len(metric_order), 1):
#     ax_c.axvline(x, color="white", lw=1.1)
# for y in np.arange(-0.5, len(model_order_all), 1):
#     ax_c.axhline(y, color="white", lw=1.1)
#
# ax_c.set_title("c  Human evaluation across models", loc="left", fontweight="bold", pad=6)
#
# cbar = fig.colorbar(im, ax=ax_c, fraction=0.046, pad=0.03)
# cbar.set_label("Mean score", fontsize=9)
# cbar.ax.tick_params(labelsize=8)
#
# # =========================================================
# # d. Rater-level evaluation variability
# # =========================================================
# focus_models = ["Base-Agent", "PMA-Core", "PMA"]
# focus_labels = ["Base", "Core", "PMA"]
#
# y_centers = np.arange(len(metric_order))[::-1] * 1.35
# model_offsets = [-0.24, 0.0, 0.24]
# rng = np.random.default_rng(2026)
#
# for k, model in enumerate(focus_models):
#     for mi, metric in enumerate(metric_order):
#         vals = np.array(rater_level[model][metric])
#         y0 = y_centers[mi] + model_offsets[k]
#
#         jitter = rng.normal(0, 0.015, size=len(vals))
#         ax_d.scatter(
#             vals,
#             np.full_like(vals, y0) + jitter,
#             s=23,
#             color=model_colors[model],
#             alpha=0.18,
#             edgecolor="none",
#             zorder=2
#         )
#
#         mean = vals.mean()
#         sd = vals.std(ddof=1)
#
#         ax_d.errorbar(
#             mean,
#             y0,
#             xerr=sd,
#             fmt="D",
#             ms=5.8,
#             color=model_colors[model],
#             ecolor=model_colors[model],
#             elinewidth=1.55,
#             capsize=3.5,
#             capthick=1.2,
#             zorder=4
#         )
#
# for y in y_centers:
#     ax_d.axhline(
#         y - 0.60,
#         color="#EAEAEA",
#         lw=1.0,
#         zorder=0
#     )
#
# ax_d.set_yticks(y_centers)
# ax_d.set_yticklabels([metric_short[m] for m in metric_order])
# ax_d.set_xlim(2.4, 5.15)
# ax_d.set_xlabel("Rater-level mean score")
# ax_d.grid(axis="x", linestyle="--", alpha=0.18)
# ax_d.set_title("d  Rater-level evaluation variability", loc="left", fontweight="bold", pad=6)
#
# legend_d = [
#     Line2D(
#         [0], [0],
#         marker="D",
#         color=model_colors[m],
#         markerfacecolor=model_colors[m],
#         markeredgecolor=model_colors[m],
#         markersize=6,
#         linewidth=1.4,
#         label=label
#     )
#     for m, label in zip(focus_models, focus_labels)
# ]
#
# ax_d.legend(
#     handles=legend_d,
#     frameon=False,
#     loc="upper left"
# )
#
# icc_single_min = min(icc_data[m]["ICC2_1_absolute_single"] for m in metric_order)
# icc_single_max = max(icc_data[m]["ICC2_1_absolute_single"] for m in metric_order)
# icc_avg_min = min(icc_data[m]["ICC2_k_absolute_average"] for m in metric_order)
# icc_avg_max = max(icc_data[m]["ICC2_k_absolute_average"] for m in metric_order)
#
# ax_d.text(
#     0.02, 0.04,
#     # f"Framework-mean ICC(A,1) = {icc_single_min:.2f}{icc_single_max:.2f}; "
#     # f"ICC(A,k) = {icc_avg_min:.2f}{icc_avg_max:.2f}",
#     f"ICC(2,k) > 0.8",
#     transform=ax_d.transAxes,
#     fontsize=8.0,
#     color="#666666",
#     ha="left",
#     va="bottom"
# )
#
# # =========================================================
# # e. Coherencediversity landscape
# # =========================================================
# ax_e.axvline(4.0, ls="--", lw=1.0, color="#A9A9A9")
# ax_e.axhline(4.0, ls="--", lw=1.0, color="#A9A9A9")
# ax_e.axvspan(4.0, 4.75, color="#EEF4FB", zorder=0)
# ax_e.axhspan(4.0, 4.90, color="#FBEFF3", zorder=0)
#
# label_offsets = {
#     "Base-Agent": (0.03, -0.04),
#     "PMA-Affect": (0.03, 0.03),
#     "PMA-Sim": (0.03, -0.05),
#     "PMA-Self": (0.03, 0.03),
#     "PMA-Mind": (0.03, -0.04),
#     "PMA-Core": (0.03, 0.03),
#     "PMA": (0.03, 0.03),
# }
#
# for model in model_order_all:
#     x = diversity[model]
#     y = coherence[model]
#     ax_e.scatter(
#         x, y,
#         s=185 if model == "PMA" else 125,
#         color=model_colors[model],
#         edgecolor="white",
#         linewidth=1.2,
#         zorder=3
#     )
#     dx, dy = label_offsets[model]
#     ax_e.text(
#         x + dx, y + dy,
#         model_short[model],
#         fontsize=9.2,
#         color="#333333"
#     )
#
# ax_e.set_xlim(3.35, 4.65)
# ax_e.set_ylim(3.75, 4.86)
# ax_e.set_xlabel("Behavioural diversity")
# ax_e.set_ylabel("Coherence composite")
# ax_e.grid(True, linestyle="--", alpha=0.20)
# ax_e.set_title("e  Coherencediversity landscape", loc="left", fontweight="bold", pad=6)
#
# # =========================================================
# # f. PMA gains over baselines
# # =========================================================
# gain_metrics = ["Emotion", "Identity", "Plausibility", "Diversity"]
# gain_labels = ["Emotion", "Identity", "Plausibility", "Diversity"]
#
# pma_vs_base = np.array([get_mean("PMA", m) - get_mean("Base-Agent", m) for m in gain_metrics])
# pma_vs_core = np.array([get_mean("PMA", m) - get_mean("PMA-Core", m) for m in gain_metrics])
#
# y = np.arange(len(gain_metrics))
# bar_h = 0.32
#
# ax_f.barh(
#     y - bar_h / 2,
#     pma_vs_base,
#     height=bar_h,
#     color="#CC466E",
#     alpha=0.85,
#     label="PMA  Base"
# )
# ax_f.barh(
#     y + bar_h / 2,
#     pma_vs_core,
#     height=bar_h,
#     color="#3B84C3",
#     alpha=0.85,
#     label="PMA  Core"
# )
#
# ax_f.axvline(0, color="black", lw=0.9)
# ax_f.set_yticks(y)
# ax_f.set_yticklabels(gain_labels)
# ax_f.set_xlim(-0.95, 1.55)
# ax_f.set_xlabel("Score difference")
# ax_f.grid(axis="x", linestyle="--", alpha=0.20)
# ax_f.set_title("f  PMA gains over baselines", loc="left", fontweight="bold", pad=6)
# ax_f.legend(frameon=False, loc="upper right")
#
# for i, val in enumerate(pma_vs_base):
#     ax_f.text(
#         val + (0.03 if val >= 0 else -0.03),
#         i - bar_h / 2,
#         f"{val:+.2f}",
#         va="center",
#         ha="left" if val >= 0 else "right",
#         fontsize=8.3
#     )
#
# for i, val in enumerate(pma_vs_core):
#     ax_f.text(
#         val + (0.03 if val >= 0 else -0.03),
#         i + bar_h / 2,
#         f"{val:+.2f}",
#         va="center",
#         ha="left" if val >= 0 else "right",
#         fontsize=8.3
#     )
#
# # =========================================================
# # Functional legend ONLY below panel a and b
# # =========================================================
# func_handles = [
#     Rectangle((0, 0), 1, 1, facecolor=func_colors[k], edgecolor="none", label=k)
#     for k in func_colors.keys()
# ]
#
# # 
# fig.canvas.draw()
#
# pos_a = ax_a.get_position()
# pos_b = ax_b.get_position()
#
# legend_center_x = (pos_a.x0 + pos_b.x1) / 2
# legend_y = min(pos_a.y0, pos_b.y0) - 0.05
#
# fig.legend(
#     handles=func_handles,
#     frameon=False,
#     loc="upper center",
#     bbox_to_anchor=(legend_center_x, legend_y),
#     bbox_transform=fig.transFigure,
#     ncol=6,
#     columnspacing=1.2,
#     handlelength=1.6,
#     handletextpad=0.5
# )
#
# # =========================================================
# # Save / show
# # =========================================================
# # fig.savefig("Figure2_daily_life_simulation_updatedICC.png", dpi=400, bbox_inches="tight")
# fig.savefig("outputs/Figure2.pdf", dpi=400, bbox_inches="tight")
# plt.show()




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap

# =========================================================
# Output paths
# =========================================================
# This version is fully hard-coded. It does not read CSV, Excel, or zip files.
# After running it, upload/replace Figure2.pdf in Overleaf as figures/Figure2.pdf.
OUTPUT_PDF = "Figure2.pdf"
OUTPUT_PNG = "Figure2.png"  # optional

# =========================================================
# Basic style
# =========================================================
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# =========================================================
# Model names and colours
# =========================================================
model_order_all = [
    "Base-Agent", "PMA-Affect", "PMA-Sim",
    "PMA-Self", "PMA-Mind", "PMA-Core", "PMA"
]

model_order_traj = [
    "Base-Agent", "PMA-Affect", "PMA-Sim",
    "PMA-Self", "PMA-Mind", "PMA-Core", "PMA"
]

model_short = {
    "Base-Agent": "Base",
    "PMA-Affect": "Affect",
    "PMA-Sim": "Sim",
    "PMA-Self": "Self",
    "PMA-Mind": "Mind",
    "PMA-Core": "Core",
    "PMA": "PMA",
}

model_colors = {
    "Base-Agent": "#B8B8B8",
    "PMA-Affect": "#D8A15B",
    "PMA-Sim": "#4FA7A6",
    "PMA-Self": "#8E72B5",
    "PMA-Mind": "#7FAE6B",
    "PMA-Core": "#3B84C3",
    "PMA": "#CC466E",
}

# =========================================================
# Low-saturation functional colours
# =========================================================
func_colors = {
    "Execution":   "#94cbc1",
    "Social":      "#cce6e2",
    "Recovery":    "#f6e2b7",
    "Feedback":    "#c6aacc",
    "Exploration": "#e2d6e7",
    "Planning":    "#efbdb8",
}

# =========================================================
# Latest hard-coded rating data
# Format: mean, SE, SD across raters
# Scores are on a 1-5 scale.
# =========================================================
rating_data = {'Base-Agent': {'Emotion': (3.65, 0.0479, 0.1514),
                'Identity': (3.4607, 0.047, 0.1487),
                'Diversity': (4.1705, 0.0498, 0.1575),
                'Plausibility': (4.9098, 0.0137, 0.0432)},
 'PMA-Affect': {'Emotion': (4.3595, 0.0503, 0.1589),
                'Identity': (3.6705, 0.0333, 0.1052),
                'Diversity': (3.9, 0.0651, 0.2058),
                'Plausibility': (4.3705, 0.0435, 0.1376)},
 'PMA-Sim': {'Emotion': (3.819, 0.0638, 0.2018),
             'Identity': (3.3295, 0.0442, 0.1396),
             'Diversity': (3.5902, 0.0711, 0.2248),
             'Plausibility': (4.4197, 0.037, 0.117)},
 'PMA-Self': {'Emotion': (3.7, 0.0566, 0.179),
              'Identity': (4.8295, 0.0196, 0.0619),
              'Diversity': (3.5902, 0.0734, 0.232),
              'Plausibility': (4.4803, 0.0397, 0.1256)},
 'PMA-Mind': {'Emotion': (3.781, 0.0509, 0.161),
              'Identity': (3.5, 0.0471, 0.1491),
              'Diversity': (4.4607, 0.0464, 0.1467),
              'Plausibility': (4.2705, 0.0354, 0.1118)},
 'PMA-Core': {'Emotion': (4.4095, 0.0497, 0.1571),
              'Identity': (4.8295, 0.017, 0.0537),
              'Diversity': (4.3197, 0.0606, 0.1917),
              'Plausibility': (4.5705, 0.0356, 0.1125)},
 'PMA': {'Emotion': (4.55, 0.0338, 0.1067),
         'Identity': (4.8492, 0.0158, 0.05),
         'Diversity': (3.5295, 0.0713, 0.2253),
         'Plausibility': (4.7803, 0.0335, 0.106)}}

metric_order = ["Emotion", "Identity", "Diversity", "Plausibility"]
metric_long = {
    "Emotion": "Emotional\nnaturalness",
    "Identity": "Identity\nconsistency",
    "Diversity": "Behavioural\ndiversity",
    "Plausibility": "Behavioural\nplausibility",
}
metric_short = {
    "Emotion": "Emotion",
    "Identity": "Identity",
    "Diversity": "Diversity",
    "Plausibility": "Plausibility",
}

def get_mean(model, metric):
    return rating_data[model][metric][0]

def get_se(model, metric):
    return rating_data[model][metric][1]

def get_sd(model, metric):
    return rating_data[model][metric][2]

# =========================================================
# ICC from framework-ratermean method
# =========================================================
icc_data = {'Emotion': {'ICC2_1_absolute_single': 0.848251, 'ICC2_k_absolute_average': 0.982425},
 'Identity': {'ICC2_1_absolute_single': 0.977689, 'ICC2_k_absolute_average': 0.997723},
 'Diversity': {'ICC2_1_absolute_single': 0.785315, 'ICC2_k_absolute_average': 0.97339},
 'Plausibility': {'ICC2_1_absolute_single': 0.807477, 'ICC2_k_absolute_average': 0.976713}}

# =========================================================
# Rater-level data
# Each point in panel d is one rater's mean score.
# =========================================================
rater_level = {'Base-Agent': {'Emotion': [3.5476, 3.5714, 3.619, 3.5238, 3.7381, 3.5714, 3.619, 4.0238, 3.7381, 3.5476],
                'Identity': [3.1639, 3.3934, 3.3607, 3.5574, 3.623, 3.4426, 3.459, 3.6885, 3.5246, 3.3934],
                'Diversity': [3.9344, 4.082, 4.2951, 4.1148, 4.0328, 4.4098, 4.3934, 4.2295, 4.0656, 4.1475],
                'Plausibility': [4.8197,
                                 4.9344,
                                 4.918,
                                 4.8689,
                                 4.918,
                                 4.9016,
                                 4.9508,
                                 4.9672,
                                 4.8852,
                                 4.9344]},
 'PMA-Core': {'Emotion': [4.3095, 4.4286, 4.2857, 4.2619, 4.4524, 4.4286, 4.381, 4.6905, 4.6429, 4.2143],
              'Identity': [4.7869, 4.7377, 4.8689, 4.8361, 4.8197, 4.9016, 4.8361, 4.9016, 4.8361, 4.7705],
              'Diversity': [3.9836, 4.2295, 4.459, 4.2295, 4.1803, 4.5574, 4.6066, 4.4098, 4.3443, 4.1967],
              'Plausibility': [4.377,
                               4.4262,
                               4.5574,
                               4.5082,
                               4.5738,
                               4.5574,
                               4.7049,
                               4.6885,
                               4.7049,
                               4.6066]},
 'PMA': {'Emotion': [4.4286, 4.5476, 4.619, 4.5714, 4.5476, 4.7143, 4.4048, 4.6429, 4.619, 4.4048],
         'Identity': [4.8033, 4.8525, 4.8197, 4.8852, 4.8197, 4.7705, 4.9016, 4.918, 4.9016, 4.8197],
         'Diversity': [3.2787, 3.3279, 3.7377, 3.3934, 3.3934, 3.8197, 3.9016, 3.5738, 3.5574, 3.3115],
         'Plausibility': [4.6557, 4.7213, 4.623, 4.7377, 4.7869, 4.7377, 4.9344, 4.9344, 4.8361, 4.8361]}}

# =========================================================
# Functional composition
# Values are percentages of daily events; all seven model variants are included.
# =========================================================
functional_composition = {'Base-Agent': {'Execution': 27.8689,
                'Social': 24.5902,
                'Recovery': 19.6721,
                'Feedback': 6.5574,
                'Exploration': 11.4754,
                'Planning': 9.8361},
 'PMA-Affect': {'Execution': 9.8361,
                'Social': 45.9016,
                'Recovery': 18.0328,
                'Feedback': 6.5574,
                'Exploration': 9.8361,
                'Planning': 9.8361},
 'PMA-Sim': {'Execution': 39.3443,
             'Social': 24.5902,
             'Recovery': 13.1148,
             'Feedback': 1.6393,
             'Exploration': 13.1148,
             'Planning': 8.1967},
 'PMA-Self': {'Execution': 36.0656,
              'Social': 21.3115,
              'Recovery': 8.1967,
              'Feedback': 8.1967,
              'Exploration': 19.6721,
              'Planning': 6.5574},
 'PMA-Mind': {'Execution': 57.377,
              'Social': 14.7541,
              'Recovery': 8.1967,
              'Feedback': 0.0,
              'Exploration': 13.1148,
              'Planning': 6.5574},
 'PMA-Core': {'Execution': 52.459,
              'Social': 14.7541,
              'Recovery': 11.4754,
              'Feedback': 9.8361,
              'Exploration': 4.918,
              'Planning': 6.5574},
 'PMA': {'Execution': 21.3115,
         'Social': 24.5902,
         'Recovery': 19.6721,
         'Feedback': 13.1148,
         'Exploration': 8.1967,
         'Planning': 13.1148}}

# =========================================================
# Compact daily trajectory blocks
# Sampled every 30 minutes from the updated 15-minute daily-life trajectory; all seven model variants are included.
# =========================================================
time_blocks = ['07:00',
 '07:30',
 '08:00',
 '08:30',
 '09:00',
 '09:30',
 '10:00',
 '10:30',
 '11:00',
 '11:30',
 '12:00',
 '12:30',
 '13:00',
 '13:30',
 '14:00',
 '14:30',
 '15:00',
 '15:30',
 '16:00',
 '16:30',
 '17:00',
 '17:30',
 '18:00',
 '18:30',
 '19:00',
 '19:30',
 '20:00',
 '20:30',
 '21:00',
 '21:30',
 '22:00']

trajectory_blocks = {'Base-Agent': ['Execution',
                'Recovery',
                'Execution',
                'Planning',
                'Social',
                'Social',
                'Execution',
                'Planning',
                'Execution',
                'Execution',
                'Recovery',
                'Recovery',
                'Execution',
                'Social',
                'Social',
                'Social',
                'Social',
                'Social',
                'Recovery',
                'Feedback',
                'Recovery',
                'Feedback',
                'Exploration',
                'Exploration',
                'Feedback',
                'Exploration',
                'Planning',
                'Execution',
                'Execution',
                'Execution',
                'Recovery'],
 'PMA-Affect': ['Recovery',
                'Recovery',
                'Recovery',
                'Planning',
                'Social',
                'Social',
                'Exploration',
                'Social',
                'Social',
                'Social',
                'Execution',
                'Social',
                'Planning',
                'Social',
                'Exploration',
                'Planning',
                'Social',
                'Social',
                'Feedback',
                'Social',
                'Social',
                'Social',
                'Execution',
                'Social',
                'Recovery',
                'Social',
                'Social',
                'Execution',
                'Social',
                'Recovery',
                'Recovery'],
 'PMA-Sim': ['Execution',
             'Recovery',
             'Execution',
             'Exploration',
             'Planning',
             'Social',
             'Social',
             'Execution',
             'Execution',
             'Planning',
             'Execution',
             'Execution',
             'Planning',
             'Exploration',
             'Execution',
             'Social',
             'Social',
             'Social',
             'Social',
             'Execution',
             'Exploration',
             'Social',
             'Execution',
             'Exploration',
             'Exploration',
             'Feedback',
             'Execution',
             'Execution',
             'Execution',
             'Recovery',
             'Recovery'],
 'PMA-Self': ['Execution',
              'Exploration',
              'Exploration',
              'Exploration',
              'Execution',
              'Planning',
              'Social',
              'Social',
              'Social',
              'Execution',
              'Execution',
              'Social',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Planning',
              'Execution',
              'Feedback',
              'Recovery',
              'Execution',
              'Feedback',
              'Social',
              'Execution',
              'Social',
              'Social',
              'Execution',
              'Planning',
              'Exploration',
              'Execution',
              'Recovery'],
 'PMA-Mind': ['Execution',
              'Recovery',
              'Planning',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Social',
              'Social',
              'Planning',
              'Execution',
              'Recovery',
              'Execution',
              'Exploration',
              'Exploration',
              'Exploration',
              'Execution',
              'Social',
              'Social',
              'Social',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Execution',
              'Exploration',
              'Execution',
              'Execution',
              'Execution'],
 'PMA-Core': ['Execution',
              'Recovery',
              'Execution',
              'Execution',
              'Feedback',
              'Execution',
              'Social',
              'Execution',
              'Execution',
              'Recovery',
              'Social',
              'Social',
              'Execution',
              'Planning',
              'Exploration',
              'Social',
              'Execution',
              'Execution',
              'Execution',
              'Recovery',
              'Execution',
              'Execution',
              'Execution',
              'Social',
              'Feedback',
              'Feedback',
              'Feedback',
              'Execution',
              'Planning',
              'Execution',
              'Execution'],
 'PMA': ['Recovery',
         'Recovery',
         'Recovery',
         'Execution',
         'Planning',
         'Social',
         'Social',
         'Execution',
         'Planning',
         'Exploration',
         'Execution',
         'Planning',
         'Execution',
         'Recovery',
         'Recovery',
         'Social',
         'Planning',
         'Planning',
         'Planning',
         'Execution',
         'Social',
         'Social',
         'Execution',
         'Social',
         'Feedback',
         'Social',
         'Feedback',
         'Execution',
         'Execution',
         'Execution',
         'Recovery']}

# =========================================================
# Derived metrics
# =========================================================
coherence = {}
diversity = {}
for model in model_order_all:
    coherence[model] = np.mean([
        get_mean(model, "Emotion"),
        get_mean(model, "Identity"),
        get_mean(model, "Plausibility"),
    ])
    diversity[model] = get_mean(model, "Diversity")

# =========================================================
# Figure layout
# =========================================================
fig = plt.figure(figsize=(16.6, 10.0))
gs = GridSpec(
    2, 3,
    figure=fig,
    left=0.07,
    right=0.985,
    top=0.965,
    bottom=0.11,
    wspace=0.33,
    hspace=0.42
)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, 0])
ax_e = fig.add_subplot(gs[1, 1])
ax_f = fig.add_subplot(gs[1, 2])

# =========================================================
# a. Daily-life behavioural trajectories
# =========================================================
bar_h = 0.76
for i, model in enumerate(model_order_traj):
    y = len(model_order_traj) - 1 - i
    for j, category in enumerate(trajectory_blocks[model]):
        ax_a.add_patch(Rectangle(
            (j, y - bar_h / 2),
            1,
            bar_h,
            facecolor=func_colors[category],
            edgecolor="white",
            linewidth=0.45
        ))

ax_a.set_xlim(0, len(time_blocks))
ax_a.set_ylim(-0.6, len(model_order_traj) - 0.4)
ax_a.set_yticks(range(len(model_order_traj)))
ax_a.set_yticklabels([model_short[m] for m in model_order_traj[::-1]])

# Label every 2 hours. Since blocks are every 30 minutes, every 4 blocks = 2 hours.
tick_idx = np.arange(0, len(time_blocks), 4)
ax_a.set_xticks(tick_idx + 0.5)
ax_a.set_xticklabels([time_blocks[i] for i in tick_idx])
ax_a.grid(axis="x", linestyle="--", alpha=0.20)
ax_a.set_xlabel("Time of day")
ax_a.set_title("a  Daily-life behavioural trajectories", loc="left", fontweight="bold", pad=6)

# =========================================================
# b. Functional composition
# =========================================================
left = np.zeros(len(model_order_traj))
for cat in func_colors.keys():
    vals = np.array([functional_composition[m][cat] for m in model_order_traj])
    ax_b.barh(
        [model_short[m] for m in model_order_traj],
        vals,
        left=left,
        color=func_colors[cat],
        edgecolor="white",
        linewidth=0.7
    )
    left += vals

ax_b.set_xlim(0, 100)
ax_b.set_xlabel("Proportion of daily events (%)")
ax_b.grid(axis="x", linestyle="--", alpha=0.20)
ax_b.set_title("b  Functional composition of simulated behaviour", loc="left", fontweight="bold", pad=6)

# =========================================================
# c. Human evaluation heatmap
# =========================================================
rating_matrix = np.array([
    [get_mean(m, metric) for metric in metric_order]
    for m in model_order_all
])

heat_cmap = LinearSegmentedColormap.from_list(
    "eval_map",
    ["#F2F2F2", "#D7E6F2", "#8FB6DA", "#CC466E"]
)

im = ax_c.imshow(
    rating_matrix,
    aspect="auto",
    cmap=heat_cmap,
    vmin=3.2,
    vmax=5.0
)

ax_c.set_yticks(np.arange(len(model_order_all)))
ax_c.set_yticklabels([model_short[m] for m in model_order_all])
ax_c.set_xticks(np.arange(len(metric_order)))
ax_c.set_xticklabels([metric_long[m] for m in metric_order])

for i in range(rating_matrix.shape[0]):
    for j in range(rating_matrix.shape[1]):
        v = rating_matrix[i, j]
        txt_color = "white" if v >= 4.50 else "black"
        ax_c.text(
            j, i, f"{v:.2f}",
            ha="center", va="center",
            fontsize=8.5,
            color=txt_color
        )

for spine in ax_c.spines.values():
    spine.set_visible(False)
ax_c.tick_params(length=0)

for x in np.arange(-0.5, len(metric_order), 1):
    ax_c.axvline(x, color="white", lw=1.1)
for y in np.arange(-0.5, len(model_order_all), 1):
    ax_c.axhline(y, color="white", lw=1.1)

ax_c.set_title("c  Human evaluation across models", loc="left", fontweight="bold", pad=6)

cbar = fig.colorbar(im, ax=ax_c, fraction=0.046, pad=0.03)
cbar.set_label("Mean score", fontsize=9)
cbar.ax.tick_params(labelsize=8)

# =========================================================
# d. Rater-level evaluation variability
# =========================================================
focus_models = ["Base-Agent", "PMA-Core", "PMA"]
focus_labels = ["Base", "Core", "PMA"]

y_centers = np.arange(len(metric_order))[::-1] * 1.35
model_offsets = [-0.24, 0.0, 0.24]
rng = np.random.default_rng(2026)

for k, model in enumerate(focus_models):
    for mi, metric in enumerate(metric_order):
        vals = np.array(rater_level[model][metric])
        y0 = y_centers[mi] + model_offsets[k]

        jitter = rng.normal(0, 0.015, size=len(vals))
        ax_d.scatter(
            vals,
            np.full_like(vals, y0) + jitter,
            s=23,
            color=model_colors[model],
            alpha=0.18,
            edgecolor="none",
            zorder=2
        )

        mean = vals.mean()
        sd = vals.std(ddof=1)

        ax_d.errorbar(
            mean,
            y0,
            xerr=sd,
            fmt="D",
            ms=5.8,
            color=model_colors[model],
            ecolor=model_colors[model],
            elinewidth=1.55,
            capsize=3.5,
            capthick=1.2,
            zorder=4
        )

for y in y_centers:
    ax_d.axhline(y - 0.60, color="#EAEAEA", lw=1.0, zorder=0)

ax_d.set_yticks(y_centers)
ax_d.set_yticklabels([metric_short[m] for m in metric_order])
ax_d.set_xlim(3.0, 5.15)
ax_d.set_xlabel("Rater-level mean score")
ax_d.grid(axis="x", linestyle="--", alpha=0.18)
ax_d.set_title("d  Rater-level evaluation variability", loc="left", fontweight="bold", pad=6)

legend_d = [
    Line2D(
        [0], [0],
        marker="D",
        color=model_colors[m],
        markerfacecolor=model_colors[m],
        markeredgecolor=model_colors[m],
        markersize=6,
        linewidth=1.4,
        label=label
    )
    for m, label in zip(focus_models, focus_labels)
]

ax_d.legend(handles=legend_d, frameon=False, loc="upper left")

ax_d.text(
    0.02, 0.04,
    "ICC(2,k) > 0.8",
    transform=ax_d.transAxes,
    fontsize=8.0,
    color="#666666",
    ha="left",
    va="bottom"
)

# =========================================================
# e. Coherence-diversity landscape
# =========================================================
ax_e.axvline(4.0, ls="--", lw=1.0, color="#A9A9A9")
ax_e.axhline(4.0, ls="--", lw=1.0, color="#A9A9A9")
ax_e.axvspan(4.0, 4.75, color="#EEF4FB", zorder=0)
ax_e.axhspan(4.0, 4.90, color="#FBEFF3", zorder=0)

label_offsets = {
    "Base-Agent": (0.03, -0.04),
    "PMA-Affect": (0.03, 0.03),
    "PMA-Sim": (0.03, -0.05),
    "PMA-Self": (0.03, 0.03),
    "PMA-Mind": (0.03, -0.04),
    "PMA-Core": (0.03, 0.03),
    "PMA": (0.03, 0.03),
}

for model in model_order_all:
    x = diversity[model]
    y = coherence[model]
    ax_e.scatter(
        x, y,
        s=185 if model == "PMA" else 125,
        color=model_colors[model],
        edgecolor="white",
        linewidth=1.2,
        zorder=3
    )
    dx, dy = label_offsets[model]
    ax_e.text(x + dx, y + dy, model_short[model], fontsize=9.2, color="#333333")

ax_e.set_xlim(3.35, 4.65)
ax_e.set_ylim(3.75, 4.86)
ax_e.set_xlabel("Behavioural diversity")
ax_e.set_ylabel("Coherence composite")
ax_e.grid(True, linestyle="--", alpha=0.20)
ax_e.set_title("e  Coherence-diversity landscape", loc="left", fontweight="bold", pad=6)

# =========================================================
# f. PMA gains over baselines
# =========================================================
gain_metrics = ["Emotion", "Identity", "Plausibility", "Diversity"]
gain_labels = ["Emotion", "Identity", "Plausibility", "Diversity"]

pma_vs_base = np.array([get_mean("PMA", m) - get_mean("Base-Agent", m) for m in gain_metrics])
pma_vs_core = np.array([get_mean("PMA", m) - get_mean("PMA-Core", m) for m in gain_metrics])

y = np.arange(len(gain_metrics))
bar_h = 0.32

ax_f.barh(
    y - bar_h / 2,
    pma_vs_base,
    height=bar_h,
    color="#CC466E",
    alpha=0.85,
    label="PMA - Base"
)
ax_f.barh(
    y + bar_h / 2,
    pma_vs_core,
    height=bar_h,
    color="#3B84C3",
    alpha=0.85,
    label="PMA - Core"
)

ax_f.axvline(0, color="black", lw=0.9)
ax_f.set_yticks(y)
ax_f.set_yticklabels(gain_labels)
ax_f.set_xlim(-0.95, 1.55)
ax_f.set_xlabel("Score difference")
ax_f.grid(axis="x", linestyle="--", alpha=0.20)
ax_f.set_title("f  PMA gains over baselines", loc="left", fontweight="bold", pad=6)
ax_f.legend(frameon=False, loc="upper right")

for i, val in enumerate(pma_vs_base):
    ax_f.text(
        val + (0.03 if val >= 0 else -0.03),
        i - bar_h / 2,
        f"{val:+.2f}",
        va="center",
        ha="left" if val >= 0 else "right",
        fontsize=8.3
    )

for i, val in enumerate(pma_vs_core):
    ax_f.text(
        val + (0.03 if val >= 0 else -0.03),
        i + bar_h / 2,
        f"{val:+.2f}",
        va="center",
        ha="left" if val >= 0 else "right",
        fontsize=8.3
    )

# =========================================================
# Functional legend below panel a and b
# =========================================================
func_handles = [
    Rectangle((0, 0), 1, 1, facecolor=func_colors[k], edgecolor="none", label=k)
    for k in func_colors.keys()
]

fig.canvas.draw()
pos_a = ax_a.get_position()
pos_b = ax_b.get_position()
legend_center_x = (pos_a.x0 + pos_b.x1) / 2
legend_y = min(pos_a.y0, pos_b.y0) - 0.05

fig.legend(
    handles=func_handles,
    frameon=False,
    loc="upper center",
    bbox_to_anchor=(legend_center_x, legend_y),
    bbox_transform=fig.transFigure,
    ncol=6,
    columnspacing=1.2,
    handlelength=1.6,
    handletextpad=0.5
)

# =========================================================
# Save / show
# =========================================================
# fig.savefig(OUTPUT_PDF, dpi=400, bbox_inches="tight")
# fig.savefig(OUTPUT_PNG, dpi=400, bbox_inches="tight")
plt.show()
