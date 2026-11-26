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
Generate publication-quality line graphs comparing synthesis performance (pass@1 and pass@3)
across existing coursework codebases for:
1. GPT-OSS 120B (Skill vs. No-skill)
2. Gemini 3.8 Flash (Skill vs. No-skill)

Outputs all figures to Figures/ with prefix 'codebase-' in PDF, PNG, and SVG formats.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Output directory
figures_dir = Path(__file__).resolve().parent

# Set publication styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.5,
    "figure.titlesize": 13,
})

# Task definitions and data
tasks = [
    "AI-Assignments",
    "OS",
    "Labs",
    "DS",
    "Mobile",
    "Neural",
    "ProgrammingLang",
    "Sockets",
]
task_x = np.arange(len(tasks))

# GPT-OSS 120B data
# Run 004127 (Skill): pass@1 = 50.00%, pass@3 = 75.00%
gpt_skill_pass1 = [33.33, 100.0, 66.67, 66.67, 0.0, 100.0, 0.0, 33.33]
gpt_skill_pass3 = [100.0, 100.0, 100.0, 100.0, 0.0, 100.0, 0.0, 100.0]
gpt_skill_overall_p1 = 50.00
gpt_skill_overall_p3 = 75.00

# Run 104042 (No skill): pass@1 = 16.67%, pass@3 = 50.00%
gpt_noskill_pass1 = [0.0, 0.0, 0.0, 33.33, 33.33, 0.0, 33.33, 33.33]
gpt_noskill_pass3 = [0.0, 0.0, 0.0, 100.0, 100.0, 0.0, 100.0, 100.0]
gpt_noskill_overall_p1 = 16.67
gpt_noskill_overall_p3 = 50.00

# Gemini data
# Run 164549 (Skill): pass@1 = 91.67%, pass@3 = 100.0%
gemini_skill_pass1 = [100.0, 100.0, 100.0, 100.0, 33.33, 100.0, 100.0, 100.0]
gemini_skill_pass3 = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
gemini_skill_overall_p1 = 91.67
gemini_skill_overall_p3 = 100.00

# Run 190315 (No skill): pass@1 = 100.0%, pass@3 = 100.0%
gemini_noskill_pass1 = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
gemini_noskill_pass3 = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
gemini_noskill_overall_p1 = 100.00
gemini_noskill_overall_p3 = 100.00

# Styling constants
COLOR_SKILL = "#2b5c8f"    # Slate / Steel Blue
COLOR_NOSKILL = "#d95f02"  # Rust / Ochre Orange
BG_SHADE = "#f7f8fa"       # Alternating task band


def save_plot(fig, stem: str):
    """Save figure in PDF, PNG, and SVG formats."""
    stems = [stem]
    if "gpt-oss-120b" in stem:
        stems.append(stem.replace("gpt-oss-120b", "gpt-oss"))

    for s in stems:
        for ext in [".pdf", ".png", ".svg"]:
            out_path = figures_dir / f"{s}{ext}"
            fig.savefig(out_path, dpi=300, bbox_inches="tight")
        print(f"Saved {s}.[pdf|png|svg]")


