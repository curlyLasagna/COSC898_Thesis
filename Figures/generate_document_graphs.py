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
Generate publication-quality line graphs comparing pass@1 and pass@3 across
Skill and No-Skill conditions for GPT-OSS 120B and Gemini.
All output files are prefixed with 'document'.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

figures_dir = Path("/Users/luis/Documents/Thesis_Submission/Figures")
figures_dir.mkdir(parents=True, exist_ok=True)

# Publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.titlesize": 14,
    "lines.linewidth": 2.5,
    "lines.markersize": 8,
})

# Color palette
COLOR_SKILL = "#0969da"     # Royal Blue
COLOR_NOSKILL = "#cf222e"   # Crimson / Coral Red
COLOR_PASS1 = "#2da44e"     # Forest Green
COLOR_PASS3 = "#8250df"     # Purple
GRID_COLOR = "#e5e7eb"

# -----------------------------------------------------------------------------
# Data Definition (Filtered: 7 Tasks, excluding Elixir/SQLite PDF & Nix Install Guide)
# -----------------------------------------------------------------------------
# GPT-OSS 120B: Skill (Run 183227): pass@1=66.67%, pass@3=85.71%, tokens=32,679
# GPT-OSS 120B: No skill (Run 221920): pass@1=9.52%, pass@3=28.57%, tokens=27,303
# Gemini: Skill (Run 231204): pass@1=100.0%, pass@3=100.0%, tokens=204,211
# Gemini: No skill (Run 171051): pass@1=100.0%, pass@3=100.0%, tokens=207,859

data = {
    "GPT-OSS 120B": {
        "Skill": {"pass@1": 66.67, "pass@3": 85.71, "tokens": 32679, "run_id": "183227"},
        "No skill": {"pass@1": 9.52, "pass@3": 28.57, "tokens": 27303, "run_id": "221920"},
    },
    "Gemini": {
        "Skill": {"pass@1": 100.0, "pass@3": 100.0, "tokens": 204211, "run_id": "231204"},
        "No skill": {"pass@1": 100.0, "pass@3": 100.0, "tokens": 207859, "run_id": "171051"},
    }
}

def style_spines_and_grid(ax):
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
    ax.grid(axis="x", color=GRID_COLOR, linestyle=":", linewidth=0.6, alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#4b5563")
    ax.spines["bottom"].set_color("#4b5563")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(100.0, decimals=0))
    ax.set_ylim(-2, 108)
    ax.set_yticks([0, 20, 40, 60, 80, 100])


# =============================================================================
# Graph 1: GPT-OSS-120B - pass@1 & pass@3 (x-axis: Metric k, lines: Skill vs No-skill)
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
x_vals = [1, 3]
x_labels = ["pass@1", "pass@3"]

# Skill line
y_skill = [data["GPT-OSS 120B"]["Skill"]["pass@1"], data["GPT-OSS 120B"]["Skill"]["pass@3"]]
ax.plot(x_vals, y_skill, marker="o", color=COLOR_SKILL, label="With Custom Skill (Run 183227)", zorder=4)
for x, y in zip(x_vals, y_skill):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color=COLOR_SKILL,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_SKILL, alpha=0.9, lw=0.8))

# No skill line
y_noskill = [data["GPT-OSS 120B"]["No skill"]["pass@1"], data["GPT-OSS 120B"]["No skill"]["pass@3"]]
ax.plot(x_vals, y_noskill, marker="s", linestyle="--", color=COLOR_NOSKILL, label="No Skill / Baseline (Run 221920)", zorder=4)
for x, y in zip(x_vals, y_noskill):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, -18),
                ha="center", fontweight="bold", color=COLOR_NOSKILL,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_NOSKILL, alpha=0.9, lw=0.8))

