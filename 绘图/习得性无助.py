import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. Data written directly in code
# =========================================================

frameworks = [
    'Human',
    'Base-Agent',
    'PMA-Affect',
    'PMA-Sim',
    'PMA-Self',
    'PMA-Core',
    'PMA'
]

groups = ['E', 'NE', 'NP']

# ---------- Failure rate ----------
failure_mean = {
    'Human': [50.0, 13.0, 11.0],   # estimated from your current figure
    'Base-Agent': [4.8333, 12.5556, 10.6782],
    'PMA-Affect': [53.5624, 8.5000, 7.4402],
    'PMA-Sim': [11.7500, 7.7500, 12.0296],
    'PMA-Self': [60.5245, 4.5556, 6.4560],
    'PMA-Core': [52.8641, 9.7027, 6.2364],
    'PMA': [55.5432, 10.4940, 5.6877]
}

failure_se = {
    'Human': [0.0, 0.0, 0.0],
    'Base-Agent': [0.3845, 0.9164, 0.5611],
    'PMA-Affect': [1.0495, 0.3708, 0.2916],
    'PMA-Sim': [0.4704, 0.2048, 0.6685],
    'PMA-Self': [1.0311, 0.3344, 0.3817],
    'PMA-Core': [1.0326, 0.4065, 0.2975],
    'PMA': [0.7574, 0.6149, 0.4481]
}

# ---------- Avoidance rate ----------
avoid_mean = {
    'Human': [30.0, 8.0, 8.0],     # estimated from your current figure
    'Base-Agent': [0.0000, 0.0000, 5.0278],
    'PMA-Affect': [24.8889, 0.0000, 4.0278],
    'PMA-Sim': [0.0000, 0.0000, 14.3333],
    'PMA-Self': [18.6389, 0.0000, 7.1944],
    'PMA-Core': [22.3333, 3.2778, 7.3889],
    'PMA': [27.1944, 6.2222, 5.6389]
}

avoid_se = {
    'Human': [0.0, 0.0, 0.0],
    'Base-Agent': [0.0000, 0.0000, 0.2634],
    'PMA-Affect': [0.5041, 0.0000, 0.3568],
    'PMA-Sim': [0.0000, 0.0000, 0.6364],
    'PMA-Self': [0.6631, 0.0000, 0.4150],
    'PMA-Core': [0.8979, 0.2372, 0.2350],
    'PMA': [0.7938, 0.3395, 0.3951]
}

# =========================================================
# 2. p-values for E vs NE (within the same framework)
#    These stars will be placed above the NE bar
# =========================================================

failure_p = {
    'Human': np.nan,
    'Base-Agent': 0.9999998,
    'PMA-Affect': 1.962443e-19,
    'PMA-Sim': 1.764286e-07,
    'PMA-Self': 2.550287e-21,
    'PMA-Core': 4.007818e-19,
    'PMA': 1.878884e-20
}

avoid_p = {
    'Human': np.nan,
    'Base-Agent': np.nan,
    'PMA-Affect': 5.682723e-21,
    'PMA-Sim': np.nan,
    'PMA-Self': 1.265172e-16,
    'PMA-Core': 3.094510e-14,
    'PMA': 1.638428e-15
}

# =========================================================
# 3. Helper functions
# =========================================================

def p_to_star(p, show_ns=False):
    if np.isnan(p):
        return ''
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'n.s.' if show_ns else ''

def plot_grouped_panel(
    ax,
    mean_dict,
    se_dict,
    p_dict,
    ylabel,
    ylim,
    panel_label,
    frameworks,
    groups,
    colors,
    show_ns=False
):
    n_groups = len(groups)          # E, NE, NP
    n_frameworks = len(frameworks)  # Human + model frameworks

    # centers of E / NE / NP groups
    group_centers = np.arange(n_groups) * 1.8

    # total width occupied by all bars within one group
    total_width = 1.35
    bar_width = total_width / n_frameworks

    # store x positions for later annotation
    x_positions = {fw: {} for fw in frameworks}

    # draw bars
    for i, fw in enumerate(frameworks):
        offset = (i - (n_frameworks - 1) / 2) * bar_width
        x = group_centers + offset
        means = mean_dict[fw]
        ses = se_dict[fw]

        ax.bar(
            x,
            means,
            width=bar_width * 0.92,
            yerr=ses,
            capsize=2,
            color=colors[fw],
            edgecolor='black',
            linewidth=0.5,
            zorder=3,
            label=fw
        )

        for g_idx, g in enumerate(groups):
            x_positions[fw][g] = x[g_idx]

    # annotate significance above the NE bar
    for fw in frameworks:
        star = p_to_star(p_dict[fw], show_ns=show_ns)
        if star == '':
            continue

        ne_x = x_positions[fw]['NE']
        ne_y = mean_dict[fw][1] + se_dict[fw][1]
        y_offset = (ylim[1] - ylim[0]) * 0.03

        ax.text(
            ne_x,
            ne_y + y_offset,
            star,
            ha='center',
            va='bottom',
            fontsize=8
        )

    # formatting
    ax.set_xticks(group_centers)
    ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linewidth=0.4, alpha=0.25, zorder=0)

    ax.set_title(panel_label, loc='left', fontweight='bold')

# =========================================================
# 4. Plot style
# =========================================================

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'axes.linewidth': 0.8
})

colors = {
    'Human': '#E76F51',
    'Base-Agent': '#E9C46A',
    'PMA-Affect': '#C9D97E',
    'PMA-Sim': '#7BC8A4',
    'PMA-Self': '#B07CC6',
    'PMA-Core': '#4C72B0',
    'PMA': '#D1495B'
}


# =========================================================
# 5. Create figure
# =========================================================

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), constrained_layout=True)

plot_grouped_panel(
    ax=axes[0],
    mean_dict=failure_mean,
    se_dict=failure_se,
    p_dict=failure_p,
    ylabel='Failure rate (%)',
    ylim=(0, 72),
    panel_label='a  Failure rate',
    frameworks=frameworks,
    groups=groups,
    colors=colors,
    show_ns=False   # set True if you want to show "n.s."
)

plot_grouped_panel(
    ax=axes[1],
    mean_dict=avoid_mean,
    se_dict=avoid_se,
    p_dict=avoid_p,
    ylabel='Avoidance rate (%)',
    ylim=(0, 38),
    panel_label='b  Avoidance rate',
    frameworks=frameworks,
    groups=groups,
    colors=colors,
    show_ns=False   # set True if you want to show "n.s."
)

# Legend
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='upper center',
    ncol=4,
    bbox_to_anchor=(0.5, 1.06),
    frameon=False
)

fig.suptitle(
    'Learned helplessness across E, NE and NP conditions',
    y=1.12,
    fontsize=11
)

# Optional caption-like note inside the figure
fig.text(
    0.5, -0.02,
    'Asterisks indicate the significance of the E-versus-NE comparison within the same framework.',
    ha='center',
    va='top',
    fontsize=8
)

# Save
#plt.savefig('learned_helplessness_grouped_by_condition_star_version.png', dpi=300, bbox_inches='tight')
#plt.savefig('learned_helplessness_grouped_by_condition_star_version.pdf', bbox_inches='tight')
plt.show()