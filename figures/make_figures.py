"""Regenerates every figure used in the article and slides.

Run from the repo root:  python figures/make_figures.py
All figures are drawn from scratch with matplotlib. Data lives in figures/data/*.csv
(transcribed from the tables of the surveyed papers). PNGs are written to article/images/.
"""
import csv
import os
from statistics import median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "..", "article", "images")
os.makedirs(OUT, exist_ok=True)
DPI = 200

# ---- colorblind-safe palette (Okabe-Ito subset) ----
AGENTIC = "#0072B2"      # blue
PLAIN = "#E69F00"        # orange
GREEN = "#009E73"
PINK = "#CC79A7"
SKY = "#56B4E9"
VERM = "#D55E00"
INK = "#1f2933"
MUTED = "#5f6b7a"
LIGHT = "#eef1f5"
LINE = "#8a94a3"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": LINE,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "hatch.linewidth": 1.1,
})


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", os.path.relpath(path))


def title(fig, text, sub=None, y=0.995):
    fig.text(0.01, y, text, fontsize=13.5, fontweight="bold", ha="left", va="top")
    if sub:
        fig.text(0.01, y - 0.045, sub, fontsize=10, color=MUTED, ha="left", va="top")


def source(fig, text, y=0.005):
    fig.text(0.01, y, text, fontsize=8, color=MUTED, ha="left", va="bottom")


# ---------- drawing helpers for diagrams ----------
def rbox(ax, x, y, w, h, text, fc="white", ec=INK, fs=9.5, bold=False, lw=1.3, tc=INK,
         ls="-", rs=1.2, z=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rs}",
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, zorder=z + 1, linespacing=1.25)
    return p


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.6, both=False, rad=0.0, ls="-", z=2):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>" if both else "-|>",
                        mutation_scale=12, color=color, lw=lw, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0)
    ax.add_patch(a)


def canvas(w_in, h_in, xmax=100, ymax=60):
    fig = plt.figure(figsize=(w_in, h_in))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    return fig, ax