ax.set_xticks(x_vals)
ax.set_xticklabels(x_labels, fontweight="bold")
ax.set_xlabel("Evaluation Metric", fontweight="bold", labelpad=8)
ax.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("GPT-OSS 120B: pass@1 and pass@3\n(Skill vs. No-Skill Comparison)", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="upper left")
style_spines_and_grid(ax)
ax.set_xlim(0.7, 3.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gpt-oss-120b-pass-at-k.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gpt-oss-120b-pass-at-k")


# =============================================================================
# Graph 2: Gemini - pass@1 & pass@3 (x-axis: Metric k, lines: Skill vs No-skill)
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)

y_gemini_skill = [data["Gemini"]["Skill"]["pass@1"], data["Gemini"]["Skill"]["pass@3"]]
y_gemini_noskill = [data["Gemini"]["No skill"]["pass@1"], data["Gemini"]["No skill"]["pass@3"]]

# Slight visual separation or double styling since both are exactly 100%
ax.plot(x_vals, y_gemini_skill, marker="o", color=COLOR_SKILL, linewidth=3.5,
        label="With Custom Skill (Run 231204)", zorder=3)
ax.plot(x_vals, y_gemini_noskill, marker="s", linestyle=":", color=COLOR_NOSKILL, linewidth=2.0,
        label="No Skill / Baseline (Run 171051)", zorder=4)

ax.annotate("100.0% (Both Skill & No Skill)", (1, 100), textcoords="offset points", xytext=(0, 9),
            ha="center", fontweight="bold", color="#1f2937",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))
ax.annotate("100.0% (Both Skill & No Skill)", (3, 100), textcoords="offset points", xytext=(0, 9),
            ha="center", fontweight="bold", color="#1f2937",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))

ax.set_xticks(x_vals)
ax.set_xticklabels(x_labels, fontweight="bold")
ax.set_xlabel("Evaluation Metric", fontweight="bold", labelpad=8)
ax.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("Gemini 3.8 Flash: pass@1 and pass@3\n(Skill vs. No-Skill Comparison)", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="lower right")
style_spines_and_grid(ax)
ax.set_xlim(0.7, 3.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gemini-pass-at-k.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gemini-pass-at-k")


# =============================================================================
# Graph 3: GPT-OSS-120B - Progression across Condition (x-axis: No-skill -> Skill)
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
c_vals = [0, 1]
c_labels = ["No Skill\n(Run 221920)", "Skill\n(Run 183227)"]

# pass@1 line
p1_gpt = [data["GPT-OSS 120B"]["No skill"]["pass@1"], data["GPT-OSS 120B"]["Skill"]["pass@1"]]
ax.plot(c_vals, p1_gpt, marker="o", color=COLOR_PASS1, label="pass@1", zorder=4)
for x, y in zip(c_vals, p1_gpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, -18 if x == 0 else -18),
                ha="center", fontweight="bold", color=COLOR_PASS1,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS1, alpha=0.9, lw=0.8))

# pass@3 line
p3_gpt = [data["GPT-OSS 120B"]["No skill"]["pass@3"], data["GPT-OSS 120B"]["Skill"]["pass@3"]]
ax.plot(c_vals, p3_gpt, marker="^", linestyle="--", color=COLOR_PASS3, label="pass@3", zorder=4)
for x, y in zip(c_vals, p3_gpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color=COLOR_PASS3,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS3, alpha=0.9, lw=0.8))

# Annotate Delta / Gain (positioned cleanly in lower right to avoid colliding with trend lines)
gain_p1 = p1_gpt[1] - p1_gpt[0]
gain_p3 = p3_gpt[1] - p3_gpt[0]
ax.text(0.72, 20, f"Δ pass@1: +{gain_p1:.2f}%\nΔ pass@3: +{gain_p3:.2f}%",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1f2937",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ecfdf5", edgecolor="#10b981", alpha=0.95))

ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels, fontweight="bold")
ax.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("GPT-OSS 120B: Impact of Custom Skill on Pass Rate", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="upper left")
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gpt-oss-120b-by-condition.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gpt-oss-120b-by-condition")


