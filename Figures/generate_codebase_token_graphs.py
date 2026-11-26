#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib>=3.8.0",
#   "numpy>=1.26.0",
#   "pandas>=2.2.0",
# ]
# ///
"""
Generate publication-quality LINE GRAPHS comparing token usage across existing coursework codebases:
- Mean values omitted (no mean reference lines, no mean in legends).
- Y-axis label: 'Total Tokens per Trial'.
- Solid line for Skill, chopped line for No-skill.
- Short X-axis task names: Course prefixes ('COSC ...') hidden, distinguishing parentheticals preserved.
- Saves to BOTH 'codebase-tokens-*' and 'codebase-tokens-line-*' filenames to ensure compatibility.
"""

from pathlib import Path
import json
import shutil
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

figures_dir = Path(__file__).resolve().parent
artifact_dir = Path("/Users/luis/.gemini/antigravity-cli/brain/efc559fa-b752-40eb-adf5-4c9ce98ce810")
artifact_dir.mkdir(parents=True, exist_ok=True)

# Styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 13,
})

# Load benchmark summary data
run_paths = {
    "gpt_skill": Path("/Users/luis/Code/Thesis_Implementation/eval_results/20261118_004127/benchmark_summary.json"),
    "gpt_noskill": Path("/Users/luis/Code/Thesis_Implementation/eval_results/20261118_104042/benchmark_summary.json"),
    "gemini_skill": Path("/Users/luis/Code/Thesis_Implementation/eval_results/20261117_164549/benchmark_summary.json"),
    "gemini_noskill": Path("/Users/luis/Code/Thesis_Implementation/eval_results/20261116_190315/benchmark_summary.json"),
}

records = []
for key, p in run_paths.items():
    with open(p) as f:
        d = json.load(f)
    for t_idx, t in enumerate(d["tasks"]):
        for s_idx, s in enumerate(t["samples"]):
            records.append({
                "cond": key,
                "task_idx": t_idx,
                "task_title": t["title"],
                "total_tokens": s.get("total_tokens", 0),
            })

df = pd.DataFrame(records)
task_means = df.groupby(["cond", "task_idx"])["total_tokens"].mean().unstack(level=0)

# Shortened names: Course codes (COSC ...) removed; parentheticals preserved to distinguish tasks
tasks_short = [
    "AI",
    "(OS)",
    "(Labs)",
    "(DS)",
    "(Mobile)",
    "(Neural)",
    "ProgLang",
    "(Sockets)",
]
task_x = np.arange(len(tasks_short))

gpt_skill = task_means["gpt_skill"].values
gpt_noskill = task_means["gpt_noskill"].values
gemini_skill = task_means["gemini_skill"].values
gemini_noskill = task_means["gemini_noskill"].values

# Line Styles: solid line for Skill, chopped line for No-skill
LINE_SKILL = "-"
LINE_NOSKILL = (0, (5, 3))  # Chopped / dashed line

# Colors
C_SKILL = "#2b5c8f"         # Steel Blue
C_NOSKILL = "#d95f02"       # Rust Orange
C_GEMINI_SKILL = "#1b5e20"   # Dark Emerald Green
C_GEMINI_NOSKILL = "#d95f02" # Rust Orange
C_GPT_SKILL = "#0d47a1"      # Navy Blue
C_GPT_NOSKILL = "#e65100"    # Warm Rust / Orange
BG_SHADE = "#f7f8fa"


def save_plot(fig, base_stem: str):
    """Save plot in PDF, PNG, SVG across standard and -line- stem aliases."""
    stems = [base_stem]
    if "-line-" in base_stem:
        stems.append(base_stem.replace("-line-", "-"))
    else:
        stems.append(base_stem.replace("codebase-tokens-", "codebase-tokens-line-"))

    # Also handle gpt-oss vs gpt-oss-120b
    extra_stems = []
    for s in stems:
        if "gpt-oss" in s and "120b" not in s:
            extra_stems.append(s.replace("gpt-oss", "gpt-oss-120b"))
    stems.extend(extra_stems)
    stems = list(dict.fromkeys(stems))

    for s in stems:
        for ext in [".pdf", ".png", ".svg"]:
            out_path = figures_dir / f"{s}{ext}"
            fig.savefig(out_path, dpi=300, bbox_inches="tight")
        shutil.copy2(figures_dir / f"{s}.png", artifact_dir / f"{s}.png")
        print(f"Saved {s}.[pdf|png|svg]")