# =====================================================================
# Figure 1: LLM-as-a-Judge vs Agent-as-a-Judge
# =====================================================================
def fig1():
    fig, ax = canvas(9, 5.6, 100, 62)
    ax.text(1, 60.5, "From a passive judge to an active one", fontsize=13.5, fontweight="bold", va="top")
    # panel backgrounds
    ax.add_patch(FancyBboxPatch((1, 4), 37, 49, boxstyle="round,pad=0,rounding_size=1.5",
                                fc=LIGHT, ec="none", zorder=0))
    ax.add_patch(FancyBboxPatch((40.5, 4), 58.5, 49, boxstyle="round,pad=0,rounding_size=1.5",
                                fc="#e8f1f8", ec="none", zorder=0))
    ax.text(2.5, 51, "(a) LLM-as-a-Judge: passive", fontsize=10.5, fontweight="bold", va="top", color=INK)
    ax.text(42, 51, "(b) Agent-as-a-Judge: active", fontsize=10.5, fontweight="bold", va="top", color=AGENTIC)

    # (a)
    rbox(ax, 4, 36, 31, 9, "Evaluand + supplied context\n(response, rubric, reference)", fc="white", fs=9)
    arrow(ax, 19.5, 36, 19.5, 30.5)
    rbox(ax, 4, 20.5, 31, 10, "LLM judge\nreads once, answers from\nits own knowledge", fc="#fdf0d0", ec=PLAIN, fs=9)
    arrow(ax, 19.5, 20.5, 19.5, 15.5)
    rbox(ax, 4, 7, 31, 8.5, "Score / preference / critique", fc="white", fs=9)
    ax.text(19.5, 5.2, "Unrecorded state and outside facts stay unknown", fontsize=7.6, ha="center",
            color=MUTED, style="italic")

    # (b)
    rbox(ax, 42, 38, 15, 8, "Evaluand\n+ context", fc="white", fs=9)
    rbox(ax, 62, 38, 18, 8, "Peer judges\n(multi-agent)", fc="white", ec=GREEN, fs=9, tc=INK)
    rbox(ax, 84, 38, 13.5, 8, "Environment\nweb, files, code", fc="white", ec=VERM, fs=8.6)
    rbox(ax, 42, 22, 15, 10, "Plan\nwhat to check,\nhow to check", fc="white", ec=PINK, fs=8.8)
    rbox(ax, 62, 20, 18, 14, "Judge agent\nkeeps an evaluation\nstate and decides\nwhat to do next", fc="#cfe3f3",
         ec=AGENTIC, fs=9, bold=True)
    rbox(ax, 84, 22, 13.5, 10, "Tools\nrun code, search,\ninspect images", fc="white", ec=VERM, fs=8.6)
    rbox(ax, 62, 7, 18, 8.5, "Memory\nfindings, artifacts", fc="white", ec=SKY, fs=9)
    rbox(ax, 84, 7, 13.5, 8.5, "Grounded\nverdict +\nevidence trail", fc="white", fs=8.2, bold=True)
    arrow(ax, 57, 42, 62, 29, AGENTIC, rad=0.0)          # evaluand -> agent
    arrow(ax, 57.5, 27, 62, 27, PINK, both=True)           # plan
    arrow(ax, 71, 34, 71, 38, GREEN, both=True)            # peers
    arrow(ax, 80, 27, 84, 27, VERM, both=True)             # tools
    arrow(ax, 90.7, 32, 90.7, 38, VERM, both=True)         # tools <-> env
    arrow(ax, 71, 20, 71, 15.5, SKY, both=True)            # memory
    arrow(ax, 80, 20.5, 84, 13.5, INK)                     # verdict
    ax.text(42, 5.2, "Loop: act, observe, update, repeat until evidence suffices", fontsize=7.6,
            color=MUTED, style="italic")
    source(fig, "Original schematic by the author, after the concept described in You et al. (2026), Fig. 1.", y=0.0)
    save(fig, "fig1_llm_vs_agent_judge.png")


# =====================================================================
# Figure 2: taxonomy tree
# =====================================================================
def fig2():
    fig, ax = canvas(9, 8.6, 100, 100)
    ax.text(1, 98.5, "Taxonomy: four mechanisms of Agent-as-a-Judge", fontsize=13.5, fontweight="bold", va="top")
    groups = [
        ("Multi-agent\ncollaboration", GREEN, [
            ("Roles", "adversarial · perspective · analytical · verdict-control", "AgentsCourt, AgentsBench, GEMA-Score, MATEval"),
            ("Modes", "sequential · reciprocal · parallel", "CodeVisionary, CollabEval, AgentV-RL"),
        ]),
        ("Tool\nintegration", VERM, [
            ("Interfaces", "code execution · search · vision · solver · shell", "TIR-Judge, OpenReward, TIM-PRM"),
            ("Selection", "fixed-rule → evidence-triggered → observation-guided → active probing", "VerifiAgent, TALE, VAGEN"),
            ("Function", "knowledge expansion · evidence access · operational verification · trace-based", "DREAM, TaTToo, MATH-VF"),
        ]),
        ("Memory", SKY, [
            ("Stored", "process · artifact · experience", "TALE, ARM-Thinker, FACT-AUDIT"),
            ("Read", "carry-forward · condensed readout · selective retrieval", "GUI-PRA, Table-Critic"),
            ("Updated", "per step · on budget · on outcome", "TALE, GUI-PRA, FACT-AUDIT"),
        ]),
        ("Planning", PINK, [
            ("What to check", "case-specific protocol · rubric · sub-aspect", "DREAM, APRES, Evaluation Agent"),
            ("How to check", "route · claim-level · step-level · evidence-channel", "EvalPlanner, AgentV-RL, TIM-PRM"),
        ]),
    ]
    total = sum(len(g[2]) for g in groups)
    row_h = 92 / total
    rbox(ax, 1, 46 - 6, 13, 12, "Agent-as-\na-Judge", fc=AGENTIC, ec=AGENTIC, tc="white", fs=10.5, bold=True)
    y = 96
    for name, color, leaves in groups:
        gh = len(leaves) * row_h
        gy = y - gh / 2
        rbox(ax, 19, gy - 4.5, 15, 9, name, fc="white", ec=color, lw=2.2, fs=9.8, bold=True)
        arrow(ax, 14, 46, 19, gy, LINE, lw=1.3)
        for i, (lbl, items, ex) in enumerate(leaves):
            ly = y - (i + 0.5) * row_h
            arrow(ax, 34, gy, 38, ly, LINE, lw=1.1)
            rbox(ax, 38, ly - row_h / 2 + 0.9, 61, row_h - 1.8, "", fc="white", ec=color, lw=1.2, rs=1.0)
            ax.text(39.5, ly + 1.7, lbl, fontsize=9.2, fontweight="bold", color=INK, va="center", zorder=6)
            ax.text(39.5, ly - 0.5, items, fontsize=8.2, color=INK, va="center", zorder=6)
            ax.text(39.5, ly - 2.7, "e.g. " + ex, fontsize=7.6, color=MUTED, va="center", style="italic", zorder=6)
        y -= gh
    source(fig, "Original diagram after the taxonomy in You et al. (2026), Sec. 3. System names are as cited by the survey.", y=0.0)
    save(fig, "fig2_taxonomy.png")


