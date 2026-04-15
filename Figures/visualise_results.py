"""
Run from the experiment working directory:
    python visualise_results.py
Saves all figures to results/figures/
"""

import json, os, warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator

warnings.filterwarnings("ignore")

# ── Global style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi":        300,
    "savefig.dpi":       300,
    "font.family":       "serif",
    "font.size":         9,
    "axes.titlesize":    10,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   8,
    "legend.framealpha": 0.9,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.25,
    "grid.linestyle":    "--",
})

# ── Models ────────────────────────────────────────────────────────────────────
MODELS = [
    "google/gemini-3-flash-preview",
    "anthropic/claude-opus-4.6",
    "openai/gpt-5.2-codex",
    "deepseek/deepseek-v3.2",
    "moonshotai/kimi-k2.5",
]
SHORT = {
    "google/gemini-3-flash-preview": "Gemini",
    "anthropic/claude-opus-4.6":     "Claude",
    "openai/gpt-5.2-codex":          "GPT",
    "deepseek/deepseek-v3.2":        "DeepSeek",
    "moonshotai/kimi-k2.5":          "Kimi",
}
MODEL_LABELS = [SHORT[m] for m in MODELS]

FIGDIR = "results/figures"
os.makedirs(FIGDIR, exist_ok=True)

# ── Muted condition palettes (ColorBrewer-inspired) ───────────────────────────
# Each experiment defines its own palette keyed by condition name
PALETTES = {
    # 2-condition: muted teal / muted coral
    2: ["#6baed6", "#fd8d3c"],
    # 3-condition: muted blue / muted green / muted orange
    3: ["#74a9cf", "#78c679", "#fd8d3c"],
    # 4-condition
    4: ["#74a9cf", "#78c679", "#fd8d3c", "#9e9ac8"],
    # 5-condition
    5: ["#74a9cf", "#41b6c4", "#78c679", "#fd8d3c", "#f768a1"],
}

def palette(conditions):
    n = len(conditions)
    cols = PALETTES.get(n, PALETTES[5][:n])
    return {c: cols[i] for i, c in enumerate(conditions)}

def load(filename):
    path = os.path.join("results", filename)
    if not os.path.exists(path):
        print(f"  [skip] {filename} not found")
        return None
    return json.load(open(path, encoding="utf-8"))

def save_fig(fig, name):
    path = os.path.join(FIGDIR, name)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved → {path}")

def legend_handles(conditions, pal):
    return [mpatches.Patch(color=pal[c], label=c, alpha=0.8) for c in conditions]

def draw_boxes(ax, data, conditions, pal):
    """
    data: {condition: {model: [values]}}
    X positions: model groups, boxes within group = conditions
    """
    n_cond    = len(conditions)
    n_models  = len(MODELS)
    group_gap = 1.0
    box_w     = 0.12
    spacing   = box_w + 0.03
    total_w   = n_cond * spacing
    offsets   = np.linspace(-total_w/2 + spacing/2,
                             total_w/2 - spacing/2, n_cond)
    group_centres = np.arange(n_models) * group_gap

    for mi, model in enumerate(MODELS):
        for ci, cond in enumerate(conditions):
            vals = [v for v in data.get(cond, {}).get(model, [])
                    if v is not None]
            if not vals:
                continue
            x = group_centres[mi] + offsets[ci]
            ax.boxplot(
                vals,
                positions=[x],
                widths=box_w * 0.88,
                patch_artist=True,
                showfliers=False,
                medianprops=dict(color="black", linewidth=1.5),
                boxprops=dict(facecolor=pal[cond], alpha=0.78, linewidth=0.7),
                whiskerprops=dict(color="#444444", linewidth=0.7),
                capprops=dict(color="#444444", linewidth=0.7),
                flierprops=dict(marker="o", markerfacecolor=pal[cond],
                                markeredgecolor="none", alpha=0.45, markersize=2.5),
            )

    ax.set_xticks(group_centres)
    ax.set_xticklabels(MODEL_LABELS)
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# ARANDA 2005
# ══════════════════════════════════════════════════════════════════════════════
print("\nAranda 2005...")
aranda = load("aranda2005_results.json")
if aranda:
    conditions = ["control", "low", "high"]
    cond_labels = {"control": "Control", "low": "Low Anchor", "high": "High Anchor"}
    pal = palette(conditions)

    data = {cond: {} for cond in conditions}
    for model in MODELS:
        mdata = aranda.get(model, {})
        for cond in conditions:
            vals = [
                v.get("months")
                for k, v in mdata.items()
                if k.endswith(f"_{cond}") and not k.startswith("aranda_")
                and v.get("months") is not None
            ]
            data[cond][model] = vals

    fig, ax = plt.subplots(figsize=(7, 4.5))
    draw_boxes(ax, data, conditions, pal)
    ax.set_ylabel("Estimated Duration (months)")
    ax.set_title("Aranda & Easterbrook (2005) — Anchoring Effect\n"
                 "(distribution over 34 TAWOS projects)")
    ax.legend(handles=[mpatches.Patch(color=pal[c], label=cond_labels[c], alpha=0.8)
                       for c in conditions], loc="upper right")
    save_fig(fig, "aranda2005_anchoring.png")