# =============================================================================
# Graph 4: Gemini - Progression across Condition (x-axis: No-skill -> Skill)
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
c_labels_gemini = ["No Skill\n(Run 171051)", "Skill\n(Run 231204)"]

p1_gemini = [data["Gemini"]["No skill"]["pass@1"], data["Gemini"]["Skill"]["pass@1"]]
p3_gemini = [data["Gemini"]["No skill"]["pass@3"], data["Gemini"]["Skill"]["pass@3"]]

ax.plot(c_vals, p1_gemini, marker="o", color=COLOR_PASS1, linewidth=3.5, label="pass@1", zorder=3)
ax.plot(c_vals, p3_gemini, marker="^", linestyle=":", color=COLOR_PASS3, linewidth=2.0, label="pass@3", zorder=4)

ax.annotate("100.0%", (0, 100), textcoords="offset points", xytext=(0, 9),
            ha="center", fontweight="bold", color="#1f2937",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))
ax.annotate("100.0%", (1, 100), textcoords="offset points", xytext=(0, 9),
            ha="center", fontweight="bold", color="#1f2937",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))

ax.text(0.5, 50, "Perfect Ceiling Performance\npass@1 = pass@3 = 100.0%\nAcross both conditions",
        ha="center", va="center", fontsize=11, fontweight="bold", color="#374151",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#f3f4f6", edgecolor="#9ca3af", alpha=0.9))

ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_gemini, fontweight="bold")
ax.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("Gemini 3.8 Flash: Impact of Custom Skill on Pass Rate", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="lower right")
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gemini-by-condition.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gemini-by-condition")


# =============================================================================
# Graph 5 & 6: Separate pass@1 and pass@3 line graphs for each model
# =============================================================================
# 5a. GPT-OSS 120B pass@1
fig, ax = plt.subplots(figsize=(5.8, 4.4), dpi=300)
ax.plot(c_vals, p1_gpt, marker="o", color=COLOR_PASS1, linewidth=2.8, zorder=4)
for x, y in zip(c_vals, p1_gpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color=COLOR_PASS1,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS1, lw=0.8))
ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels, fontweight="bold")
ax.set_xlabel("Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("pass@1 Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("GPT-OSS 120B: pass@1 (Skill vs. No-Skill)", fontweight="bold", pad=12)
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()
for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gpt-oss-120b-pass1.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gpt-oss-120b-pass1")

# 5b. GPT-OSS 120B pass@3
fig, ax = plt.subplots(figsize=(5.8, 4.4), dpi=300)
ax.plot(c_vals, p3_gpt, marker="^", color=COLOR_PASS3, linewidth=2.8, zorder=4)
for x, y in zip(c_vals, p3_gpt):
    ax.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color=COLOR_PASS3,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS3, lw=0.8))
ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels, fontweight="bold")
ax.set_xlabel("Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("pass@3 Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("GPT-OSS 120B: pass@3 (Skill vs. No-Skill)", fontweight="bold", pad=12)
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()
for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gpt-oss-120b-pass3.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gpt-oss-120b-pass3")

# 6a. Gemini pass@1
fig, ax = plt.subplots(figsize=(5.8, 4.4), dpi=300)
ax.plot(c_vals, p1_gemini, marker="o", color=COLOR_PASS1, linewidth=2.8, zorder=4)
for x, y in zip(c_vals, p1_gemini):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 9),
                ha="center", fontweight="bold", color=COLOR_PASS1,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS1, lw=0.8))
ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_gemini, fontweight="bold")
ax.set_xlabel("Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("pass@1 Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("Gemini 3.8 Flash: pass@1 (Skill vs. No-Skill)", fontweight="bold", pad=12)
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()
for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gemini-pass1.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gemini-pass1")

# 6b. Gemini pass@3
fig, ax = plt.subplots(figsize=(5.8, 4.4), dpi=300)
ax.plot(c_vals, p3_gemini, marker="^", color=COLOR_PASS3, linewidth=2.8, zorder=4)
for x, y in zip(c_vals, p3_gemini):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 9),
                ha="center", fontweight="bold", color=COLOR_PASS3,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_PASS3, lw=0.8))
ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_gemini, fontweight="bold")
ax.set_xlabel("Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("pass@3 Rate (%)", fontweight="bold", labelpad=8)
ax.set_title("Gemini 3.8 Flash: pass@3 (Skill vs. No-Skill)", fontweight="bold", pad=12)
style_spines_and_grid(ax)
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()
for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gemini-pass3.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gemini-pass3")


# =============================================================================
# Graph 7: Comprehensive 2-Panel Side-by-Side Comparison
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), dpi=300, sharey=True)