def plot_single_metric_comparison(
    metric_name: str,
    model_name: str,
    skill_vals: list,
    noskill_vals: list,
    skill_mean: float,
    noskill_mean: float,
    stem: str,
):
    """Plot a single pass@k line comparison (Skill vs. No-skill) across 8 codebase tasks."""
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=300)

    # Shaded alternating task background
    for i in range(len(tasks)):
        if i % 2 == 1:
            ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # Plot lines & markers
    ax.plot(
        task_x,
        skill_vals,
        color=COLOR_SKILL,
        linestyle="-",
        linewidth=2.2,
        marker="o",
        markersize=7.5,
        label=f"Skill (Mean: {skill_mean:.1f}%)",
        zorder=4,
    )
    ax.plot(
        task_x,
        noskill_vals,
        color=COLOR_NOSKILL,
        linestyle="--",
        linewidth=2.0,
        marker="s",
        markersize=7,
        label=f"No Skill (Mean: {noskill_mean:.1f}%)",
        zorder=3,
    )

    # Horizontal mean benchmark lines
    ax.axhline(
        skill_mean,
        color=COLOR_SKILL,
        linestyle=":",
        linewidth=1.2,
        alpha=0.75,
        zorder=2,
    )
    ax.axhline(
        noskill_mean,
        color=COLOR_NOSKILL,
        linestyle=":",
        linewidth=1.2,
        alpha=0.75,
        zorder=2,
    )

    # Value annotations with collision prevention
    for i in range(len(tasks)):
        s_val = skill_vals[i]
        ns_val = noskill_vals[i]

        if abs(s_val - ns_val) < 8:
            # Overlapping or very close points
            ax.text(
                i,
                s_val + 3.8,
                f"{s_val:.0f}%",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
                color=COLOR_SKILL,
                zorder=5,
            )
            ax.text(
                i,
                ns_val - 5.5,
                f"{ns_val:.0f}%",
                ha="center",
                va="top",
                fontsize=8.5,
                fontweight="bold",
                color=COLOR_NOSKILL,
                zorder=5,
            )
        else:
            ax.text(
                i,
                s_val + (3.8 if s_val >= ns_val else -5.5),
                f"{s_val:.0f}%",
                ha="center",
                va="bottom" if s_val >= ns_val else "top",
                fontsize=8.5,
                fontweight="bold",
                color=COLOR_SKILL,
                zorder=5,
            )
            ax.text(
                i,
                ns_val + (3.8 if ns_val > s_val else -5.5),
                f"{ns_val:.0f}%",
                ha="center",
                va="bottom" if ns_val > s_val else "top",
                fontsize=8.5,
                fontweight="bold",
                color=COLOR_NOSKILL,
                zorder=5,
            )

    ax.set_xticks(task_x)
    ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks)], fontsize=8.5)
    ax.set_xlim(-0.5, len(tasks) - 0.5)
    ax.set_ylim(-12, 114)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_ylabel(f"Synthesis Accuracy ({metric_name})")
    ax.set_title(
        f"{model_name}: {metric_name} Comparison Across Codebase Tasks (Skill vs. No-skill)",
        fontweight="bold",
        pad=10,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(
        loc="upper right" if max(skill_vals[0], noskill_vals[0]) < 80 else "lower left",
        frameon=True,
        facecolor="white",
        edgecolor="#cccccc",
        framealpha=0.95,
    )

    plt.tight_layout()
    save_plot(fig, stem)
    plt.close(fig)


def plot_dual_metric_comparison(
    model_name: str,
    skill_p1: list,
    skill_p3: list,
    noskill_p1: list,
    noskill_p3: list,
    skill_mean_p1: float,
    skill_mean_p3: float,
    noskill_mean_p1: float,
    noskill_mean_p3: float,
    stem: str,
):
    """Plot both pass@1 and pass@3 lines comparing Skill vs. No-skill in a single unified graph."""
    fig, ax = plt.subplots(figsize=(10.2, 4.8), dpi=300)

    for i in range(len(tasks)):
        if i % 2 == 1:
            ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

    # 4 distinct line styles
    # Skill pass@1: solid steel blue
    ax.plot(
        task_x,
        skill_p1,
        color=COLOR_SKILL,
        linestyle="-",
        linewidth=2.2,
        marker="o",
        markersize=7.5,
        label=f"Skill pass@1 (Mean: {skill_mean_p1:.1f}%)",
        zorder=4,
    )
    # Skill pass@3: dash-dot steel blue
    ax.plot(
        task_x,
        skill_p3,
        color="#173a5e",
        linestyle="-.",
        linewidth=2.0,
        marker="^",
        markersize=7.5,
        label=f"Skill pass@3 (Mean: {skill_mean_p3:.1f}%)",
        zorder=4,
    )
    # No skill pass@1: dashed rust orange
    ax.plot(
        task_x,
        noskill_p1,
        color=COLOR_NOSKILL,
        linestyle="--",
        linewidth=2.0,
        marker="s",
        markersize=7,
        label=f"No Skill pass@1 (Mean: {noskill_mean_p1:.1f}%)",
        zorder=3,
    )
    # No skill pass@3: dotted rust orange
    ax.plot(
        task_x,
        noskill_p3,
        color="#8c3b00",
        linestyle=":",
        linewidth=2.2,
        marker="D",
        markersize=6.5,
        label=f"No Skill pass@3 (Mean: {noskill_mean_p3:.1f}%)",
        zorder=3,
    )

    ax.set_xticks(task_x)
    ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks)], fontsize=8.5)
    ax.set_xlim(-0.5, len(tasks) - 0.5)
    ax.set_ylim(-8, 114)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_ylabel("Synthesis Accuracy (%)")
    ax.set_title(
        f"{model_name}: pass@1 and pass@3 on Codebase Tasks (Skill vs. No-skill)",
        fontweight="bold",
        pad=10,
    )
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(
        loc="upper right" if max(skill_p1[0], noskill_p1[0]) < 80 else "lower left",
        frameon=True,
        facecolor="white",
        edgecolor="#cccccc",
        framealpha=0.95,
        ncol=2,
    )

    plt.tight_layout()
    save_plot(fig, stem)
    plt.close(fig)