# ══════════════════════════════════════════════════════════════════════════════
# LØHRE 2014
# ══════════════════════════════════════════════════════════════════════════════
print("\nLøhre 2014...")
lohre = load("lohre2014_results.json")
if lohre:
    exp_configs = {
        "exp1": {
            "title":      "Experiment 1 — High Anchor (~1000h)",
            "conditions": ["control", "precise_single", "round_single",
                           "precise_interval", "imprecise_interval"],
            "labels":     {"control": "Control", "precise_single": "Precise Single",
                           "round_single": "Round Single", "precise_interval": "Precise Interval",
                           "imprecise_interval": "Imprecise Interval"},
            "filename":   "lohre2014_exp1.png",
            "figsize":    (8.5, 4.5),
        },
        "exp2": {
            "title":      "Experiment 2 — Low Anchor (~20h)",
            "conditions": ["control", "precise_interval", "imprecise_interval"],
            "labels":     {"control": "Control", "precise_interval": "Precise Interval",
                           "imprecise_interval": "Imprecise Interval"},
            "filename":   "lohre2014_exp2.png",
            "figsize":    (7, 4.5),
        },
        "exp3": {
            "title":      "Experiment 3 — Source Credibility (Anchor: 10h)",
            "conditions": ["control", "low_credibility", "neutral", "high_credibility"],
            "labels":     {"control": "Control", "low_credibility": "Low Credibility",
                           "neutral": "Neutral", "high_credibility": "High Credibility"},
            "filename":   "lohre2014_exp3.png",
            "figsize":    (8, 4.5),
        },
    }

    for exp_key, cfg in exp_configs.items():
        exp_data = lohre.get(exp_key, {})
        conditions = cfg["conditions"]
        pal = palette(conditions)

        data = {cond: {} for cond in conditions}
        for model in MODELS:
            for cond in conditions:
                vals = [
                    doc_data.get(cond, {}).get("most_likely")
                    for doc_data in exp_data.get(model, {}).values()
                    if doc_data.get(cond, {}) and
                       doc_data[cond].get("most_likely") is not None
                ]
                data[cond][model] = [v for v in vals if v is not None]

        fig, ax = plt.subplots(figsize=cfg["figsize"])
        draw_boxes(ax, data, conditions, pal)
        ax.set_ylabel("Most Likely Estimate (work-hours)")
        ax.set_title(f"Løhre & Jørgensen (2014) — {cfg['title']}\n"
                     "(distribution over project briefs)")
        ax.legend(handles=[mpatches.Patch(color=pal[c], label=cfg["labels"][c], alpha=0.8)
                           for c in conditions], loc="upper right",
                  ncol=2 if len(conditions) > 3 else 1)
        save_fig(fig, cfg["filename"])


# ══════════════════════════════════════════════════════════════════════════════
# CONNOLLY 1997
# ══════════════════════════════════════════════════════════════════════════════
print("\nConnolly 1997...")
s1 = load("connolly1997_study1_results.json")
s2 = load("connolly1997_study2_results.json")

def connolly_extract(study_data, conditions, metric):
    """Extract per-model lists of metric values across all pairs."""
    out = {cond: {} for cond in conditions}
    for cond in conditions:
        for model in MODELS:
            vals = []
            for pair_data in study_data.get(cond, {}).get(model, {}).values():
                for est in pair_data.values():
                    if not est:
                        continue
                    if metric == "pi_width":
                        f = est.get("whole_fractiles", {})
                        p01, p50, p99 = f.get("p01"), f.get("p50"), f.get("p99")
                        if p01 and p50 and p99 and p50 > 0:
                            vals.append((p99 - p01) / p50)
                    elif metric == "gap":
                        g = est.get("gap")
                        if g is not None:
                            vals.append(g)
                    elif metric == "whole_p50":
                        v = est.get("whole_p50")
                        if v:
                            vals.append(v)
            out[cond][model] = vals
    return out