# 1. GPT-OSS 120B DEDICATED LINE GRAPH (Skill vs. No-skill)
def plot_gpt_line_graph():
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=300)

    for i in range(len(tasks_short)):
        if i % 2 == 1:
            ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Solid line for Skill
    ax.plot(
        task_x, gpt_skill,
        color=C_SKILL, linestyle=LINE_SKILL, linewidth=2.4, marker="o", markersize=8,
        label="Skill", zorder=4
    )
    # Chopped line for No-skill
    ax.plot(
        task_x, gpt_noskill,
        color=C_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.2, marker="s", markersize=7.5,
        label="No skill", zorder=3
    )

    # Value annotations in k tokens
    for i in range(len(tasks_short)):
        sv = gpt_skill[i]
        nsv = gpt_noskill[i]
        ax.text(i, sv + 1300, f"{sv/1000:.1f}k", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_SKILL, zorder=5)
        ax.text(i, nsv - 1900, f"{nsv/1000:.1f}k", ha="center", va="top", fontsize=8.5, fontweight="bold", color=C_NOSKILL, zorder=5)

    ax.set_xticks(task_x)
    ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks_short)], fontsize=9.5)
    ax.set_xlim(-0.5, len(tasks_short) - 0.5)
    ax.set_ylim(0, 52000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v/1000):,}k" if v > 0 else "0"))
    ax.set_ylabel("Total Tokens per Trial")
    ax.set_title("GPT-OSS 120B: Token Usage Across Codebase Tasks (Skill vs. No-skill)", fontweight="bold", pad=10)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    plt.tight_layout()
    save_plot(fig, "codebase-tokens-gpt-oss")
    plt.close(fig)


# 2. GEMINI 3.8 FLASH DEDICATED LINE GRAPH (Skill vs. No-skill)
def plot_gemini_line_graph():
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=300)

    for i in range(len(tasks_short)):
        if i % 2 == 1:
            ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Solid line for Skill
    ax.plot(
        task_x, gemini_skill,
        color=C_SKILL, linestyle=LINE_SKILL, linewidth=2.4, marker="o", markersize=8,
        label="Skill", zorder=4
    )
    # Chopped line for No-skill
    ax.plot(
        task_x, gemini_noskill,
        color=C_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.2, marker="s", markersize=7.5,
        label="No skill", zorder=3
    )

    for i in range(len(tasks_short)):
        sv = gemini_skill[i]
        nsv = gemini_noskill[i]
        if sv >= nsv:
            ax.text(i, sv + 7000, f"{sv/1000:.1f}k", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_SKILL, zorder=5)
            ax.text(i, nsv - 10000, f"{nsv/1000:.1f}k", ha="center", va="top", fontsize=8.5, fontweight="bold", color=C_NOSKILL, zorder=5)
        else:
            ax.text(i, sv - 10000, f"{sv/1000:.1f}k", ha="center", va="top", fontsize=8.5, fontweight="bold", color=C_SKILL, zorder=5)
            ax.text(i, nsv + 7000, f"{nsv/1000:.1f}k", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=C_NOSKILL, zorder=5)

    ax.set_xticks(task_x)
    ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks_short)], fontsize=9.5)
    ax.set_xlim(-0.5, len(tasks_short) - 0.5)
    ax.set_ylim(40000, 315000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v/1000):,}k" if v > 0 else "0"))
    ax.set_ylabel("Total Tokens per Trial")
    ax.set_title("Gemini 3.8 Flash: Token Usage Across Codebase Tasks (Skill vs. No-skill)", fontweight="bold", pad=10)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    plt.tight_layout()
    save_plot(fig, "codebase-tokens-gemini")
    plt.close(fig)