def plot_two_panel_model(
    model_name: str,
    skill_p1: list,
    noskill_p1: list,
    skill_p3: list,
    noskill_p3: list,
    skill_mean_p1: float,
    noskill_mean_p1: float,
    skill_mean_p3: float,
    noskill_mean_p3: float,
    stem: str,
):
    """Plot side-by-side subplots: (a) pass@1 and (b) pass@3 for a given model."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 4.4), dpi=300, sharey=True)

    for ax, metric, s_vals, ns_vals, s_mean, ns_mean, panel_tag in [
        (ax1, "pass@1", skill_p1, noskill_p1, skill_mean_p1, noskill_mean_p1, "(a)"),
        (ax2, "pass@3", skill_p3, noskill_p3, skill_mean_p3, noskill_mean_p3, "(b)"),
    ]:
        for i in range(len(tasks)):
            if i % 2 == 1:
                ax.axvspan(i - 0.5, i + 0.5, color=BG_SHADE, alpha=0.9, zorder=0)

        ax.plot(
            task_x,
            s_vals,
            color=COLOR_SKILL,
            linestyle="-",
            linewidth=2.2,
            marker="o",
            markersize=7,
            label=f"Skill (Mean: {s_mean:.1f}%)",
            zorder=4,
        )
        ax.plot(
            task_x,
            ns_vals,
            color=COLOR_NOSKILL,
            linestyle="--",
            linewidth=2.0,
            marker="s",
            markersize=6.5,
            label=f"No Skill (Mean: {ns_mean:.1f}%)",
            zorder=3,
        )

        ax.axhline(s_mean, color=COLOR_SKILL, linestyle=":", linewidth=1.2, alpha=0.75, zorder=2)
        ax.axhline(ns_mean, color=COLOR_NOSKILL, linestyle=":", linewidth=1.2, alpha=0.75, zorder=2)

        for i in range(len(tasks)):
            sv = s_vals[i]
            nsv = ns_vals[i]
            if abs(sv - nsv) < 8:
                ax.text(i, sv + 3.8, f"{sv:.0f}%", ha="center", va="bottom", fontsize=8, fontweight="bold", color=COLOR_SKILL, zorder=5)
                ax.text(i, nsv - 5.5, f"{nsv:.0f}%", ha="center", va="top", fontsize=8, fontweight="bold", color=COLOR_NOSKILL, zorder=5)
            else:
                ax.text(i, sv + (3.8 if sv >= nsv else -5.5), f"{sv:.0f}%", ha="center", va="bottom" if sv >= nsv else "top", fontsize=8, fontweight="bold", color=COLOR_SKILL, zorder=5)
                ax.text(i, nsv + (3.8 if nsv > sv else -5.5), f"{nsv:.0f}%", ha="center", va="bottom" if nsv > sv else "top", fontsize=8, fontweight="bold", color=COLOR_NOSKILL, zorder=5)

        ax.set_xticks(task_x)
        ax.set_xticklabels([f"T{i+1}\n{name}" for i, name in enumerate(tasks)], fontsize=8)
        ax.set_xlim(-0.5, len(tasks) - 0.5)
        ax.set_ylim(-12, 114)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
        ax.set_title(f"{panel_tag} {model_name}: {metric}", fontweight="bold", pad=8)
        ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
        ax.legend(
            loc="upper right" if max(s_vals[0], ns_vals[0]) < 80 else "lower left",
            frameon=True,
            facecolor="white",
            edgecolor="#cccccc",
            framealpha=0.95,
        )

    ax1.set_ylabel("Synthesis Accuracy (%)")
    plt.tight_layout()
    save_plot(fig, stem)
    plt.close(fig)


def plot_overall_pass_at_k(stem: str = "codebase-overall-pass-at-k"):
    """Plot overall Pass@1 and Pass@3 curves comparing Skill vs. No-skill across both models."""
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=300)

    k_vals = np.array([1, 3])

    # GPT-OSS 120B
    ax.plot(
        k_vals,
        [gpt_skill_overall_p1, gpt_skill_overall_p3],
        color=COLOR_SKILL,
        linestyle="-",
        linewidth=2.2,
        marker="o",
        markersize=8,
        label="GPT-OSS 120B (Skill)",
        zorder=4,
    )
    ax.plot(
        k_vals,
        [gpt_noskill_overall_p1, gpt_noskill_overall_p3],
        color=COLOR_SKILL,
        linestyle="--",
        linewidth=2.0,
        marker="s",
        markersize=7.5,
        label="GPT-OSS 120B (No skill)",
        zorder=4,
    )

    # Gemini 3.8 Flash
    ax.plot(
        k_vals,
        [gemini_skill_overall_p1, gemini_skill_overall_p3],
        color=COLOR_NOSKILL,
        linestyle="-",
        linewidth=2.2,
        marker="^",
        markersize=8,
        label="Gemini 3.8 Flash (Skill)",
        zorder=3,
    )
    ax.plot(
        k_vals,
        [gemini_noskill_overall_p1, gemini_noskill_overall_p3],
        color=COLOR_NOSKILL,
        linestyle="--",
        linewidth=2.0,
        marker="D",
        markersize=7.5,
        label="Gemini 3.8 Flash (No skill)",
        zorder=3,
    )

    # Data value text annotations
    annotations = [
        (1, gpt_skill_overall_p1, "50.0%", COLOR_SKILL, "bottom", (0, 6)),
        (3, gpt_skill_overall_p3, "75.0%", COLOR_SKILL, "bottom", (0, 6)),
        (1, gpt_noskill_overall_p1, "16.7%", COLOR_SKILL, "top", (0, -10)),
        (3, gpt_noskill_overall_p3, "50.0%", COLOR_SKILL, "top", (0, -10)),
        (1, gemini_skill_overall_p1, "91.7%", COLOR_NOSKILL, "top", (-12, -12)),
        (3, gemini_skill_overall_p3, "100.0%", COLOR_NOSKILL, "bottom", (-15, 6)),
        (1, gemini_noskill_overall_p1, "100.0%", COLOR_NOSKILL, "bottom", (0, 6)),
        (3, gemini_noskill_overall_p3, "100.0%*", COLOR_NOSKILL, "bottom", (15, 6)),
    ]

    for x_val, y_val, txt, col, va, offset in annotations:
        ax.annotate(
            txt,
            (x_val, y_val),
            xytext=offset,
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=9,
            fontweight="bold",
            color=col,
        )

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["pass@1", "pass@2", "pass@3"], fontsize=10)
    ax.set_xlim(0.7, 3.3)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_ylabel("Overall Accuracy (%)")
    ax.set_title("Overall Pass@k Progression: Skill vs. No-skill Across Codebases", fontweight="bold", pad=10)
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=1)
    ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#cccccc", framealpha=0.95)

    plt.tight_layout()
    save_plot(fig, stem)
    plt.close(fig)


def main():
    print("Generating codebase benchmark graphs...")

    # 1. GPT-OSS 120B individual pass@1 and pass@3 line graphs
    plot_single_metric_comparison(
        metric_name="pass@1",
        model_name="GPT-OSS 120B",
        skill_vals=gpt_skill_pass1,
        noskill_vals=gpt_noskill_pass1,
        skill_mean=gpt_skill_overall_p1,
        noskill_mean=gpt_noskill_overall_p1,
        stem="codebase-gpt-oss-120b-pass1",
    )

    plot_single_metric_comparison(
        metric_name="pass@3",
        model_name="GPT-OSS 120B",
        skill_vals=gpt_skill_pass3,
        noskill_vals=gpt_noskill_pass3,
        skill_mean=gpt_skill_overall_p3,
        noskill_mean=gpt_noskill_overall_p3,
        stem="codebase-gpt-oss-120b-pass3",
    )

    # 2. Gemini individual pass@1 and pass@3 line graphs
    plot_single_metric_comparison(
        metric_name="pass@1",
        model_name="Gemini 3.8 Flash",
        skill_vals=gemini_skill_pass1,
        noskill_vals=gemini_noskill_pass1,
        skill_mean=gemini_skill_overall_p1,
        noskill_mean=gemini_noskill_overall_p1,
        stem="codebase-gemini-pass1",
    )

    plot_single_metric_comparison(
        metric_name="pass@3",
        model_name="Gemini 3.8 Flash",
        skill_vals=gemini_skill_pass3,
        noskill_vals=gemini_noskill_pass3,
        skill_mean=gemini_skill_overall_p3,
        noskill_mean=gemini_noskill_overall_p3,
        stem="codebase-gemini-pass3",
    )

    # 3. Two line graphs for each model comparing skill and no-skill in 2-panel subplots
    plot_two_panel_model(
        model_name="GPT-OSS 120B",
        skill_p1=gpt_skill_pass1,
        noskill_p1=gpt_noskill_pass1,
        skill_p3=gpt_skill_pass3,
        noskill_p3=gpt_noskill_pass3,
        skill_mean_p1=gpt_skill_overall_p1,
        noskill_mean_p1=gpt_noskill_overall_p1,
        skill_mean_p3=gpt_skill_overall_p3,
        noskill_mean_p3=gpt_noskill_overall_p3,
        stem="codebase-gpt-oss-120b-pass1-pass3-panels",
    )

    plot_two_panel_model(
        model_name="Gemini 3.8 Flash",
        skill_p1=gemini_skill_pass1,
        noskill_p1=gemini_noskill_pass1,
        skill_p3=gemini_skill_pass3,
        noskill_p3=gemini_noskill_pass3,
        skill_mean_p1=gemini_skill_overall_p1,
        noskill_mean_p1=gemini_noskill_overall_p1,
        skill_mean_p3=gemini_skill_overall_p3,
        noskill_mean_p3=gemini_noskill_overall_p3,
        stem="codebase-gemini-pass1-pass3-panels",
    )

    # 4. Unified overlay graphs (pass@1 and pass@3 combined on one plot)
    plot_dual_metric_comparison(
        model_name="GPT-OSS 120B",
        skill_p1=gpt_skill_pass1,
        skill_p3=gpt_skill_pass3,
        noskill_p1=gpt_noskill_pass1,
        noskill_p3=gpt_noskill_pass3,
        skill_mean_p1=gpt_skill_overall_p1,
        skill_mean_p3=gpt_skill_overall_p3,
        noskill_mean_p1=gpt_noskill_overall_p1,
        noskill_mean_p3=gpt_noskill_overall_p3,
        stem="codebase-gpt-oss-120b-pass-comparison",
    )

    plot_dual_metric_comparison(
        model_name="Gemini 3.8 Flash",
        skill_p1=gemini_skill_pass1,
        skill_p3=gemini_skill_pass3,
        noskill_p1=gemini_noskill_pass1,
        noskill_p3=gemini_noskill_pass3,
        skill_mean_p1=gemini_skill_overall_p1,
        skill_mean_p3=gemini_skill_overall_p3,
        noskill_mean_p1=gemini_noskill_overall_p1,
        noskill_mean_p3=gemini_noskill_overall_p3,
        stem="codebase-gemini-pass-comparison",
    )

    # 5. Overall Pass@k progression curve
    plot_overall_pass_at_k(stem="codebase-overall-pass-at-k")

    print("All codebase graphs generated successfully!")


if __name__ == "__main__":
    main()