# PI width — Study 1 and Study 2 as separate figures
for study_data, study_label, conditions, fname in [
    (s1, "Study 1", ["A","B","C","D"], "connolly1997_pi_width_study1.png"),
    (s2, "Study 2 — Extreme Limits", ["A","B"], "connolly1997_pi_width_study2.png"),
]:
    if not study_data:
        continue
    cond_labels = {
        "A": "A: GT wording, whole first",
        "B": "B: GT wording, subtasks first",
        "C": "C: LT wording, whole first",
        "D": "D: LT wording, subtasks first",
    }
    pal = palette(conditions)
    data = connolly_extract(study_data, conditions, "pi_width")

    fig, ax = plt.subplots(figsize=(7.5 if len(conditions) == 4 else 6, 4.5))
    draw_boxes(ax, data, conditions, pal)
    ax.set_ylabel("Relative PI Width  (p99 − p01) / p50")
    ax.set_title(f"Connolly & Dean (1997) — PI Width ({study_label})\n"
                 "(distribution over task pairs)")
    ax.legend(handles=[mpatches.Patch(color=pal[c], label=cond_labels[c], alpha=0.8)
                       for c in conditions], loc="upper right")
    save_fig(fig, fname)

# Subtask gap — Study 1 only
if s1:
    conditions = ["A","B","C","D"]
    pal  = palette(conditions)
    data = connolly_extract(s1, conditions, "gap")

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # Replace all-zero distributions with a tiny epsilon so collapsed boxes
    # remain visible as a line (genuinely zero gap is a real result, not missing data)
    EPS = 0.01
    for cond in conditions:
        for model in MODELS:
            vals = data[cond].get(model, [])
            if vals and all(abs(v) < EPS for v in vals):
                data[cond][model] = [EPS if i % 2 == 0 else -EPS for i in range(len(vals))]
    draw_boxes(ax, data, conditions, pal)
    ax.axhline(0, color="black", linewidth=0.9, linestyle="--", alpha=0.5, zorder=0)
    ax.set_ylabel("Subtask Sum − Whole Estimate (hours)")
    ax.set_title("Connolly & Dean (1997) — Subtask Additive Bias (Study 1)\n"
                 "Positive = subtask sum exceeds holistic estimate")
    COND_LABELS_S1 = {
        "A": "A: GT wording, whole first",
        "B": "B: GT wording, subtasks first",
        "C": "C: LT wording, whole first",
        "D": "D: LT wording, subtasks first",
    }
    ax.legend(handles=[mpatches.Patch(color=pal[c], label=COND_LABELS_S1[c], alpha=0.8)
                       for c in conditions], loc="upper right")
    save_fig(fig, "connolly1997_subtask_gap.png")

# Whole p50 — Study 1 and Study 2
for study_data, study_label, conditions, fname in [
    (s1, "Study 1", ["A","B","C","D"], "connolly1997_whole_p50_study1.png"),
    (s2, "Study 2", ["A","B"],         "connolly1997_whole_p50_study2.png"),
]:
    if not study_data:
        continue
    pal  = palette(conditions)
    data = connolly_extract(study_data, conditions, "whole_p50")

    fig, ax = plt.subplots(figsize=(7.5 if len(conditions) == 4 else 6, 4.5))
    draw_boxes(ax, data, conditions, pal)
    ax.set_ylabel("Whole-Task Median Estimate p50 (hours)")
    ax.set_title(f"Connolly & Dean (1997) — Whole-Task Estimates ({study_label})\n"
                 "(distribution over task pairs)")
    COND_LABELS_S1 = {
        "A": "A: GT wording, whole first",
        "B": "B: GT wording, subtasks first",
        "C": "C: LT wording, whole first",
        "D": "D: LT wording, subtasks first",
    }
    ax.legend(handles=[mpatches.Patch(color=pal[c], label=COND_LABELS_S1.get(c, f"Condition {c}"), alpha=0.8)
                       for c in conditions], loc="upper right")
    save_fig(fig, fname)