# Subplot 1: GPT-OSS 120B
ax1.plot(x_vals, y_skill, marker="o", color=COLOR_SKILL, label="Skill (Run 183227)", zorder=4)
for x, y in zip(x_vals, y_skill):
    ax1.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 10),
                 ha="center", fontweight="bold", color=COLOR_SKILL,
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_SKILL, lw=0.8))

ax1.plot(x_vals, y_noskill, marker="s", linestyle="--", color=COLOR_NOSKILL, label="No skill (Run 221920)", zorder=4)
for x, y in zip(x_vals, y_noskill):
    ax1.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, -18),
                 ha="center", fontweight="bold", color=COLOR_NOSKILL,
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOR_NOSKILL, lw=0.8))

ax1.set_xticks(x_vals)
ax1.set_xticklabels(x_labels, fontweight="bold")
ax1.set_xlabel("Evaluation Metric", fontweight="bold", labelpad=8)
ax1.set_ylabel("Pass Rate (%)", fontweight="bold", labelpad=8)
ax1.set_title("(a) GPT-OSS 120B (Local)", fontweight="bold", pad=10)
ax1.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="upper left")
style_spines_and_grid(ax1)
ax1.set_xlim(0.7, 3.3)

# Subplot 2: Gemini
ax2.plot(x_vals, y_gemini_skill, marker="o", color=COLOR_SKILL, linewidth=3.5, label="Skill (Run 231204)", zorder=3)
ax2.plot(x_vals, y_gemini_noskill, marker="s", linestyle=":", color=COLOR_NOSKILL, linewidth=2.0, label="No skill (Run 171051)", zorder=4)

ax2.annotate("100.0% (Both Conditions)", (1, 100), textcoords="offset points", xytext=(0, 9),
             ha="center", fontweight="bold", color="#1f2937",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))
ax2.annotate("100.0% (Both Conditions)", (3, 100), textcoords="offset points", xytext=(0, 9),
             ha="center", fontweight="bold", color="#1f2937",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#f3f4f6", edgecolor="#9ca3af", lw=0.8))

ax2.set_xticks(x_vals)
ax2.set_xticklabels(x_labels, fontweight="bold")
ax2.set_xlabel("Evaluation Metric", fontweight="bold", labelpad=8)
ax2.set_title("(b) Gemini 3.8 Flash (Frontier API)", fontweight="bold", pad=10)
ax2.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="lower right")
style_spines_and_grid(ax2)
ax2.set_xlim(0.7, 3.3)

fig.suptitle("Comparison of pass@1 and pass@3 Accuracy: Skill vs. No-Skill", fontweight="bold", y=1.02)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-model-comparison-pass-at-k.{ext}", dpi=300)
plt.close(fig)
print("Saved document-model-comparison-pass-at-k")


# =============================================================================
# Graph 8: Token Usage - Combined Side-by-Side Dual Panels
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), dpi=300)

tok_gpt = [data["GPT-OSS 120B"]["No skill"]["tokens"], data["GPT-OSS 120B"]["Skill"]["tokens"]]
tok_gemini = [data["Gemini"]["No skill"]["tokens"], data["Gemini"]["Skill"]["tokens"]]

