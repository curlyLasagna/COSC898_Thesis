# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib>=3.8.0",
#   "numpy>=1.26.0",
#   "pandas>=2.2.0",
# ]
# ///

#!/usr/bin/env python3
"""
Generate publication-quality graphs for Natural Language benchmark evaluations:
Comparing Pass@1 and Pass@3 between Skill and No-skill conditions for:
1. GPT-OSS 120B (eval runs 20261101_161538 vs 20261118_003227)
2. Gemini 3.8 Flash (eval runs 20261031_113621 vs 20261114_145333)

Outputs PDF, PNG (300 dpi), and SVG vector files with the 'natural_lang_' prefix.
"""

from pathlib import Path
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# Set paths
figures_dir = Path(__file__).resolve().parent
eval_dir = Path("/Users/luis/Code/Thesis_Implementation/eval_results")

# Setup Matplotlib styling to match thesis publication aesthetic
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 13,
})

# Color palette adhering to thesis style
COLOR_SKILL = "#2b5c8f"     # Slate / Steel Blue
COLOR_NOSKILL = "#d95f02"   # Ochre / Rust Orange
BG_SHADE = "#f4f5f8"        # Alternating background shading
TRACK_DIVIDER_COLOR = "#888888"

TASK_NAMES = [
    "Java 17", "Flutter", "Python", "GCC", "Clang",
    "Node.js", "Rust", "Go", ".NET SDK", "Ruby",
    "R", "RStudio", "MySQL", "Workbench"
]

# Overall benchmark summary data provided in prompt
OVERALL_DATA = {
    "GPT-OSS 120B": {
        "Skill": {
            "run_id": "161538",
            "pass@1": 73.81,
            "pass@3": 78.57,
            "tokens": 25974,
            "precision": 83.5,
            "over_prov": 1.39,
        },
        "No skill": {
            "run_id": "003227",
            "pass@1": 33.33,
            "pass@3": 64.29,
            "tokens": 18116,
            "precision": None,
            "over_prov": None,
        },
    },
    "Gemini": {
        "Skill": {
            "run_id": "113621",
            "pass@1": 95.24,
            "pass@3": 100.0,
            "tokens": 221295,
            "precision": None,
            "over_prov": None,
        },
        "No skill": {
            "run_id": "145333",
            "pass@1": 88.10,
            "pass@3": 100.0,
            "tokens": 102640,
            "precision": None,
            "over_prov": None,
        },
    },
}

def load_run_tasks(run_id_full: str):
    summary_path = eval_dir / run_id_full / "benchmark_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"Missing {summary_path}")
    with open(summary_path) as f:
        d = json.load(f)
    tasks = d["tasks"]
    if isinstance(tasks, dict):
        tasks = list(tasks.values())
    p1 = [t["scores"]["pass@1"] * 100 for t in tasks]
    p3 = [t["scores"]["pass@3"] * 100 for t in tasks]
    tokens = []
    for t in tasks:
        samples = t.get("samples", [])
        toks = [s.get("total_tokens", 0) for s in samples if "total_tokens" in s]
        tokens.append(sum(toks) / len(toks) if toks else 0)
    return p1, p3, tokens

# Load task-level data
gpt_sk_p1, gpt_sk_p3, gpt_sk_tok = load_run_tasks("20261101_161538")
gpt_no_p1, gpt_no_p3, gpt_no_tok = load_run_tasks("20261118_003227")
gem_sk_p1, gem_sk_p3, gem_sk_tok = load_run_tasks("20261031_113621")
gem_no_p1, gem_no_p3, gem_no_tok = load_run_tasks("20261114_145333")

def save_fig(fig, base_name: str):
    for ext in ["pdf", "png", "svg"]:
        out_path = figures_dir / f"{base_name}.{ext}"
        if ext == "png":
            fig.savefig(out_path, dpi=300, bbox_inches="tight")
        else:
            fig.savefig(out_path, bbox_inches="tight")
    print(f"Saved {base_name}.(pdf|png|svg)")
    plt.close(fig)