# ══════════════════════════════════════════════════════════════════════════════
# JØRGENSEN 2002
# ══════════════════════════════════════════════════════════════════════════════
print("\nJørgensen 2002...")
j2_a = load("jorgensen2002_study_a_results.json")
j2_b = load("jorgensen2002_study_b_results.json")
j2_c = load("jorgensen2002_study_c_results.json")
j2_d = load("jorgensen2002_study_d_results.json")

# Study A — PI widths, one box per model
if j2_a:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    col = PALETTES[2][0]   # single condition — one muted colour
    for mi, model in enumerate(MODELS):
        vals = [v.get("pi_width") for v in j2_a.get(model, {}).values()
                if v and v.get("pi_width") is not None]
        if not vals:
            continue
        ax.boxplot(
            vals, positions=[mi], widths=0.45,
            patch_artist=True, showfliers=False,
            medianprops=dict(color="black", linewidth=1.5),
            boxprops=dict(facecolor=col, alpha=0.78, linewidth=0.7),
            whiskerprops=dict(color="#444444", linewidth=0.7),
            capprops=dict(color="#444444", linewidth=0.7),
            flierprops=dict(marker="o", markerfacecolor=col,
                            markeredgecolor="none", alpha=0.45, markersize=2.5),
        )
    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels(MODEL_LABELS)
    ax.set_ylabel("Relative PI Width  (max − min) / most_likely")
    ax.set_title("Jørgensen et al. (2002) — Study A\n90% Prediction Interval Widths")
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    save_fig(fig, "jorgensen2002_study_a_pi_width.png")

# Study B — role estimates
if j2_b:
    ROLES = ["EM", "PM", "UD", "DEV", "GROUP"]
    role_labels = {"EM": "Eng. Manager", "PM": "Project Manager",
                   "UD": "UX Designer", "DEV": "Developer",
                   "GROUP": "Group Consensus"}
    pal = palette(ROLES)

    data = {role: {} for role in ROLES}
    for role in ROLES:
        for model in MODELS:
            vals = [
                doc_data[role]["most_likely"]
                for doc_data in j2_b.get(model, {}).values()
                if role in doc_data and doc_data[role].get("most_likely")
            ]
            data[role][model] = vals

    fig, ax = plt.subplots(figsize=(9, 4.5))
    draw_boxes(ax, data, ROLES, pal)

    ax.set_ylabel("Most Likely Estimate (work-hours)")
    ax.set_title("Jørgensen et al. (2002) — Study B\n"
                 "Role-Based Individual vs Group Consensus Estimates")
    ax.legend(handles=[mpatches.Patch(color=pal[r], label=role_labels[r], alpha=0.8)
                       for r in ROLES], loc="upper right", ncol=2)
    save_fig(fig, "jorgensen2002_study_b_roles.png")

# Study C — PI width vs confidence level (line plot, one line per model)
if j2_c:
    confidence_levels = [50, 75, 90, 99]
    MODEL_COLOURS = {
        "google/gemini-3-flash-preview": "#fbbc04",
        "anthropic/claude-opus-4.6":     "#d97757",
        "openai/gpt-5.2-codex":          "#74aa9c",
        "deepseek/deepseek-v3.2":        "#4d8ef0",
        "moonshotai/kimi-k2.5":          "#9b59b6",
    }
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    for model in MODELS:
        medians, q25s, q75s = [], [], []
        for conf in confidence_levels:
            vals = [
                doc_data.get(str(conf), {}).get("pi_width")
                for doc_data in j2_c.get(model, {}).values()
                if doc_data.get(str(conf)) and doc_data[str(conf)].get("pi_width") is not None
            ]
            vals = [v for v in vals if v is not None]
            if vals:
                medians.append(float(np.median(vals)))
                q25s.append(float(np.percentile(vals, 25)))
                q75s.append(float(np.percentile(vals, 75)))
            else:
                medians.append(None); q25s.append(None); q75s.append(None)

        col = MODEL_COLOURS[model]
        ax.plot(confidence_levels, medians, "o-", color=col,
                label=SHORT[model], linewidth=1.8, markersize=5, zorder=3)
        valid = [(x, lo, hi) for x, lo, hi in zip(confidence_levels, q25s, q75s)
                 if lo is not None]
        if valid:
            xv, lov, hiv = zip(*valid)
            ax.fill_between(xv, lov, hiv, color=col, alpha=0.12)

    ax.set_xlabel("Confidence Level (%)")
    ax.set_ylabel("Relative PI Width  (max − min) / most_likely")
    ax.set_xticks(confidence_levels)
    ax.set_title("Jørgensen et al. (2002) — Study C\n"
                 "PI Width Sensitivity to Confidence Level\n"
                 "(median ± IQR ribbon over project briefs)")
    MODEL_COLOURS_LOCAL = {
        "google/gemini-3-flash-preview": "#fbbc04",
        "anthropic/claude-opus-4.6":     "#d97757",
        "openai/gpt-5.2-codex":          "#74aa9c",
        "deepseek/deepseek-v3.2":        "#4d8ef0",
        "moonshotai/kimi-k2.5":          "#9b59b6",
    }
    SHORT_LOCAL = {
        "google/gemini-3-flash-preview": "Gemini",
        "anthropic/claude-opus-4.6":     "Claude",
        "openai/gpt-5.2-codex":          "GPT",
        "deepseek/deepseek-v3.2":        "DeepSeek",
        "moonshotai/kimi-k2.5":          "Kimi",
    }
    ax.legend(handles=[mpatches.Patch(color=MODEL_COLOURS_LOCAL[m],
                                      label=SHORT_LOCAL[m], alpha=0.85)
                       for m in MODELS], ncol=1)
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    save_fig(fig, "jorgensen2002_study_c_pi_sensitivity.png")