c_vals = [0, 1]
c_labels_gpt = ["No Skill\n(Run 221920)", "Skill\n(Run 183227)"]
c_labels_gem = ["No Skill\n(Run 171051)", "Skill\n(Run 231204)"]

# Panel 1: GPT-OSS 120B
ax1.plot(c_vals, tok_gpt, marker="o", color="#d95f02", linewidth=2.8, markersize=8, zorder=4)
for x, y in zip(c_vals, tok_gpt):
    ax1.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10 if x == 1 else -18),
                 ha="center", fontweight="bold", color="#d95f02",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#d95f02", lw=0.8))

delta_gpt = tok_gpt[1] - tok_gpt[0]
pct_gpt = (delta_gpt / tok_gpt[0]) * 100
ax1.text(0.5, 36000, f"Δ: +{delta_gpt:,} tokens\n(+{pct_gpt:.1f}%)",
         ha="center", va="center", fontsize=10.5, fontweight="bold", color="#9a3412",
         bbox=dict(boxstyle="round,pad=0.45", facecolor="#fff7ed", edgecolor="#fdba74", lw=0.8))

ax1.set_xticks(c_vals)
ax1.set_xticklabels(c_labels_gpt, fontweight="bold")
ax1.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax1.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax1.set_title("(a) GPT-OSS 120B", fontweight="bold", pad=10)
ax1.set_ylim(20000, 38000)
ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax1.set_axisbelow(True)
ax1.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color("#4b5563")
ax1.spines["bottom"].set_color("#4b5563")
ax1.set_xlim(-0.3, 1.3)

# Panel 2: Gemini 3.8 Flash
ax2.plot(c_vals, tok_gemini, marker="s", color="#2b5c8f", linewidth=2.8, markersize=8, zorder=4)
for x, y in zip(c_vals, tok_gemini):
    ax2.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10 if x == 1 else -18),
                 ha="center", fontweight="bold", color="#2b5c8f",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#2b5c8f", lw=0.8))

delta_gem = tok_gemini[1] - tok_gemini[0]
pct_gem = (delta_gem / tok_gemini[0]) * 100
gem_sign = "+" if delta_gem >= 0 else ""
ax2.text(0.5, 212000, f"Δ: {gem_sign}{delta_gem:,} tokens\n({gem_sign}{pct_gem:.2f}%)",
         ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1e40af",
         bbox=dict(boxstyle="round,pad=0.45", facecolor="#eff6ff", edgecolor="#93c5fd", lw=0.8))

ax2.set_xticks(c_vals)
ax2.set_xticklabels(c_labels_gem, fontweight="bold")
ax2.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax2.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax2.set_title("(b) Gemini 3.8 Flash", fontweight="bold", pad=10)
ax2.set_ylim(195000, 215000)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax2.set_axisbelow(True)
ax2.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color("#4b5563")
ax2.spines["bottom"].set_color("#4b5563")
ax2.set_xlim(-0.3, 1.3)

fig.suptitle("Total Token Usage Across Conditions: Skill vs. No-Skill", fontweight="bold", y=1.02)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-tokens-comparison-panels.{ext}", dpi=300)
plt.close(fig)
print("Saved document-tokens-comparison-panels")


# =============================================================================
# Graph 9: Token Usage - Dedicated GPT-OSS 120B Line Graph
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
ax.plot(c_vals, tok_gpt, marker="o", color="#d95f02", linewidth=2.8, markersize=8, zorder=4)
for x, y in zip(c_vals, tok_gpt):
    ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10 if x == 1 else -18),
                ha="center", fontweight="bold", color="#d95f02",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#d95f02", lw=0.8))