# ==============================================================================
# Graph 1: Overall Pass@k Progression for GPT-OSS 120B (Skill vs No-Skill)
# ==============================================================================
def plot_overall_pass_k_single(model_name: str, y_min: float = 0, y_max: float = 105):
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
    
    m_data = OVERALL_DATA[model_name]
    x_vals = [1, 3]
    x_labels = ["pass@1", "pass@3"]
    
    y_sk = [m_data["Skill"]["pass@1"], m_data["Skill"]["pass@3"]]
    y_no = [m_data["No skill"]["pass@1"], m_data["No skill"]["pass@3"]]
    
    # Plot lines with styling
    ax.plot(
        x_vals, y_sk,
        color=COLOR_SKILL, marker="o", markersize=8, linewidth=2.4,
        label=f"Skill (`{m_data['Skill']['run_id']}`)",
        zorder=4
    )
    ax.plot(
        x_vals, y_no,
        color=COLOR_NOSKILL, marker="s", markersize=8, linewidth=2.2, linestyle="--",
        label=f"No skill (`{m_data['No skill']['run_id']}`)",
        zorder=4
    )
    
    # Data value annotations
    if model_name == "GPT-OSS 120B":
        # Skill annotations
        ax.annotate(
            f"{y_sk[0]:.2f}%", (x_vals[0], y_sk[0]),
            textcoords="offset points", xytext=(0, 9), ha="center",
            fontweight="bold", color=COLOR_SKILL, fontsize=10.5
        )
        ax.annotate(
            f"{y_sk[1]:.2f}%", (x_vals[1], y_sk[1]),
            textcoords="offset points", xytext=(0, 9), ha="center",
            fontweight="bold", color=COLOR_SKILL, fontsize=10.5
        )
        # No skill annotations
        ax.annotate(
            f"{y_no[0]:.2f}%", (x_vals[0], y_no[0]),
            textcoords="offset points", xytext=(0, 9), ha="center",
            fontweight="bold", color=COLOR_NOSKILL, fontsize=10.5
        )
        ax.annotate(
            f"{y_no[1]:.2f}%", (x_vals[1], y_no[1]),
            textcoords="offset points", xytext=(0, -18), ha="center",
            fontweight="bold", color=COLOR_NOSKILL, fontsize=10.5
        )
        # Delta box placed in upper-left to prevent any overlap
        delta_p1 = y_sk[0] - y_no[0]
        delta_p3 = y_sk[1] - y_no[1]
        summary_text = f"Δ pass@1: +{delta_p1:.2f}%\nΔ pass@3: +{delta_p3:.2f}%"
        ax.text(
            0.05, 0.70, summary_text,
            transform=ax.transAxes,
            fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#cccccc", alpha=0.9),
            verticalalignment="top"
        )
    else:  # Gemini
        ax.annotate(
            f"{y_sk[0]:.2f}%", (x_vals[0], y_sk[0]),
            textcoords="offset points", xytext=(0, 9), ha="center",
            fontweight="bold", color=COLOR_SKILL, fontsize=10.5
        )
        ax.annotate(
            f"{y_no[0]:.2f}%", (x_vals[0], y_no[0]),
            textcoords="offset points", xytext=(0, -18), ha="center",
            fontweight="bold", color=COLOR_NOSKILL, fontsize=10.5
        )
        # At pass@3 both hit 100.00%
        ax.annotate(
            f"{y_sk[1]:.2f}%\n(Both)", (x_vals[1], y_sk[1]),
            textcoords="offset points", xytext=(0, 9), ha="center",
            fontweight="bold", color="#1c3d5a", fontsize=10.0
        )
        delta_p1 = y_sk[0] - y_no[0]
        delta_p3 = y_sk[1] - y_no[1]
        summary_text = f"Δ pass@1: +{delta_p1:.2f}%\nΔ pass@3: +{delta_p3:.2f}%"
        ax.text(
            0.05, 0.18, summary_text,
            transform=ax.transAxes,
            fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#cccccc", alpha=0.9),
            verticalalignment="bottom"
        )
    
    # Midpoint fill to visualize gap
    ax.fill_between(x_vals, y_sk, y_no, color=COLOR_SKILL, alpha=0.08, zorder=2)
    
    ax.set_xticks(x_vals)
    ax.set_xticklabels(x_labels, fontweight="bold", fontsize=11)
    ax.set_xlim(0.7, 3.3)
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.set_ylabel("Synthesis Accuracy (%)", fontweight="bold")
    ax.set_title(f"Natural Language Flake Synthesis: {model_name}\nSkill vs. No-Skill Evaluation", fontweight="bold", pad=12)
    
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)
    plt.tight_layout()
    
    slug = model_name.lower().replace(" ", "_").replace("-", "_")
    save_fig(fig, f"natural_lang_{slug}_pass_k")