# Study D — ego-free vs Study A, side by side per model
if j2_d and j2_a:
    conditions  = ["Study A", "Study D"]
    cond_labels = {"Study A": "Standard (Study A)", "Study D": "Ego-Free (Study D)"}
    pal = palette(conditions)

    data = {"Study A": {}, "Study D": {}}
    for model in MODELS:
        data["Study A"][model] = [
            v.get("pi_width") for v in j2_a.get(model, {}).values()
            if v and v.get("pi_width") is not None
        ]
        data["Study D"][model] = [
            v.get("pi_width") for v in j2_d.get(model, {}).values()
            if v and v.get("pi_width") is not None
        ]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    draw_boxes(ax, data, conditions, pal)
    ax.set_ylabel("Relative PI Width  (max − min) / most_likely")
    ax.set_title("Jørgensen et al. (2002) — Study D\n"
                 "Ego-Free vs Standard 90% PI Widths")
    ax.legend(handles=[mpatches.Patch(color=pal[c], label=cond_labels[c], alpha=0.8)
                       for c in conditions], loc="upper right")
    save_fig(fig, "jorgensen2002_study_d_ego_free.png")


# ══════════════════════════════════════════════════════════════════════════════
# JØRGENSEN 2009 — Four experiments, each as a two-panel figure
# ══════════════════════════════════════════════════════════════════════════════
print("\nJørgensen 2009...")
j2009 = load("jorgensen2009_results.json")
if j2009:
    exp_titles = {
        "exp_a": "Experiment A — 3 Risks vs As Many as Possible",
        "exp_b": "Experiment B — 1 Risk vs Structured Retrospective",
        "exp_c": "Experiment C — 1 Risk vs Probability/Severity Table",
        "exp_d": "Experiment D — Colleague Framing",
    }
    conditions  = ["LESS", "MORE"]
    cond_labels = {"LESS": "LESS (fewer risks)", "MORE": "MORE (more risks)"}
    pal = palette(conditions)

    for exp_key, exp_title in exp_titles.items():
        exp_data = j2009.get(exp_key)
        if not exp_data:
            continue

        fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))

        for ax, metric, ylabel, panel_title in [
            (axes[0], "effort",  "Most Likely Effort (work-hours)", "Effort Estimate"),
            (axes[1], "success", "Success Confidence (%)",          "Success Confidence"),
        ]:
            data = {cond: {} for cond in conditions}
            for cond in conditions:
                for model in MODELS:
                    vals = [
                        v.get(metric)
                        for v in exp_data.get(cond, {}).get(model, {}).values()
                        if v and v.get(metric) is not None
                    ]
                    data[cond][model] = vals

            n_cond   = len(conditions)
            box_w    = 0.12
            spacing  = box_w + 0.03
            total_w  = n_cond * spacing
            offsets  = np.linspace(-total_w/2 + spacing/2,
                                    total_w/2 - spacing/2, n_cond)
            group_centres = np.arange(len(MODELS))

            for mi, model in enumerate(MODELS):
                for ci, cond in enumerate(conditions):
                    vals = [v for v in data[cond].get(model, []) if v is not None]
                    if not vals:
                        continue
                    x = group_centres[mi] + offsets[ci]
                    ax.boxplot(
                        vals, positions=[x], widths=box_w*0.88,
                        patch_artist=True, showfliers=False,
                        medianprops=dict(color="black", linewidth=1.5),
                        boxprops=dict(facecolor=pal[cond], alpha=0.78, linewidth=0.7),
                        whiskerprops=dict(color="#444444", linewidth=0.7),
                        capprops=dict(color="#444444", linewidth=0.7),
                        flierprops=dict(marker="o", markerfacecolor=pal[cond],
                                        markeredgecolor="none", alpha=0.45, markersize=2.5),
                    )

            ax.set_xticks(group_centres)
            ax.set_xticklabels(MODEL_LABELS)
            ax.set_ylabel(ylabel)
            ax.set_title(panel_title)
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

        axes[0].legend(
            handles=[mpatches.Patch(color=pal[c], label=cond_labels[c], alpha=0.8)
                     for c in conditions],
            loc="upper right"
        )
        fig.suptitle(f"Jørgensen (2009) — {exp_title}\n"
                     "(distribution over project documents)", y=1.01)
        fig.tight_layout()
        save_fig(fig, f"jorgensen2009_{exp_key}.png")