# =====================================================================
# Figure 3: multi-agent collaboration modes
# =====================================================================
def fig3():
    fig, ax = canvas(9, 6.2, 100, 70)
    ax.text(1, 68.5, "Three ways judges collaborate", fontsize=13.5, fontweight="bold", va="top")
    roles = [("Adversarial", VERM), ("Perspective", PINK), ("Analytical", SKY), ("Verdict-control", GREEN)]
    ax.text(1, 62.5, "Role types:", fontsize=9, color=MUTED, va="center")
    x = 13
    for r, c in roles:
        ax.add_patch(FancyBboxPatch((x, 60.6), 3.2, 3.8, boxstyle="round,pad=0,rounding_size=0.8", fc=c, ec="none"))
        ax.text(x + 4.4, 62.5, r, fontsize=9, va="center")
        x += 6.5 + len(r) * 1.45
    cols = [(1, "Sequential"), (35, "Reciprocal"), (69, "Parallel")]
    for cx, name in cols:
        ax.add_patch(FancyBboxPatch((cx, 8), 30, 48, boxstyle="round,pad=0,rounding_size=1.5", fc=LIGHT, ec="none", zorder=0))
        ax.text(cx + 15, 53.5, name, fontsize=11, fontweight="bold", ha="center", va="center")

    # sequential: analytical -> adversarial -> verdict-control
    def node(x, y, t, c, w=11, h=6.5):
        rbox(ax, x, y, w, h, t, fc="white", ec=c, lw=2.2, fs=8.6)
    node(3, 41, "Extract\nevidence", SKY, 12)
    node(17, 41, "Argue\nfor / against", VERM, 12)
    node(10, 27, "Judge issues\nverdict", GREEN, 14)
    arrow(ax, 15, 44.2, 17, 44.2)
    arrow(ax, 23, 41, 20, 33.5)
    arrow(ax, 9, 41, 13.5, 33.5)
    ax.text(16, 20.5, "Each stage consumes the\nprevious stage's artifact", fontsize=8.6, ha="center", va="center", color=INK)
    ax.text(16, 13, "+ traceable    − upstream lock-in", fontsize=8.6, ha="center", color=MUTED, style="italic")

    # reciprocal: A <-> B, presiding judge
    node(38, 41, "Judge A\n(professional)", PINK, 11.5)
    node(53, 41, "Judge B\n(lay)", PINK, 11.5)
    arrow(ax, 49.5, 45.5, 53, 45.5, INK, both=True)
    arrow(ax, 53, 42.5, 49.5, 42.5, INK, both=False, rad=0.0, ls=(0, (2, 2)))
    node(45.5, 27, "Presiding judge\nchecks convergence", GREEN, 16)
    arrow(ax, 43.7, 41, 49, 33.5)
    arrow(ax, 58.7, 41, 54, 33.5)
    ax.text(50, 20.5, "Agents read each other's reasoning\nand revise until positions settle", fontsize=8.6, ha="center", va="center")
    ax.text(50, 13, "+ surfaces hidden assumptions\n− agreement can bury dissent", fontsize=8.6, ha="center", color=MUTED, style="italic", va="center")

    # parallel
    node(72, 44.5, "Verifier 1", SKY, 10, 5)
    node(72, 37.5, "Verifier 2", SKY, 10, 5)
    node(72, 30.5, "Verifier 3", SKY, 10, 5)
    rbox(ax, 87, 34.5, 11, 8.5, "Resolver\nvote · weights", fc="white", ec=GREEN, lw=2.2, fs=8.4)
    for yy in (47, 40, 33):
        arrow(ax, 82, yy, 87, 38.7)
    ax.text(84, 22.5, "Independent checks, then one\nresolver combines them", fontsize=8.6, ha="center", va="center")
    ax.text(84, 14, "+ reproducible aggregation\n− no cross-checking", fontsize=8.6, ha="center", color=MUTED, style="italic", va="center")

    ax.text(16, 5.2, "e.g. AgentsCourt, CodeVisionary", fontsize=8, ha="center", color=MUTED)
    ax.text(50, 5.2, "e.g. AgentsBench, CollabEval, HiMATE", fontsize=8, ha="center", color=MUTED)
    ax.text(84, 5.2, "e.g. AgentV-RL, Multi-Agent Verification", fontsize=8, ha="center", color=MUTED)
    source(fig, "Original schematic after You et al. (2026), Sec. 3.1. Example systems are as named in the survey.", y=0.0)
    save(fig, "fig3_collaboration_modes.png")