plot_overall_pass_k_single("GPT-OSS 120B", y_min=20, y_max=92)
plot_overall_pass_k_single("Gemini", y_min=75, y_max=108)


# ==============================================================================
# Graph 2: Combined 2-Panel Overall Pass@k Comparison (Both Models)
# ==============================================================================
def plot_overall_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=300, sharey=True)
    
    x_vals = [1, 3]
    x_labels = ["pass@1", "pass@3"]
    
    for ax, model_name, subtitle, y_sk, y_no, r_sk, r_no, is_gpt in [
        (ax1, "GPT-OSS 120B", "(Open-Weight Baseline)", 
         [OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@1"], OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@3"]],
         [OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@1"], OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@3"]],
         OVERALL_DATA["GPT-OSS 120B"]["Skill"]["run_id"],
         OVERALL_DATA["GPT-OSS 120B"]["No skill"]["run_id"], True),
        (ax2, "Gemini 3.8 Flash", "(Frontier Baseline)",
         [OVERALL_DATA["Gemini"]["Skill"]["pass@1"], OVERALL_DATA["Gemini"]["Skill"]["pass@3"]],
         [OVERALL_DATA["Gemini"]["No skill"]["pass@1"], OVERALL_DATA["Gemini"]["No skill"]["pass@3"]],
         OVERALL_DATA["Gemini"]["Skill"]["run_id"],
         OVERALL_DATA["Gemini"]["No skill"]["run_id"], False),
    ]:
        ax.plot(
            x_vals, y_sk,
            color=COLOR_SKILL, marker="o", markersize=8, linewidth=2.4,
            label=f"Skill (`{r_sk}`)", zorder=4
        )
        ax.plot(
            x_vals, y_no,
            color=COLOR_NOSKILL, marker="s", markersize=8, linewidth=2.2, linestyle="--",
            label=f"No skill (`{r_no}`)", zorder=4
        )
        
        # Annotate
        if is_gpt:
            ax.annotate(f"{y_sk[0]:.1f}%", (x_vals[0], y_sk[0]), textcoords="offset points", xytext=(0, 8), ha="center", fontweight="bold", color=COLOR_SKILL)
            ax.annotate(f"{y_sk[1]:.1f}%", (x_vals[1], y_sk[1]), textcoords="offset points", xytext=(0, 8), ha="center", fontweight="bold", color=COLOR_SKILL)
            ax.annotate(f"{y_no[0]:.1f}%", (x_vals[0], y_no[0]), textcoords="offset points", xytext=(0, 8), ha="center", fontweight="bold", color=COLOR_NOSKILL)
            ax.annotate(f"{y_no[1]:.1f}%", (x_vals[1], y_no[1]), textcoords="offset points", xytext=(0, -17), ha="center", fontweight="bold", color=COLOR_NOSKILL)
            
            delta_p1 = y_sk[0] - y_no[0]
            delta_p3 = y_sk[1] - y_no[1]
            ax.text(
                0.05, 0.72, f"Δ pass@1: +{delta_p1:.1f}%\nΔ pass@3: +{delta_p3:.1f}%",
                transform=ax.transAxes, fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#cccccc", alpha=0.9)
            )
        else:
            ax.annotate(f"{y_sk[0]:.1f}%", (x_vals[0], y_sk[0]), textcoords="offset points", xytext=(0, 8), ha="center", fontweight="bold", color=COLOR_SKILL)
            ax.annotate(f"{y_no[0]:.1f}%", (x_vals[0], y_no[0]), textcoords="offset points", xytext=(0, -17), ha="center", fontweight="bold", color=COLOR_NOSKILL)
            ax.annotate(f"{y_sk[1]:.1f}% (Both)", (x_vals[1], y_sk[1]), textcoords="offset points", xytext=(0, 8), ha="center", fontweight="bold", color="#1c3d5a")
            
            delta_p1 = y_sk[0] - y_no[0]
            delta_p3 = y_sk[1] - y_no[1]
            ax.text(
                0.05, 0.12, f"Δ pass@1: +{delta_p1:.1f}%\nΔ pass@3: +{delta_p3:.1f}%",
                transform=ax.transAxes, fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#cccccc", alpha=0.9)
            )
        
        ax.fill_between(x_vals, y_sk, y_no, color=COLOR_SKILL, alpha=0.08, zorder=2)
        ax.set_xticks(x_vals)
        ax.set_xticklabels(x_labels, fontweight="bold", fontsize=11)
        ax.set_xlim(0.7, 3.3)
        ax.set_ylim(20, 110)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
        ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(f"{model_name}\n{subtitle}", fontweight="bold", fontsize=11.5)
        
        ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    ax1.set_ylabel("Synthesis Accuracy (%)", fontweight="bold")
    fig.suptitle("Natural Language Benchmark: Pass@k Progression Across Models (Skill vs. No-Skill)", fontweight="bold", fontsize=12.5, y=1.02)
    plt.tight_layout()
    save_fig(fig, "natural_lang_pass_k_comparison")

