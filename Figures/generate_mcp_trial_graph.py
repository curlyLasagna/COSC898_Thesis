#!/usr/bin/env python3
"""
Generate publication-quality figure comparing MCP tool calls across benchmark trials
between Gemini 3.8 Flash (eval run 20261031_113621) and GPT-OSS 120B (eval run 20261101_161538).
Omits subplot (b) to focus exclusively on the trial-by-trial breakdown.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paths
base_eval_dir = Path("/Users/luis/Code/Thesis_Implementation/eval_results")
figures_dir = Path("/Users/luis/Documents/Thesis_Submission/Figures")
figures_dir.mkdir(parents=True, exist_ok=True)

f_gemini = base_eval_dir / "20261031_113621" / "tool_call_frequency_by_trial.csv"
f_gpt = base_eval_dir / "20261101_161538" / "tool_call_frequency_by_trial.csv"

# Load datasets
df_gemini = pd.read_csv(f_gemini)[["task", "sample", "call_mcp_tool"]].rename(
    columns={"call_mcp_tool": "gemini_mcp"}
)
df_gpt = pd.read_csv(f_gpt)[["task", "sample", "call_mcp_tool", "list_resources"]].rename(
    columns={"call_mcp_tool": "gpt_mcp", "list_resources": "gpt_list_res"}
)

task_names = [
    "Java 17", "Flutter", "Python", "GCC", "Clang",
    "Node.js", "Rust", "Go", ".NET SDK", "Ruby",
    "R", "RStudio", "MySQL", "Workbench"
]

all_trials = []
for t in range(14):
    for s in range(3):
        all_trials.append({
            "task": f"task_{t:02d}",
            "sample": f"sample_{s:02d}",
            "trial_idx": t * 3 + s,
            "task_num": t,
            "task_name": task_names[t],
            "sample_num": s,
            "sample_label": f"s{s}"
        })

df = pd.DataFrame(all_trials)
df = df.merge(df_gemini, on=["task", "sample"], how="left")
df = df.merge(df_gpt, on=["task", "sample"], how="left")

# Set up publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 13,
})

fig, ax = plt.subplots(figsize=(11.5, 4.2), dpi=300)

# Colors
color_gemini = "#2b5c8f"  # Slate / Steel Blue
color_gpt = "#d95f02"     # Rust / Ochre Orange
bg_shade = "#f4f5f8"      # Light neutral for alternating task blocks

indices = np.arange(len(df))
bar_width = 0.38

# Alternate shading for task blocks (every 3 trials)
for t in range(14):
    if t % 2 == 1:
        ax.axvspan(t * 3 - 0.5, t * 3 + 2.5, color=bg_shade, alpha=0.95, zorder=0)

# Plot bars
bars_gemini = ax.bar(
    indices - bar_width / 2,
    df["gemini_mcp"].fillna(0),
    width=bar_width,
    color=color_gemini,
    label="Gemini 3.8 Flash (Mean: 3.40)",
    edgecolor="none",
    zorder=3
)

bars_gpt = ax.bar(
    indices + bar_width / 2,
    df["gpt_mcp"].fillna(0),
    width=bar_width,
    color=color_gpt,
    label="GPT-OSS 120B (Mean: 0.15)",
    edgecolor="none",
    zorder=3
)

# Annotate non-zero GPT-OSS values
for idx, val in enumerate(df["gpt_mcp"]):
    if val > 0:
        ax.text(
            idx + bar_width / 2,
            val + 0.25,
            f"{int(val)}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=color_gpt
        )

# Mark missing trials (N/A)
missing_gemini = df[df["gemini_mcp"].isna()]["trial_idx"]
for m_idx in missing_gemini:
    ax.text(m_idx - bar_width / 2, 0.25, "N/A", ha="center", va="bottom", fontsize=7.5, color="#777777", rotation=90)

missing_gpt = df[df["gpt_mcp"].isna()]["trial_idx"]
for m_idx in missing_gpt:
    ax.text(m_idx + bar_width / 2, 0.25, "N/A", ha="center", va="bottom", fontsize=7.5, color="#777777", rotation=90)

# Reference lines for mean
gemini_mean = df_gemini["gemini_mcp"].mean()
gpt_mean = df_gpt["gpt_mcp"].mean()

ax.axhline(gemini_mean, color=color_gemini, linestyle="--", linewidth=1.2, alpha=0.85, zorder=4)
ax.axhline(gpt_mean, color=color_gpt, linestyle=":", linewidth=1.2, alpha=0.85, zorder=4)

ax.set_xlim(-0.7, len(df) - 0.3)
ax.set_ylim(0, 10.5)
ax.set_ylabel("Number of MCP Tool Calls")
ax.set_title("MCP Tool Invocations Across 42 Benchmark Trials", fontweight="bold", pad=10)
ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)

# Task block center ticks & labels
task_centers = [t * 3 + 1 for t in range(14)]
ax.set_xticks(task_centers)
ax.set_xticklabels([f"T{t}\n{name}" for t, name in enumerate(task_names)], fontsize=8.2)
ax.tick_params(axis="x", length=0, pad=5)

ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

plt.tight_layout()

# Save in multiple formats
pdf_path = figures_dir / "mcp-calls-by-trial.pdf"
png_path = figures_dir / "mcp-calls-by-trial.png"
svg_path = figures_dir / "mcp-calls-by-trial.svg"

fig.savefig(str(pdf_path), bbox_inches="tight")
fig.savefig(str(png_path), dpi=300, bbox_inches="tight")
fig.savefig(str(svg_path), bbox_inches="tight")
plt.close(fig)

print(f"Generated {pdf_path}, {png_path}, and {svg_path}")