# =====================================================================
# Table 3 helpers
# =====================================================================
BENCHES = ["RewardBench", "RM-Bench", "JudgeBench"]


def table3():
    rows = read_csv("table3_reward_models.csv")
    for r in rows:
        for k in ("subset_1", "subset_2", "subset_3", "subset_4", "overall"):
            r[k] = float(r[k])
    return rows


# =====================================================================
# Figure 4: leaderboard bars
# =====================================================================
def fig4():
    rows = table3()
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 4.9), sharey=True)
    order = ["TIR-Judge", "Agentic Reward Model", "Multi-Agent Verification", "VerifiAgent", "Themis",
             "RRM", "RM-R1", "Think-RM"]
    labels = ["TIR-Judge", "Agentic Reward Model", "Multi-Agent Verification", "VerifiAgent", "Themis",
              "RRM", "RM-R1", "Think-RM"]
    for ax, b in zip(axes, BENCHES):
        sub = {r["method"]: r for r in rows if r["benchmark"] == b}
        for i, m in enumerate(order):
            r = sub[m]
            col = AGENTIC if r["category"] == "agentic" else PLAIN
            hatch = "////" if r["extracted_from_original"] == "no" else None
            ax.barh(i, r["overall"], color=col, edgecolor="white" if hatch else col, hatch=hatch,
                    height=0.68, linewidth=0)
            ax.text(r["overall"] + 1, i, f"{r['overall']:.1f}", va="center", fontsize=9)
        ax.set_xlim(0, 108)
        ax.set_title(b, fontsize=11, fontweight="bold", loc="left")
        ax.set_xlabel("Overall accuracy (%)")
        ax.grid(axis="x", color="#e3e7ec", lw=0.8)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(order)))
    axes[0].set_yticklabels(labels, fontsize=9)
    axes[0].invert_yaxis()
    handles = [Patch(fc=AGENTIC, label="Agentic judge"), Patch(fc=PLAIN, label="Non-agentic reasoning reward model"),
               Patch(fc="#b8c4cf", ec="white", hatch="////", label="Not extracted from the original paper's table\n(published elsewhere or reproduced by the survey authors)")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8.6, bbox_to_anchor=(0.5, -0.03))
    title(fig, "Does going agentic help? Reward-model benchmarks", y=1.02)
    fig.subplots_adjust(top=0.86, bottom=0.2, wspace=0.08, left=0.2)
    source(fig, "Data: You et al., 2026, Table 3 (overall column, percent). Chart drawn by the author.", y=-0.09)
    save(fig, "fig4_leaderboard_table3.png")