plot_overall_combined()


# ==============================================================================
# Helper for Task-Level Line Graphs
# ==============================================================================
def plot_task_line_graph(
    model_name: str,
    metric_name: str,       # "pass@1" or "pass@3"
    y_sk_tasks: list,
    y_no_tasks: list,
    mean_sk: float,
    mean_no: float,
    run_sk: str,
    run_no: str,
    base_name: str,
):
    fig, ax = plt.subplots(figsize=(11.5, 4.3), dpi=300)
    indices = np.arange(len(TASK_NAMES))
    
    # Alternate shading for task readability
    for t in range(len(TASK_NAMES)):
        if t % 2 == 1:
            ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)
            
    # Track separator (Computer Science vs Data Science)
    # Tasks 0-9 are CS, Tasks 10-13 are DS
    ax.axvline(9.5, color=TRACK_DIVIDER_COLOR, linestyle=":", linewidth=1.5, zorder=2)
    ax.text(4.5, 108, "Computer Science Track", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#444444")
    ax.text(11.5, 108, "Data Science Track", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#444444")
    
    # Reference mean lines
    ax.axhline(mean_sk, color=COLOR_SKILL, linestyle="--", linewidth=1.2, alpha=0.8, zorder=2,
               label=f"Skill Mean: {mean_sk:.1f}%")
    ax.axhline(mean_no, color=COLOR_NOSKILL, linestyle=":", linewidth=1.2, alpha=0.8, zorder=2,
               label=f"No skill Mean: {mean_no:.1f}%")
    
    # Plot task lines
    ax.plot(
        indices, y_sk_tasks,
        color=COLOR_SKILL, marker="o", markersize=6.5, linewidth=2.0,
        label=f"Skill (`{run_sk}`)", zorder=4
    )
    ax.plot(
        indices, y_no_tasks,
        color=COLOR_NOSKILL, marker="s", markersize=6.0, linewidth=1.8, linestyle="--",
        label=f"No skill (`{run_no}`)", zorder=4
    )
    
    ax.set_xticks(indices)
    ax.set_xticklabels([f"T{i}\n{name}" for i, name in enumerate(TASK_NAMES)], fontsize=8.2)
    ax.tick_params(axis="x", length=0, pad=5)
    
    ax.set_xlim(-0.6, len(TASK_NAMES) - 0.4)
    ax.set_ylim(-5, 118)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.set_ylabel(f"{metric_name.upper()} Success Rate (%)", fontweight="bold")
    ax.set_title(
        f"Natural Language Benchmark: {model_name} {metric_name.upper()} by Task\nSkill (`{run_sk}`) vs. No-Skill (`{run_no}`)",
        fontweight="bold", pad=12
    )
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95, ncol=2)
    plt.tight_layout()
    save_fig(fig, base_name)


# 1. GPT-OSS 120B Pass@1 Line Graph across tasks
plot_task_line_graph(
    model_name="GPT-OSS 120B",
    metric_name="pass@1",
    y_sk_tasks=gpt_sk_p1,
    y_no_tasks=gpt_no_p1,
    mean_sk=OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@1"],
    mean_no=OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@1"],
    run_sk="161538",
    run_no="003227",
    base_name="natural_lang_gpt_oss_120b_pass1",
)

# 2. GPT-OSS 120B Pass@3 Line Graph across tasks
plot_task_line_graph(
    model_name="GPT-OSS 120B",
    metric_name="pass@3",
    y_sk_tasks=gpt_sk_p3,
    y_no_tasks=gpt_no_p3,
    mean_sk=OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@3"],
    mean_no=OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@3"],
    run_sk="161538",
    run_no="003227",
    base_name="natural_lang_gpt_oss_120b_pass3",
)

# 3. Gemini Pass@1 Line Graph across tasks
plot_task_line_graph(
    model_name="Gemini 3.8 Flash",
    metric_name="pass@1",
    y_sk_tasks=gem_sk_p1,
    y_no_tasks=gem_no_p1,
    mean_sk=OVERALL_DATA["Gemini"]["Skill"]["pass@1"],
    mean_no=OVERALL_DATA["Gemini"]["No skill"]["pass@1"],
    run_sk="113621",
    run_no="145333",
    base_name="natural_lang_gemini_pass1",
)

# 4. Gemini Pass@3 Line Graph across tasks
plot_task_line_graph(
    model_name="Gemini 3.8 Flash",
    metric_name="pass@3",
    y_sk_tasks=gem_sk_p3,
    y_no_tasks=gem_no_p3,
    mean_sk=OVERALL_DATA["Gemini"]["Skill"]["pass@3"],
    mean_no=OVERALL_DATA["Gemini"]["No skill"]["pass@3"],
    run_sk="113621",
    run_no="145333",
    base_name="natural_lang_gemini_pass3",
)


# ==============================================================================
# Graph Combined: 2-Panel Task Breakdown for Each Model (Pass@1 and Pass@3 together)
# ==============================================================================
def plot_model_tasks_combined(
    model_name: str,
    p1_sk: list, p1_no: list,
    p3_sk: list, p3_no: list,
    mean_p1_sk: float, mean_p1_no: float,
    mean_p3_sk: float, mean_p3_no: float,
    run_sk: str, run_no: str,
    base_name: str,
):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 6.8), dpi=300, sharex=True)
    indices = np.arange(len(TASK_NAMES))
    
    for ax, metric, y_sk, y_no, m_sk, m_no in [
        (ax1, "Pass@1", p1_sk, p1_no, mean_p1_sk, mean_p1_no),
        (ax2, "Pass@3", p3_sk, p3_no, mean_p3_sk, mean_p3_no),
    ]:
        for t in range(len(TASK_NAMES)):
            if t % 2 == 1:
                ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)
        
        ax.axvline(9.5, color=TRACK_DIVIDER_COLOR, linestyle=":", linewidth=1.5, zorder=2)
        
        # Mean reference lines
        ax.axhline(m_sk, color=COLOR_SKILL, linestyle="--", linewidth=1.1, alpha=0.8, zorder=2,
                   label=f"Skill Mean: {m_sk:.1f}%")
        ax.axhline(m_no, color=COLOR_NOSKILL, linestyle=":", linewidth=1.1, alpha=0.8, zorder=2,
                   label=f"No skill Mean: {m_no:.1f}%")
        
        ax.plot(indices, y_sk, color=COLOR_SKILL, marker="o", markersize=6.0, linewidth=1.9,
                label=f"Skill (`{run_sk}`)", zorder=4)
        ax.plot(indices, y_no, color=COLOR_NOSKILL, marker="s", markersize=5.5, linewidth=1.7, linestyle="--",
                label=f"No skill (`{run_no}`)", zorder=4)
        
        ax.set_ylim(-5, 115)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
        ax.set_ylabel(f"{metric} (%)", fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95, ncol=2, fontsize=8.8)
    
    ax1.set_title(f"{model_name}: Task-Level Pass@1 and Pass@3 (Skill vs. No-Skill)", fontweight="bold", pad=10)
    ax1.text(4.5, 106, "Computer Science Track", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#444444")
    ax1.text(11.5, 106, "Data Science Track", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#444444")
    
    ax2.set_xticks(indices)
    ax2.set_xticklabels([f"T{i}\n{name}" for i, name in enumerate(TASK_NAMES)], fontsize=8.2)
    ax2.tick_params(axis="x", length=0, pad=5)
    
    plt.tight_layout()
    save_fig(fig, base_name)

plot_model_tasks_combined(
    model_name="GPT-OSS 120B",
    p1_sk=gpt_sk_p1, p1_no=gpt_no_p1,
    p3_sk=gpt_sk_p3, p3_no=gpt_no_p3,
    mean_p1_sk=OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@1"],
    mean_p1_no=OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@1"],
    mean_p3_sk=OVERALL_DATA["GPT-OSS 120B"]["Skill"]["pass@3"],
    mean_p3_no=OVERALL_DATA["GPT-OSS 120B"]["No skill"]["pass@3"],
    run_sk="161538", run_no="003227",
    base_name="natural_lang_gpt_oss_120b_tasks_combined"
)

plot_model_tasks_combined(
    model_name="Gemini 3.8 Flash",
    p1_sk=gem_sk_p1, p1_no=gem_no_p1,
    p3_sk=gem_sk_p3, p3_no=gem_no_p3,
    mean_p1_sk=OVERALL_DATA["Gemini"]["Skill"]["pass@1"],
    mean_p1_no=OVERALL_DATA["Gemini"]["No skill"]["pass@1"],
    mean_p3_sk=OVERALL_DATA["Gemini"]["Skill"]["pass@3"],
    mean_p3_no=OVERALL_DATA["Gemini"]["No skill"]["pass@3"],
    run_sk="113621", run_no="145333",
    base_name="natural_lang_gemini_tasks_combined"
)


# ==============================================================================
# Token Usage Graphs
# ==============================================================================

# 1. Overall Mean Token Usage Comparison (Bar Graph)
def plot_overall_token_usage():
    fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=300)
    
    models = ["GPT-OSS 120B", "Gemini 3.8 Flash"]
    x = np.arange(len(models))
    bar_width = 0.35
    
    skill_tokens = [
        OVERALL_DATA["GPT-OSS 120B"]["Skill"]["tokens"],
        OVERALL_DATA["Gemini"]["Skill"]["tokens"],
    ]
    noskill_tokens = [
        OVERALL_DATA["GPT-OSS 120B"]["No skill"]["tokens"],
        OVERALL_DATA["Gemini"]["No skill"]["tokens"],
    ]
    
    rects1 = ax.bar(
        x - bar_width / 2, skill_tokens, bar_width,
        label="Skill (`161538` / `113621`)", color=COLOR_SKILL, edgecolor="none", zorder=3
    )
    rects2 = ax.bar(
        x + bar_width / 2, noskill_tokens, bar_width,
        label="No skill (`003227` / `145333`)", color=COLOR_NOSKILL, edgecolor="none", zorder=3
    )
    
    # Value annotations on top of bars
    for rect, val in zip(rects1, skill_tokens):
        ax.text(
            rect.get_x() + rect.get_width() / 2, val + 4000,
            f"{val:,.0f}", ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color=COLOR_SKILL
        )
    for rect, val in zip(rects2, noskill_tokens):
        ax.text(
            rect.get_x() + rect.get_width() / 2, val + 4000,
            f"{val:,.0f}", ha="center", va="bottom",
            fontsize=9.5, fontweight="bold", color=COLOR_NOSKILL
        )
        
    # Multiplier callout
    gpt_mult = skill_tokens[0] / noskill_tokens[0]
    gem_mult = skill_tokens[1] / noskill_tokens[1]
    ax.text(
        x[0], max(skill_tokens[0], noskill_tokens[0]) + 17000,
        f"+{((gpt_mult-1)*100):.1f}% tokens\n({gpt_mult:.2f}×)",
        ha="center", va="bottom", fontsize=8.8, color="#444444", fontweight="bold"
    )
    ax.text(
        x[1], max(skill_tokens[1], noskill_tokens[1]) + 17000,
        f"+{((gem_mult-1)*100):.1f}% tokens\n({gem_mult:.2f}×)",
        ha="center", va="bottom", fontsize=8.8, color="#444444", fontweight="bold"
    )
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight="bold", fontsize=11)
    ax.set_ylabel("Mean Tokens per Trial", fontweight="bold")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}"))
    ax.set_ylim(0, 275000)
    ax.set_title("Natural Language Benchmark: Mean Token Consumption by Condition\nSkill vs. No-Skill", fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)
    
    plt.tight_layout()
    save_fig(fig, "natural_lang_token_usage_overall")

