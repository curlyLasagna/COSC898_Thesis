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
Generate publication-quality line graphs for each evaluation run based on Run ID
referencing /Users/luis/Code/Thesis_Implementation/eval_results:
  1. Run ID 183227 (20261108_183222): GPT-OSS 120B (Skill)
  2. Run ID 221920 (20261116_221920): GPT-OSS 120B (No skill)
  3. Run ID 231204 (20261107_231204): Gemini 3.8 Flash (Skill)
  4. Run ID 171051 (20261116_171051): Gemini 3.8 Flash (No skill)

Outputs vector PDF, high-res PNG (300 DPI), and SVG with 'document-' prefix.
"""

from pathlib import Path
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

figures_dir = Path("/Users/luis/Documents/Thesis_Submission/Figures")
figures_dir.mkdir(parents=True, exist_ok=True)
eval_base = Path("/Users/luis/Code/Thesis_Implementation/eval_results")

# Styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 13,
})

# Colors
COLOR_SKILL = "#2b5c8f"     # Slate / Steel Blue
COLOR_NOSKILL = "#d95f02"   # Ochre / Rust Orange
COLOR_PASS1 = "#2da44e"     # Forest Green
COLOR_PASS3 = "#8250df"     # Purple
BG_SHADE = "#f4f5f8"
GRID_COLOR = "#e5e7eb"

SHORT_TASK_NAMES = [
    "COSC 175\n(C++/VS Code)",
    "ITEC 451\n(McGuire)",
    "Elixir/SQLite\n(HTML)",
    "Full-Stack\n(Elixir/Node)",
    "CS 564\n(Jupyter)",
    "Rust Toolchain\n(Brown Univ)",
    "MMP 350\n(Web Dev)",
]

# Run Registry
RUNS = {
    "183227": {
        "dir": "20261108_183222",
        "model": "GPT-OSS 120B",
        "condition": "Skill",
        "color": COLOR_SKILL,
    },
    "221920": {
        "dir": "20261116_221920",
        "model": "GPT-OSS 120B",
        "condition": "No skill",
        "color": COLOR_NOSKILL,
    },
    "231204": {
        "dir": "20261107_231204",
        "model": "Gemini 3.8 Flash",
        "condition": "Skill",
        "color": COLOR_SKILL,
    },
    "171051": {
        "dir": "20261116_171051",
        "model": "Gemini 3.8 Flash",
        "condition": "No skill",
        "color": COLOR_NOSKILL,
    },
}

# Load data from eval_results (excluding task 3: Elixir/SQLite PDF and task 6: Nix Install Guide)
EXCLUDE_TASK_INDICES = {3, 6}

run_data = {}
for rid, meta in RUNS.items():
    summary_path = eval_base / meta["dir"] / "benchmark_summary.json"
    with open(summary_path) as f:
        d = json.load(f)
    
    tasks = [t for i, t in enumerate(d["tasks"]) if i not in EXCLUDE_TASK_INDICES]
    p1 = [t["scores"]["pass@1"] * 100 for t in tasks]
    p3 = [t["scores"]["pass@3"] * 100 for t in tasks]
    task_mean_tokens = [
        sum(s["total_tokens"] for s in t["samples"]) / len(t["samples"])
        for t in tasks
    ]
    all_filtered_samples = [s for t in tasks for s in t["samples"]]
    
    trial_tokens = []
    trial_labels = []
    for t_idx, t in enumerate(tasks):
        for s_idx, s in enumerate(t["samples"]):
            trial_tokens.append(s["total_tokens"])
            trial_labels.append(f"T{t_idx}s{s_idx}")

    run_data[rid] = {
        **meta,
        "overall_pass1": sum(p1) / len(p1),
        "overall_pass3": sum(p3) / len(p3),
        "mean_tokens": sum(s["total_tokens"] for s in all_filtered_samples) / len(all_filtered_samples),
        "task_pass1": p1,
        "task_pass3": p3,
        "task_tokens": task_mean_tokens,
        "trial_tokens": trial_tokens,
        "trial_labels": trial_labels,
    }

def save_fig(fig, base_name: str):
    for ext in ["pdf", "png", "svg"]:
        out_path = figures_dir / f"{base_name}.{ext}"
        if ext == "png":
            fig.savefig(out_path, dpi=300, bbox_inches="tight")
        else:
            fig.savefig(out_path, bbox_inches="tight")
    print(f"Saved {base_name}.(pdf|png|svg)")
    plt.close(fig)

indices = np.arange(len(SHORT_TASK_NAMES))

# =============================================================================
# 1. Line Graphs of Accuracy (pass@1 & pass@3 by Task) for EACH Run ID
# =============================================================================
for rid, data in run_data.items():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
    
    # Alternate background shading
    for t in range(len(SHORT_TASK_NAMES)):
        if t % 2 == 1:
            ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Reference mean lines
    ax.axhline(data["overall_pass1"], color=COLOR_PASS1, linestyle="--", linewidth=1.2, alpha=0.75, zorder=2,
               label=f"Overall pass@1 Mean: {data['overall_pass1']:.2f}%")
    ax.axhline(data["overall_pass3"], color=COLOR_PASS3, linestyle=":", linewidth=1.2, alpha=0.75, zorder=2,
               label=f"Overall pass@3 Mean: {data['overall_pass3']:.2f}%")

    # Plot pass@1 and pass@3 lines
    ax.plot(indices, data["task_pass1"], marker="o", color=COLOR_PASS1, linewidth=2.2, markersize=7,
            label=f"pass@1 per Task", zorder=4)
    ax.plot(indices, data["task_pass3"], marker="^", linestyle="--", color=COLOR_PASS3, linewidth=2.0, markersize=7,
            label=f"pass@3 per Task", zorder=4)

    # Annotate points (with collision offsets)
    for i, (y1, y3) in enumerate(zip(data["task_pass1"], data["task_pass3"])):
        if abs(y1 - y3) < 0.1:
            # Shared value
            ax.annotate(f"{y1:.0f}%", (i, y1), textcoords="offset points", xytext=(0, 8),
                        ha="center", fontsize=8.2, fontweight="bold", color="#1f2937",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#cccccc", lw=0.6))
        else:
            ax.annotate(f"{y1:.0f}%", (i, y1), textcoords="offset points", xytext=(0, -14),
                        ha="center", fontsize=8.0, fontweight="bold", color=COLOR_PASS1,
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS1, lw=0.6))
            ax.annotate(f"{y3:.0f}%", (i, y3), textcoords="offset points", xytext=(0, 8),
                        ha="center", fontsize=8.0, fontweight="bold", color=COLOR_PASS3,
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS3, lw=0.6))

    ax.set_xticks(indices)
    ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
    ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
    ax.set_ylim(-6, 116)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(100.0, decimals=0))
    ax.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
    ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
    
    cond_desc = f"{data['model']} ({data['condition']}) — Run ID `{rid}`"
    ax.set_title(f"Run {rid}: Task-Level pass@1 and pass@3 Accuracy\n{cond_desc}", fontweight="bold", pad=12)
    
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#4b5563")
    ax.spines["bottom"].set_color("#4b5563")
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="lower left" if data["overall_pass1"] > 50 else "upper right", ncol=2)
    
    fig.tight_layout()
    save_fig(fig, f"document-run-{rid}-accuracy")


# =============================================================================
# 2. Line Graphs of Token Usage by Task for EACH Run ID
# =============================================================================
for rid, data in run_data.items():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
    
    # Alternate background shading
    for t in range(len(SHORT_TASK_NAMES)):
        if t % 2 == 1:
            ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Reference mean line
    ax.axhline(data["mean_tokens"], color="#6b7280", linestyle="--", linewidth=1.3, alpha=0.85, zorder=2,
               label=f"Run Mean: {int(data['mean_tokens']):,} tokens")

    # Plot token line
    ax.plot(indices, data["task_tokens"], marker="o", color=data["color"], linewidth=2.4, markersize=7.5,
            label=f"Mean Tokens per Task", zorder=4)

    # Annotate points
    max_tok = max(data["task_tokens"])
    min_tok = min(data["task_tokens"])
    y_range = max_tok - min_tok
    
    for i, tok in enumerate(data["task_tokens"]):
        ax.annotate(f"{int(tok):,}", (i, tok), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=8.0, fontweight="bold", color=data["color"],
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=data["color"], lw=0.6))

    ax.set_xticks(indices)
    ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
    ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
    
    # Headroom to avoid any text collision
    ax.set_ylim(min(0, min_tok * 0.8), max_tok * 1.25)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
    ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
    
    cond_desc = f"{data['model']} ({data['condition']}) — Run ID `{rid}`"
    ax.set_title(f"Run {rid}: Token Usage by Task\n{cond_desc}", fontweight="bold", pad=12)
    
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#4b5563")
    ax.spines["bottom"].set_color("#4b5563")
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper left")
    
    fig.tight_layout()
    save_fig(fig, f"document-run-{rid}-tokens")


# =============================================================================
# 3. Combined Dual-Panel Line Graphs (Accuracy & Tokens) for EACH Run ID
# =============================================================================
for rid, data in run_data.items():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 4.5), dpi=300)
    
    # Panel 1: Accuracy
    for t in range(len(SHORT_TASK_NAMES)):
        if t % 2 == 1:
            ax1.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    ax1.axhline(data["overall_pass1"], color=COLOR_PASS1, linestyle="--", linewidth=1.1, alpha=0.75, zorder=2,
                label=f"Mean pass@1: {data['overall_pass1']:.1f}%")
    ax1.axhline(data["overall_pass3"], color=COLOR_PASS3, linestyle=":", linewidth=1.1, alpha=0.75, zorder=2,
                label=f"Mean pass@3: {data['overall_pass3']:.1f}%")

    ax1.plot(indices, data["task_pass1"], marker="o", color=COLOR_PASS1, linewidth=2.0, markersize=6.5,
             label="pass@1", zorder=4)
    ax1.plot(indices, data["task_pass3"], marker="^", linestyle="--", color=COLOR_PASS3, linewidth=1.8, markersize=6.5,
             label="pass@3", zorder=4)

    ax1.set_xticks(indices)
    ax1.set_xticklabels([f"T{i}" for i in range(len(SHORT_TASK_NAMES))], fontsize=8.5)
    ax1.set_xlim(-0.5, len(SHORT_TASK_NAMES) - 0.5)
    ax1.set_ylim(-5, 115)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(100.0, decimals=0))
    ax1.set_ylabel("Pass Rate (%)", fontweight="bold")
    ax1.set_xlabel("Benchmark Task (T0 - T6)", fontweight="bold")
    ax1.set_title("(a) Synthesis Accuracy", fontweight="bold")
    ax1.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="lower left" if data["overall_pass1"] > 50 else "upper right")

    # Panel 2: Token Usage
    for t in range(len(SHORT_TASK_NAMES)):
        if t % 2 == 1:
            ax2.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    ax2.axhline(data["mean_tokens"], color="#6b7280", linestyle="--", linewidth=1.1, alpha=0.85, zorder=2,
                label=f"Mean: {int(data['mean_tokens']):,} tokens")

    ax2.plot(indices, data["task_tokens"], marker="s", color=data["color"], linewidth=2.0, markersize=6.5,
             label="Tokens per Task", zorder=4)

    for i, tok in enumerate(data["task_tokens"]):
        ax2.annotate(f"{int(tok):,}", (i, tok), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=7.5, fontweight="bold", color=data["color"],
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=data["color"], lw=0.5))

    ax2.set_xticks(indices)
    ax2.set_xticklabels([f"T{i}" for i in range(len(SHORT_TASK_NAMES))], fontsize=8.5)
    ax2.set_xlim(-0.5, len(SHORT_TASK_NAMES) - 0.5)
    max_tok = max(data["task_tokens"])
    min_tok = min(data["task_tokens"])
    ax2.set_ylim(min(0, min_tok * 0.8), max_tok * 1.25)
    ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax2.set_ylabel("Total Tokens Consumed", fontweight="bold")
    ax2.set_xlabel("Benchmark Task (T0 - T6)", fontweight="bold")
    ax2.set_title("(b) Token Consumption", fontweight="bold")
    ax2.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper left")

    fig.suptitle(f"Run ID `{rid}` ({data['model']}, {data['condition']}): Accuracy & Token Telemetry",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    save_fig(fig, f"document-run-{rid}-combined")


# =============================================================================
# 4. Cross-Run Task-by-Task Comparison Graphs
# =============================================================================
# 4a. GPT-OSS 120B Task-Level pass@1: Run 183227 (Skill) vs Run 221920 (No skill)
fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
for t in range(len(SHORT_TASK_NAMES)):
    if t % 2 == 1:
        ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

d_sk = run_data["183227"]
d_no = run_data["221920"]

ax.axhline(d_sk["overall_pass1"], color=COLOR_SKILL, linestyle="--", linewidth=1.2, alpha=0.8,
           label=f"Skill Mean: {d_sk['overall_pass1']:.1f}%")
ax.axhline(d_no["overall_pass1"], color=COLOR_NOSKILL, linestyle=":", linewidth=1.2, alpha=0.8,
           label=f"No-skill Mean: {d_no['overall_pass1']:.1f}%")

ax.plot(indices, d_sk["task_pass1"], marker="o", color=COLOR_SKILL, linewidth=2.2, markersize=7.5,
        label="Skill (Run `183227`)", zorder=4)
ax.plot(indices, d_no["task_pass1"], marker="s", linestyle="--", color=COLOR_NOSKILL, linewidth=2.0, markersize=7.0,
        label="No-skill (Run `221920`)", zorder=4)

ax.set_xticks(indices)
ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
ax.set_ylim(-6, 116)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(100.0, decimals=0))
ax.set_ylabel("pass@1 Rate (%)", fontweight="bold", labelpad=8)
ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
ax.set_title("Document Benchmark: GPT-OSS 120B pass@1 Across Tasks\nSkill (Run `183227`) vs. No-Skill (Run `221920`)",
             fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper left", ncol=2)
fig.tight_layout()
save_fig(fig, "document-runs-gpt-oss-120b-pass1-comparison")

# 4b. GPT-OSS 120B Task-Level pass@3: Run 183227 (Skill) vs Run 221920 (No skill)
fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
for t in range(len(SHORT_TASK_NAMES)):
    if t % 2 == 1:
        ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

ax.axhline(d_sk["overall_pass3"], color=COLOR_SKILL, linestyle="--", linewidth=1.2, alpha=0.8,
           label=f"Skill Mean: {d_sk['overall_pass3']:.1f}%")
ax.axhline(d_no["overall_pass3"], color=COLOR_NOSKILL, linestyle=":", linewidth=1.2, alpha=0.8,
           label=f"No-skill Mean: {d_no['overall_pass3']:.1f}%")

ax.plot(indices, d_sk["task_pass3"], marker="o", color=COLOR_SKILL, linewidth=2.2, markersize=7.5,
        label="Skill (Run `183227`)", zorder=4)
ax.plot(indices, d_no["task_pass3"], marker="s", linestyle="--", color=COLOR_NOSKILL, linewidth=2.0, markersize=7.0,
        label="No-skill (Run `221920`)", zorder=4)

ax.set_xticks(indices)
ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
ax.set_ylim(-6, 116)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(100.0, decimals=0))
ax.set_ylabel("pass@3 Rate (%)", fontweight="bold", labelpad=8)
ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
ax.set_title("Document Benchmark: GPT-OSS 120B pass@3 Across Tasks\nSkill (Run `183227`) vs. No-Skill (Run `221920`)",
             fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper left", ncol=2)
fig.tight_layout()
save_fig(fig, "document-runs-gpt-oss-120b-pass3-comparison")

# 4c. GPT-OSS 120B Task-Level Tokens: Run 183227 (Skill) vs Run 221920 (No skill)
fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
for t in range(len(SHORT_TASK_NAMES)):
    if t % 2 == 1:
        ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

ax.plot(indices, d_sk["task_tokens"], marker="o", color=COLOR_SKILL, linewidth=2.2, markersize=7.5,
        label="Skill (Run `183227`)", zorder=4)
ax.plot(indices, d_no["task_tokens"], marker="s", linestyle="--", color=COLOR_NOSKILL, linewidth=2.0, markersize=7.0,
        label="No-skill (Run `221920`)", zorder=4)

ax.set_xticks(indices)
ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
ax.set_ylim(0, 68000)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
ax.set_title("Document Benchmark: GPT-OSS 120B Token Usage by Task\nSkill (Run `183227`) vs. No-Skill (Run `221920`)",
             fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper left", ncol=2)
fig.tight_layout()
save_fig(fig, "document-runs-gpt-oss-120b-tokens-comparison")

# 4d. Gemini Task-Level Tokens: Run 231204 (Skill) vs Run 171051 (No skill)
fig, ax = plt.subplots(figsize=(10.5, 4.4), dpi=300)
for t in range(len(SHORT_TASK_NAMES)):
    if t % 2 == 1:
        ax.axvspan(t - 0.5, t + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

d_gem_sk = run_data["231204"]
d_gem_no = run_data["171051"]

ax.plot(indices, d_gem_sk["task_tokens"], marker="o", color=COLOR_SKILL, linewidth=2.2, markersize=7.5,
        label="Skill (Run `231204`)", zorder=4)
ax.plot(indices, d_gem_no["task_tokens"], marker="s", linestyle="--", color=COLOR_NOSKILL, linewidth=2.0, markersize=7.0,
        label="No-skill (Run `171051`)", zorder=4)

ax.set_xticks(indices)
ax.set_xticklabels(SHORT_TASK_NAMES, fontsize=8.5)
ax.set_xlim(-0.6, len(SHORT_TASK_NAMES) - 0.4)
ax.set_ylim(80000, 390000)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax.set_xlabel("Document Benchmark Task", fontweight="bold", labelpad=8)
ax.set_title("Document Benchmark: Gemini 3.8 Flash Token Usage by Task\nSkill (Run `231204`) vs. No-Skill (Run `171051`)",
             fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cccccc", loc="upper right", ncol=2)
fig.tight_layout()
save_fig(fig, "document-runs-gemini-tokens-comparison")

print("All Run ID graphs generated successfully!")