# =====================================================================
# Figure 5: uneven gains
# =====================================================================
def fig5():
    rows = table3()
    best_diff, med_diff, sub_diff, sub_names = {}, {}, {}, {}
    for b in BENCHES:
        sub = [r for r in rows if r["benchmark"] == b]
        ag = [r for r in sub if r["category"] == "agentic"]
        na = [r for r in sub if r["category"] != "agentic"]
        best_diff[b] = max(r["overall"] for r in ag) - max(r["overall"] for r in na)
        med_diff[b] = median(r["overall"] for r in ag) - median(r["overall"] for r in na)
        sub_names[b] = sub[0]["subset_names"].split("|")
        sub_diff[b] = [max(r[f"subset_{k}"] for r in ag) - max(r[f"subset_{k}"] for r in na) for k in (1, 2, 3, 4)]
    fig = plt.figure(figsize=(9.6, 4.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.1], wspace=0.28, left=0.07, right=0.98, top=0.86, bottom=0.14)
    ax = fig.add_subplot(gs[0])
    x = range(3)
    w = 0.36
    bv = [best_diff[b] for b in BENCHES]
    mv = [med_diff[b] for b in BENCHES]
    ax.bar([i - w / 2 for i in x], bv, w, color=AGENTIC, label="Best agentic vs best non-agentic")
    ax.bar([i + w / 2 for i in x], mv, w, color="#9bc4e0", edgecolor=AGENTIC, linewidth=1.0,
           label="Median agentic vs median non-agentic")
    for i in x:
        for off, v in ((-w / 2, bv[i]), (w / 2, mv[i])):
            ax.text(i + off, v + (0.6 if v >= 0 else -0.6), f"{v:+.1f}", ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=9)
    ax.axhline(0, color=INK, lw=1)
    ax.set_xticks(list(x))
    ax.set_xticklabels(BENCHES)
    ax.set_ylabel("Agentic minus non-agentic (points)")
    ax.set_ylim(-20, 22)
    ax.grid(axis="y", color="#e3e7ec", lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("(a) Overall score gap", loc="left", fontsize=10.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=8.2, loc="upper right")
    ax.text(-0.45, 14, "agentic ahead ↑", fontsize=8.4, color=AGENTIC, ha="left", va="top")
    ax.text(-0.45, -19, "plain ahead ↓", fontsize=8.4, color="#9a6a00", ha="left", va="bottom")

    ax2 = fig.add_subplot(gs[1])
    cmap = LinearSegmentedColormap.from_list("div", [PLAIN, "#eeeeee", AGENTIC])
    grid = [sub_diff[b] for b in BENCHES]
    im = ax2.imshow(grid, cmap=cmap, vmin=-12.5, vmax=12.5, aspect="auto")
    for i, b in enumerate(BENCHES):
        for j in range(4):
            v = grid[i][j]
            ax2.text(j, i - 0.12, sub_names[b][j], ha="center", va="center", fontsize=8.4, color=INK)
            ax2.text(j, i + 0.2, f"{v:+.1f}", ha="center", va="center", fontsize=10, fontweight="bold", color=INK)
    ax2.set_xticks([])
    ax2.set_yticks(range(3))
    ax2.set_yticklabels(BENCHES)
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.set_xticks([k - 0.5 for k in range(1, 4)], minor=True)
    ax2.set_yticks([k - 0.5 for k in range(1, 3)], minor=True)
    ax2.grid(which="minor", color="white", lw=3)
    ax2.tick_params(which="both", length=0)
    ax2.set_title("(b) Best-vs-best gap per subset (points)", loc="left", fontsize=10.5, fontweight="bold")
    cb = fig.colorbar(im, ax=ax2, fraction=0.04, pad=0.02)
    cb.set_label("orange = plain ahead · blue = agentic ahead", fontsize=8)
    cb.outline.set_visible(False)
    title(fig, "Uneven gains: agentic judges win some benchmarks and lose others", y=1.0)
    source(fig, "Gaps computed by the author from You et al., 2026, Table 3. 'Best' and 'median' are over the 5 agentic and 3 non-agentic rows.", y=0.0)
    save(fig, "fig5_uneven_gains.png")
    return best_diff, med_diff, sub_diff


# =====================================================================
# Figure 6: benchmark landscape table-figure
# =====================================================================
def fig6():
    rows = read_csv("table2_reward_benchmarks.csv")
    cols = [("Benchmark", 0.0, 0.17), ("Family", 0.17, 0.12), ("Form", 0.29, 0.1), ("Domain", 0.39, 0.28),
            ("Judgment signal", 0.67, 0.25), ("Items", 0.92, 0.08)]
    fam_col = {"reward-model": AGENTIC, "nlg": GREEN}
    form_col = {"pair-wise": "#d6e6f3", "point-wise": "#fbe7bd", "step-wise": "#e9d3e1"}
    n = len(rows)
    fig = plt.figure(figsize=(9.6, 0.38 * n + 1.8))
    ax = fig.add_axes([0.01, 0.06, 0.98, 0.86])
    ax.set_xlim(0, 1)
    ax.set_ylim(n + 0.4, -1.0)
    ax.axis("off")
    for name, x, w in cols:
        ax.text(x + 0.005, -0.6, name, fontsize=9.6, fontweight="bold", va="center")
    ax.plot([0, 1], [-0.15, -0.15], color=INK, lw=1.2)
    for i, r in enumerate(rows):
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0, i - 0.25), 1, 1, fc="#f6f8fa", ec="none", zorder=0))
        fam = "Reward model" if r["family"] == "reward-model" else "NLG eval"
        ax.text(0.005, i + 0.25, r["benchmark"], fontsize=9.2, fontweight="bold", va="center")
        ax.add_patch(plt.Rectangle((0.175, i - 0.2 + 0.25 - 0.1), 0.012, 0.5, fc=fam_col[r["family"]], ec="none"))
        ax.text(0.195, i + 0.25, fam, fontsize=8.8, va="center")
        ax.add_patch(FancyBboxPatch((0.292, i - 0.03), 0.085, 0.56, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc=form_col[r["evaluand_form"]], ec="none"))
        ax.text(0.3345, i + 0.25, r["evaluand_form"], fontsize=8.4, va="center", ha="center")
        ax.text(0.395, i + 0.25, r["domain"], fontsize=8.6, va="center")
        ax.text(0.675, i + 0.25, r["judgment_signal"], fontsize=8.6, va="center")
        ax.text(0.995, i + 0.25, f"{int(r['scale']):,}", fontsize=8.8, va="center", ha="right")
    ax.plot([0, 1], [n - 0.25, n - 0.25], color=LINE, lw=0.8)
    title(fig, "Benchmark landscape: what each one tests", y=0.995)
    source(fig, "Data: You et al., 2026, Tables 2 and 4 (benchmark metadata). 'Items' is the scale column in the paper. Table drawn by the author.", y=0.0)
    save(fig, "fig6_benchmark_landscape.png")