plot_overall_token_usage()


# 2. Overall Token Usage as a Line Graph Progression
def plot_overall_token_line():
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=300)
    
    x_vals = [0, 1]
    x_labels = ["No skill", "Skill"]
    
    gpt_vals = [
        OVERALL_DATA["GPT-OSS 120B"]["No skill"]["tokens"],
        OVERALL_DATA["GPT-OSS 120B"]["Skill"]["tokens"],
    ]
    gem_vals = [
        OVERALL_DATA["Gemini"]["No skill"]["tokens"],
        OVERALL_DATA["Gemini"]["Skill"]["tokens"],
    ]
    
    ax.plot(
        x_vals, gpt_vals, color=COLOR_NOSKILL, marker="s", markersize=8, linewidth=2.2,
        label="GPT-OSS 120B (`003227` → `161538`)", zorder=4
    )
    ax.plot(
        x_vals, gem_vals, color=COLOR_SKILL, marker="o", markersize=8, linewidth=2.4,
        label="Gemini 3.8 Flash (`145333` → `113621`)", zorder=4
    )
    
    # Annotate points (place above markers to avoid axis tick overlap)
    ax.annotate(f"{gpt_vals[0]:,}", (x_vals[0], gpt_vals[0]), textcoords="offset points", xytext=(0, 9), ha="center", fontweight="bold", color=COLOR_NOSKILL)
    ax.annotate(f"{gpt_vals[1]:,}", (x_vals[1], gpt_vals[1]), textcoords="offset points", xytext=(0, 9), ha="center", fontweight="bold", color=COLOR_NOSKILL)
    ax.annotate(f"{gem_vals[0]:,}", (x_vals[0], gem_vals[0]), textcoords="offset points", xytext=(0, 9), ha="center", fontweight="bold", color=COLOR_SKILL)
    ax.annotate(f"{gem_vals[1]:,}", (x_vals[1], gem_vals[1]), textcoords="offset points", xytext=(0, 9), ha="center", fontweight="bold", color=COLOR_SKILL)
    
    ax.set_xticks(x_vals)
    ax.set_xticklabels(x_labels, fontweight="bold", fontsize=11)
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(0, 265000)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}"))
    ax.set_ylabel("Mean Tokens per Trial", fontweight="bold")
    ax.set_title("Natural Language Benchmark: Token Usage by Condition\nNo-Skill vs. Skill", fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)
    
    plt.tight_layout()
    save_fig(fig, "natural_lang_token_usage_line")