# 3. SIDE-BY-SIDE 2-PANEL LINE GRAPH (Both Models)
def plot_two_panel_line_graph():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 4.5), dpi=300)

    # Panel 1: GPT-OSS
    for i in range(len(tasks_short)):
        if i % 2 == 1:
            ax1.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    ax1.plot(task_x, gpt_skill, color=C_SKILL, linestyle=LINE_SKILL, linewidth=2.3, marker="o", markersize=7.5, label="Skill", zorder=4)
    ax1.plot(task_x, gpt_noskill, color=C_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.1, marker="s", markersize=7, label="No skill", zorder=3)

    for i in range(len(tasks_short)):
        sv = gpt_skill[i]
        nsv = gpt_noskill[i]
        ax1.text(i, sv + 1300, f"{sv/1000:.1f}k", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=C_SKILL, zorder=5)
        ax1.text(i, nsv - 1800, f"{nsv/1000:.1f}k", ha="center", va="top", fontsize=8.2, fontweight="bold", color=C_NOSKILL, zorder=5)

    ax1.set_xticks(task_x)
    ax1.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks_short)], fontsize=8.8)
    ax1.set_xlim(-0.5, len(tasks_short) - 0.5)
    ax1.set_ylim(0, 52000)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v/1000):,}k" if v > 0 else "0"))
    ax1.set_ylabel("Total Tokens per Trial")
    ax1.set_title("(a) GPT-OSS 120B", fontweight="bold", pad=8)
    ax1.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax1.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    # Panel 2: Gemini
    for i in range(len(tasks_short)):
        if i % 2 == 1:
            ax2.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    ax2.plot(task_x, gemini_skill, color=C_SKILL, linestyle=LINE_SKILL, linewidth=2.3, marker="o", markersize=7.5, label="Skill", zorder=4)
    ax2.plot(task_x, gemini_noskill, color=C_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.1, marker="s", markersize=7, label="No skill", zorder=3)

    for i in range(len(tasks_short)):
        sv = gemini_skill[i]
        nsv = gemini_noskill[i]
        if sv >= nsv:
            ax2.text(i, sv + 7000, f"{sv/1000:.1f}k", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=C_SKILL, zorder=5)
            ax2.text(i, nsv - 10000, f"{nsv/1000:.1f}k", ha="center", va="top", fontsize=8.2, fontweight="bold", color=C_NOSKILL, zorder=5)
        else:
            ax2.text(i, sv - 10000, f"{sv/1000:.1f}k", ha="center", va="top", fontsize=8.2, fontweight="bold", color=C_SKILL, zorder=5)
            ax2.text(i, nsv + 7000, f"{nsv/1000:.1f}k", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=C_NOSKILL, zorder=5)

    ax2.set_xticks(task_x)
    ax2.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks_short)], fontsize=8.8)
    ax2.set_xlim(-0.5, len(tasks_short) - 0.5)
    ax2.set_ylim(40000, 315000)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v/1000):,}k" if v > 0 else "0"))
    ax2.set_ylabel("Total Tokens per Trial")
    ax2.set_title("(b) Gemini 3.8 Flash", fontweight="bold", pad=8)
    ax2.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax2.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    plt.tight_layout()
    save_plot(fig, "codebase-tokens-panels")
    plt.close(fig)


# 4. UNIFIED 4-LINE GRAPH ACROSS ALL 8 CODEBASE TASKS
def plot_unified_line_graph():
    fig, ax = plt.subplots(figsize=(10.2, 5.0), dpi=300)

    for i in range(len(tasks_short)):
        if i % 2 == 1:
            ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Solid line for Skill, chopped line for No-skill
    ax.plot(
        task_x, gemini_skill,
        color=C_GEMINI_SKILL, linestyle=LINE_SKILL, linewidth=2.4, marker="o", markersize=8,
        label="Gemini 3.8 Flash (Skill)", zorder=5
    )
    ax.plot(
        task_x, gemini_noskill,
        color=C_GEMINI_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.2, marker="s", markersize=7.5,
        label="Gemini 3.8 Flash (No skill)", zorder=4
    )
    ax.plot(
        task_x, gpt_skill,
        color=C_GPT_SKILL, linestyle=LINE_SKILL, linewidth=2.2, marker="^", markersize=7.5,
        label="GPT-OSS 120B (Skill)", zorder=4
    )
    ax.plot(
        task_x, gpt_noskill,
        color=C_GPT_NOSKILL, linestyle=LINE_NOSKILL, linewidth=2.0, marker="D", markersize=7,
        label="GPT-OSS 120B (No skill)", zorder=3
    )

    for i in range(len(tasks_short)):
        ax.annotate(
            f"{gemini_skill[i]/1000:.1f}k",
            (i, gemini_skill[i]),
            xytext=(0, 6), textcoords="offset points",
            ha="center", va="bottom", fontsize=8, fontweight="bold", color=C_GEMINI_SKILL, zorder=6
        )
        ax.annotate(
            f"{gpt_skill[i]/1000:.1f}k",
            (i, gpt_skill[i]),
            xytext=(0, 5), textcoords="offset points",
            ha="center", va="bottom", fontsize=8, fontweight="bold", color=C_GPT_SKILL, zorder=6
        )

    ax.set_xticks(task_x)
    ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks_short)], fontsize=9.2)
    ax.set_xlim(-0.5, len(tasks_short) - 0.5)
    ax.set_ylim(-5000, 310000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v/1000):,}k" if v > 0 else "0"))
    ax.set_ylabel("Total Tokens per Trial")
    ax.set_title("Token Usage Comparison Across Codebase Tasks (Skill vs. No-skill)", fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    plt.tight_layout()
    save_plot(fig, "codebase-tokens-all")
    plt.close(fig)


def main():
    print("Generating updated codebase token line graphs...")
    plot_gpt_line_graph()
    plot_gemini_line_graph()
    plot_two_panel_line_graph()
    plot_unified_line_graph()
    print("All token line graphs generated successfully!")


if __name__ == "__main__":
    main()