# =====================================================================
# Figure 7: cost vs reliability (conceptual)
# =====================================================================
def fig7():
    import numpy as np
    fig, ax = plt.subplots(figsize=(9, 5.2))
    x = np.linspace(0.3, 10, 300)
    # conceptual curves
    env = 38 + 52 * (1 - np.exp(-0.55 * (x - 0.3))) - 0.0 * x
    env = env - 1.6 * np.clip(x - 6.2, 0, None) ** 1.4
    open_ended = 72 + 10 * (1 - np.exp(-0.9 * (x - 0.3))) - 0.0 * x
    ax.plot(x, env, color=AGENTIC, lw=2.8)
    ax.plot(x, open_ended, color=PLAIN, lw=2.8, ls="--")
    ax.scatter([0.3], [env[0]], s=70, color=AGENTIC, zorder=5)
    ax.scatter([0.3], [open_ended[0]], s=70, color=PLAIN, zorder=5)
    ax.annotate("Plain LLM judge\n(one call)", (0.3, open_ended[0]), (0.55, 90), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=LINE), color=INK, va="center")
    ax.text(9.9, 62, "Tasks that depend on\nunseen evidence\n(code runs, state, facts)", color=AGENTIC,
            fontsize=9.4, fontweight="bold", ha="right", va="top")
    ax.text(9.9, 76, "Open-ended answers judged on\nwhat is already on the page", color="#9a6a00",
            fontsize=9.4, fontweight="bold", ha="right", va="top")
    ax.axvspan(2.2, 6.2, color="#e8f1f8", zorder=0)
    ax.text(4.2, 33, "worth it for evidence-\ndependent tasks", fontsize=8.8, ha="center", color=AGENTIC)
    ax.annotate("diminishing returns, then\nerrors compound across steps", (7.9, env[np.argmin(abs(x - 7.9))]),
                (6.6, 41), fontsize=8.6, color=MUTED, arrowprops=dict(arrowstyle="->", color=LINE))
    ax.set_xlim(0, 10)
    ax.set_ylim(28, 108)
    ax.set_xlabel("Evaluation effort per verdict  (calls, tools, agents, latency)  →")
    ax.set_ylabel("Reliability of the verdict  →")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.15, 107, "ILLUSTRATION ONLY: the author's conceptual sketch, not data from any paper", fontsize=8.6,
            fontweight="bold", color=VERM, va="top")
    ax.text(0.15, 102.5, "Real data point (Zhuge et al., 2024, DevAI): plain LLM judge 10.99 min, $29.63;\n"
                      "agentic judge 118.43 min, $30.58. Latency rose about 10x, dollars barely moved.",
            fontsize=8.2, color=MUTED, va="top")
    title(fig, "Cost vs reliability: when does extra checking pay off?", y=1.02)
    source(fig, "Conceptual sketch by the author (opinion). The DevAI numbers are from Zhuge et al., 2024, Sec. 4.4.", y=-0.05)
    save(fig, "fig7_cost_vs_reliability.png")