plot_overall_token_line()


# 3. Task-Level Token Line Graph for a Single Model
def plot_task_token_line_graph(
    model_name: str,
    tok_sk: list,
    tok_no: list,
    mean_sk: float,
    mean_no: float,
    run_sk: str,
    run_no: str,
    base_name: str,
):
    fig, ax = plt.subplots(figsize=(11.5, 4.4), dpi=300)
    indices = np.arange(len(TASK_NAMES))
    
    for t in range(len(TASK_NAMES)):
        if t % 2 == 1:
            ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)
            
    ax.axvline(9.5, color=TRACK_DIVIDER_COLOR, linestyle=":", linewidth=1.5, zorder=2)
    max_y = max(max(tok_sk), max(tok_no))
    y_top = max_y * 1.32
    
    # Track annotations placed cleanly in upper areas
    ax.text(6.0, y_top * 0.92, "Computer Science Track", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#444444")
    ax.text(11.5, y_top * 0.92, "Data Science Track", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#444444")
    
    # Reference mean lines
    ax.axhline(mean_sk, color=COLOR_SKILL, linestyle="--", linewidth=1.2, alpha=0.8, zorder=2,
               label=f"Skill Mean: {int(mean_sk):,} tokens")
    ax.axhline(mean_no, color=COLOR_NOSKILL, linestyle=":", linewidth=1.2, alpha=0.8, zorder=2,
               label=f"No skill Mean: {int(mean_no):,} tokens")
    
    # Lines
    ax.plot(indices, tok_sk, color=COLOR_SKILL, marker="o", markersize=6.5, linewidth=2.0,
            label=f"Skill (`{run_sk}`)", zorder=4)
    ax.plot(indices, tok_no, color=COLOR_NOSKILL, marker="s", markersize=6.0, linewidth=1.8, linestyle="--",
            label=f"No skill (`{run_no}`)", zorder=4)
    
    ax.set_xticks(indices)
    ax.set_xticklabels([f"T{i}\n{name}" for i, name in enumerate(TASK_NAMES)], fontsize=8.2)
    ax.tick_params(axis="x", length=0, pad=5)
    
    ax.set_xlim(-0.6, len(TASK_NAMES) - 0.4)
    ax.set_ylim(0, y_top)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}"))
    ax.set_ylabel("Mean Total Tokens", fontweight="bold")
    ax.set_title(
        f"Natural Language Benchmark: {model_name} Token Consumption by Task\nSkill (`{run_sk}`) vs. No-Skill (`{run_no}`)",
        fontweight="bold", pad=12
    )
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95, ncol=1)
    plt.tight_layout()
    save_fig(fig, base_name)