ax.text(0.5, 36000, f"Δ: +{delta_gpt:,} tokens\n(+{pct_gpt:.1f}%)",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#9a3412",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#fff7ed", edgecolor="#fdba74", lw=0.8))

ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_gpt, fontweight="bold")
ax.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax.set_title("GPT-OSS 120B: Token Usage (Skill vs. No-Skill)", fontweight="bold", pad=12)
ax.set_ylim(20000, 38000)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax.set_axisbelow(True)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#4b5563")
ax.spines["bottom"].set_color("#4b5563")
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gpt-oss-120b-tokens.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gpt-oss-120b-tokens")


# =============================================================================
# Graph 10: Token Usage - Dedicated Gemini Line Graph
# =============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
ax.plot(c_vals, tok_gemini, marker="s", color="#2b5c8f", linewidth=2.8, markersize=8, zorder=4)
for x, y in zip(c_vals, tok_gemini):
    ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10 if x == 1 else -18),
                ha="center", fontweight="bold", color="#2b5c8f",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#2b5c8f", lw=0.8))

ax.text(0.5, 212000, f"Δ: {gem_sign}{delta_gem:,} tokens\n({gem_sign}{pct_gem:.2f}%)",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1e40af",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#eff6ff", edgecolor="#93c5fd", lw=0.8))

ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_gem, fontweight="bold")
ax.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("Total Tokens Consumed", fontweight="bold", labelpad=8)
ax.set_title("Gemini 3.8 Flash: Token Usage (Skill vs. No-Skill)", fontweight="bold", pad=12)
ax.set_ylim(195000, 215000)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
ax.set_axisbelow(True)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#4b5563")
ax.spines["bottom"].set_color("#4b5563")
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-gemini-tokens.{ext}", dpi=300)
plt.close(fig)
print("Saved document-gemini-tokens")


# =============================================================================
# Graph 11: Token Usage - Unified Comparison on Log Scale
# =============================================================================
fig, ax = plt.subplots(figsize=(7.0, 5.0), dpi=300)
c_labels_unified = ["No Skill", "Skill"]

ax.plot(c_vals, tok_gemini, marker="s", color="#2b5c8f", linewidth=2.5, markersize=8,
        label="Gemini 3.8 Flash (Frontier)", zorder=4)
ax.plot(c_vals, tok_gpt, marker="o", color="#d95f02", linewidth=2.5, markersize=8,
        label="GPT-OSS 120B (Local)", zorder=4)

for x, y in zip(c_vals, tok_gemini):
    ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color="#2b5c8f",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#2b5c8f", lw=0.8))

for x, y in zip(c_vals, tok_gpt):
    ax.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontweight="bold", color="#d95f02",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#d95f02", lw=0.8))

ax.set_yscale("log")
ax.set_ylim(10000, 350000)
ax.set_yticks([10000, 20000, 50000, 100000, 200000, 300000])
ax.get_yaxis().set_major_formatter(mtick.ScalarFormatter())
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))

ax.set_xticks(c_vals)
ax.set_xticklabels(c_labels_unified, fontweight="bold")
ax.set_xlabel("Experimental Condition", fontweight="bold", labelpad=8)
ax.set_ylabel("Total Tokens Consumed (Log Scale)", fontweight="bold", labelpad=8)
ax.set_title("Token Usage Comparison: Gemini vs. GPT-OSS 120B\n(Skill vs. No-Skill)", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="#f9fafb", edgecolor="#e5e7eb", loc="center left")
ax.set_axisbelow(True)
ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.85)
ax.grid(axis="x", color=GRID_COLOR, linestyle=":", linewidth=0.6, alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#4b5563")
ax.spines["bottom"].set_color("#4b5563")
ax.set_xlim(-0.3, 1.3)
fig.tight_layout()

for ext in ["png", "pdf", "svg"]:
    fig.savefig(figures_dir / f"document-token-usage-logscale.{ext}", dpi=300)
    fig.savefig(figures_dir / f"document-token-usage.{ext}", dpi=300)
plt.close(fig)
print("Saved document-token-usage & document-token-usage-logscale")