# =====================================================================
# Figure 8: original Agent-as-a-Judge (DevAI) results
# =====================================================================
def fig8():
    al = read_csv("devai_alignment.csv")
    ab = read_csv("devai_ablation.csv")
    fig = plt.figure(figsize=(9.6, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1], wspace=0.28, left=0.07, right=0.98, top=0.78, bottom=0.2)
    ax = fig.add_subplot(gs[0])
    agents = ["MetaGPT", "GPT-Pilot", "OpenHands"]
    keys = ["metagpt", "gpt_pilot", "openhands"]
    cfg = [("black-box", "LLM-as-a-Judge", PLAIN, None, "LLM judge, black-box"),
           ("black-box", "Agent-as-a-Judge", AGENTIC, None, "Agent judge, black-box"),
           ("gray-box", "LLM-as-a-Judge", PLAIN, "////", "LLM judge, gray-box"),
           ("gray-box", "Agent-as-a-Judge", AGENTIC, "////", "Agent judge, gray-box")]
    w = 0.16
    for j, (setting, judge, col, hatch, lab) in enumerate(cfg):
        row = next(r for r in al if r["setting"] == setting and r["judge"] == judge)
        vals = [float(row[k]) for k in keys]
        pos = [i + (j - 2) * w for i in range(3)]
        ax.bar(pos, vals, w * 0.92, color=col, edgecolor="white" if hatch else col, hatch=hatch, linewidth=0, label=lab)
        for p, v in zip(pos, vals):
            ax.text(p, v + 1, f"{v:.0f}", ha="center", fontsize=7.8)
    hum = next(r for r in al if r["setting"] == "reference")
    hv = [float(hum[k]) for k in keys]
    hp = [i + 2 * w for i in range(3)]
    ax.bar(hp, hv, w * 0.92, color="#7b8794", linewidth=0, label="Human majority vote")
    for p, v in zip(hp, hv):
        ax.text(p, v + 1, f"{v:.0f}", ha="center", fontsize=7.8)
    ax.set_xticks([i for i in range(3)])
    ax.set_xticklabels(["MetaGPT", "GPT-Pilot", "OpenHands"])
    ax.set_xlabel("Agent being judged")
    ax.set_ylabel("Agreement with human consensus (%)")
    ax.set_ylim(40, 108)
    ax.grid(axis="y", color="#e3e7ec", lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.6, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    ax.set_title("(a) Alignment rate on DevAI", loc="left", fontsize=10.5, fontweight="bold", pad=34)
    ax2 = fig.add_subplot(gs[1])
    labels = [r["components_added"] for r in ab]
    vals = [float(r["alignment_rate_pct"]) for r in ab]
    ax2.plot(range(len(vals)), vals, color=AGENTIC, lw=2.4, marker="o", ms=7)
    for i, v in enumerate(vals):
        ax2.text(i, v + 2, f"{v:.1f}", ha="center", fontsize=8.8)
    ax2.set_xticks(range(len(vals)))
    ax2.set_xticklabels(labels, fontsize=8.6)
    ax2.set_ylim(55, 100)
    ax2.set_ylabel("Alignment rate (%)")
    ax2.set_xlabel("Judge components, added cumulatively")
    ax2.grid(axis="y", color="#e3e7ec", lw=0.8)
    ax2.set_axisbelow(True)
    ax2.set_title("(b) Ablation, judging OpenHands", loc="left", fontsize=10.5, fontweight="bold", pad=34)
    title(fig, "The original Agent-as-a-Judge experiment (DevAI benchmark)", y=1.03)
    source(fig, "Data: Zhuge et al., 2024, Tables 3 and 4. Hatched bars = gray-box setting (manually collected trajectory data). Chart drawn by the author.", y=-0.01)
    save(fig, "fig8_devai_original_results.png")


# =====================================================================
# Figure 9: tool interfaces
# =====================================================================
def fig9():
    rows = read_csv("tool_interfaces.csv")
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    names = [r["interface"] for r in rows]
    cnt = [int(r["count"]) for r in rows]
    sh = [float(r["share_pct"]) for r in rows]
    ax.barh(range(len(rows)), cnt, color=VERM, height=0.66)
    for i, (c, s) in enumerate(zip(cnt, sh)):
        ax.text(c + 0.3, i, f"{c}  ({s:.1f}%)", va="center", fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlim(0, 21)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel("Interface uses (count)")
    ax.grid(axis="x", color="#e3e7ec", lw=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    title(fig, "What tools do agentic judges reach for?", sub="60 interface uses across 34 tool-augmented judges", y=1.05)
    source(fig, "Data: You et al., 2026, Appendix Table 10 (the survey's own manual coding). Chart drawn by the author.", y=-0.06)
    save(fig, "fig9_tool_interfaces.png")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    diffs = fig5()
    print("best-vs-best gaps:", {k: round(v, 1) for k, v in diffs[0].items()})
    print("median-vs-median gaps:", {k: round(v, 1) for k, v in diffs[1].items()})
    fig6()
    fig7()
    fig8()
    fig9()