plot_task_token_line_graph(
    model_name="GPT-OSS 120B",
    tok_sk=gpt_sk_tok,
    tok_no=gpt_no_tok,
    mean_sk=OVERALL_DATA["GPT-OSS 120B"]["Skill"]["tokens"],
    mean_no=OVERALL_DATA["GPT-OSS 120B"]["No skill"]["tokens"],
    run_sk="161538",
    run_no="003227",
    base_name="natural_lang_gpt_oss_120b_tokens",
)

plot_task_token_line_graph(
    model_name="Gemini 3.8 Flash",
    tok_sk=gem_sk_tok,
    tok_no=gem_no_tok,
    mean_sk=OVERALL_DATA["Gemini"]["Skill"]["tokens"],
    mean_no=OVERALL_DATA["Gemini"]["No skill"]["tokens"],
    run_sk="113621",
    run_no="145333",
    base_name="natural_lang_gemini_tokens",
)


# 4. Combined 2-Panel Task Token Graph for Both Models
def plot_combined_task_tokens():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.4), dpi=300, sharex=True)
    indices = np.arange(len(TASK_NAMES))
    
    for ax, model_name, tok_sk, tok_no, m_sk, m_no, r_sk, r_no in [
        (ax1, "GPT-OSS 120B", gpt_sk_tok, gpt_no_tok,
         OVERALL_DATA["GPT-OSS 120B"]["Skill"]["tokens"],
         OVERALL_DATA["GPT-OSS 120B"]["No skill"]["tokens"], "161538", "003227"),
        (ax2, "Gemini 3.8 Flash", gem_sk_tok, gem_no_tok,
         OVERALL_DATA["Gemini"]["Skill"]["tokens"],
         OVERALL_DATA["Gemini"]["No skill"]["tokens"], "113621", "145333"),
    ]:
        for t in range(len(TASK_NAMES)):
            if t % 2 == 1:
                ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)
        
        ax.axvline(9.5, color=TRACK_DIVIDER_COLOR, linestyle=":", linewidth=1.5, zorder=2)
        
        ax.axhline(m_sk, color=COLOR_SKILL, linestyle="--", linewidth=1.1, alpha=0.8, zorder=2,
                   label=f"Skill Mean: {int(m_sk):,}")
        ax.axhline(m_no, color=COLOR_NOSKILL, linestyle=":", linewidth=1.1, alpha=0.8, zorder=2,
                   label=f"No skill Mean: {int(m_no):,}")
        
        ax.plot(indices, tok_sk, color=COLOR_SKILL, marker="o", markersize=6.0, linewidth=1.9,
                label=f"Skill (`{r_sk}`)", zorder=4)
        ax.plot(indices, tok_no, color=COLOR_NOSKILL, marker="s", markersize=5.5, linewidth=1.7, linestyle="--",
                label=f"No skill (`{r_no}`)", zorder=4)
        
        y_top = max(max(tok_sk), max(tok_no)) * 1.34
        ax.set_ylim(0, y_top)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y):,}"))
        ax.set_ylabel("Tokens per Trial", fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95, ncol=1, fontsize=8.6)
        ax.set_title(f"{model_name}: Token Consumption by Task", fontweight="bold", pad=8)
        ax.text(6.0, y_top * 0.90, "Computer Science Track", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#444444")
        ax.text(11.5, y_top * 0.90, "Data Science Track", ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#444444")
    
    ax2.set_xticks(indices)
    ax2.set_xticklabels([f"T{i}\n{name}" for i, name in enumerate(TASK_NAMES)], fontsize=8.2)
    ax2.tick_params(axis="x", length=0, pad=5)
    
    plt.tight_layout()
    save_fig(fig, "natural_lang_tokens_combined")

plot_combined_task_tokens()

print("All Natural Language evaluation graphs successfully generated!")