# ══════════════════════════════════════════════════════════════════════════════
# MOLØKKEN 2003
# ══════════════════════════════════════════════════════════════════════════════
print("\nMoløkken & Jørgensen 2003...")
mol = load("molokken2003_results.json")
if mol:
    phases = ["before", "group", "after"]
    phase_labels = {"before": "Individual (Before)",
                    "group":  "Group Consensus",
                    "after":  "Individual (After)"}
    pal = palette(phases)

    # Box plot
    data = {p: {} for p in phases}
    for phase in phases:
        key = "avg_before" if phase == "before" else \
              "group"      if phase == "group"  else "avg_after"
        for model in MODELS:
            vals = [
                d.get(key) for d in mol.get(model, {}).values()
                if d.get(key) is not None
            ]
            data[phase][model] = vals

    fig, ax = plt.subplots(figsize=(7, 4.5))
    draw_boxes(ax, data, phases, pal)
    ax.set_ylabel("Effort Estimate (work-hours)")
    ax.set_title("Moløkken & Jørgensen (2003) — Before / Group / After\n"
                 "(distribution over full-specification projects)")
    ax.legend(handles=[mpatches.Patch(color=pal[p], label=phase_labels[p], alpha=0.8)
                       for p in phases], loc="upper right")
    save_fig(fig, "molokken2003_boxplot.png")




# ══════════════════════════════════════════════════════════════════════════════
# HAUGEN 2006
# ══════════════════════════════════════════════════════════════════════════════
print("\nHaugen 2006...")
haugen = load("haugen2006_results.json")
if haugen:
    conditions  = ["unstructured", "planning_poker"]
    cond_labels = {"unstructured": "Unstructured", "planning_poker": "Planning Poker"}
    pal = palette(conditions)

    for metric, ylabel, title_suffix, fname_suffix in [
        ("group",       "Group Consensus Estimate (pair-days)",
         "Group Consensus Estimates",    "group_consensus"),
        ("indiv_stdev", "Std Dev of Individual Estimates (pair-days)",
         "Individual Estimate Variance", "individual_variance"),
    ]:
        data = {cond: {} for cond in conditions}
        for cond in conditions:
            for model in MODELS:
                vals = []
                for pair_data in haugen.get(model, {}).values():
                    for entry in pair_data.get(cond, []):
                        if metric == "group":
                            if entry.get("group") is not None:
                                vals.append(entry["group"])
                        else:
                            indivs = [v for v in entry.get("individual", {}).values()
                                      if v is not None]
                            if len(indivs) > 1:
                                vals.append(float(np.std(indivs, ddof=1)))
                data[cond][model] = vals

        fig, ax = plt.subplots(figsize=(6, 4.5))
        draw_boxes(ax, data, conditions, pal)
        ax.set_ylabel(ylabel)
        ax.set_title(f"Haugen (2006) — {title_suffix}\n"
                     "(distribution over user story files)")
        ax.legend(handles=[mpatches.Patch(color=pal[c], label=cond_labels[c], alpha=0.8)
                           for c in conditions], loc="upper right")
        save_fig(fig, f"haugen2006_{fname_suffix}.png")

print(f"\nAll figures saved to {FIGDIR}/")
