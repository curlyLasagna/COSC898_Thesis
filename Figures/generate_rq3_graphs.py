# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "altair>=5.4.0",
#   "matplotlib>=3.8.0",
#   "numpy>=1.26.0",
#   "pandas>=2.2.0",
#   "vl-convert-python>=1.6.0",
# ]
# ///

from pathlib import Path
import altair as alt
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


def parse_mmss_to_seconds(time_str: str) -> float:
    """Convert [+-]MM:SS.ss string to seconds (float)."""
    sign = -1.0 if time_str.startswith("-") else 1.0
    clean = time_str.lstrip("+-")
    mins, secs = clean.split(":")
    return sign * (int(mins) * 60.0 + float(secs))


def format_seconds_mmss(seconds: float) -> str:
    """Format seconds as +M:SS.ss or -M:SS.ss."""
    sign = "-" if seconds < 0 else "+"
    abs_sec = abs(seconds)
    mins = int(abs_sec // 60)
    rem_sec = abs_sec - mins * 60
    return f"{sign}{mins}:{rem_sec:05.2f}"


raw_records = [
    # Rust Toolchain
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student A", "Imperative", "3:21.22"),
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student A", "Declarative (nix develop)", "4:54.86"),
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student B", "Imperative", "5:19.95"),
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student B", "Declarative (nix develop)", "7:06.64"),
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student C", "Imperative", "4:56.23"),
    ("Installation of the Rust Compiler", "rq3-rust-results", "Student C", "Declarative (nix develop)", "4:45.80"),
    # Jupyter Notebook
    ("Jupyter Notebook", "rq3-jupyter-results", "Student A", "Imperative", "4:59.33"),
    ("Jupyter Notebook", "rq3-jupyter-results", "Student A", "Declarative (nix develop)", "3:42.04"),
    ("Jupyter Notebook", "rq3-jupyter-results", "Student B", "Imperative", "7:21.44"),
    ("Jupyter Notebook", "rq3-jupyter-results", "Student B", "Declarative (nix develop)", "8:41.60"),
    ("Jupyter Notebook", "rq3-jupyter-results", "Student C", "Imperative", "8:37.12"),
    ("Jupyter Notebook", "rq3-jupyter-results", "Student C", "Declarative (nix develop)", "9:22.12"),
    # Full Stack Environment
    ("Full Stack Environment", "rq3-fullstack-results", "Student A", "Imperative", "11:22.12"),
    ("Full Stack Environment", "rq3-fullstack-results", "Student A", "Declarative (nix develop)", "12:02.39"),
    ("Full Stack Environment", "rq3-fullstack-results", "Student B", "Imperative", "8:59.18"),
    ("Full Stack Environment", "rq3-fullstack-results", "Student B", "Declarative (nix develop)", "10:27.73"),
    ("Full Stack Environment", "rq3-fullstack-results", "Student C", "Imperative", "11:31.58"),
    ("Full Stack Environment", "rq3-fullstack-results", "Student C", "Declarative (nix develop)", "15:50.40"),
]

df = pd.DataFrame(
    [
        {
            "Subsection": sub,
            "Slug": slug,
            "Participant": student,
            "Method": method,
            "TimeLabel": t_str,
            "Seconds": parse_mmss_to_seconds(t_str),
            "Minutes": round(parse_mmss_to_seconds(t_str) / 60.0, 3),
        }
        for sub, slug, student, method, t_str in raw_records
    ]
)

figures_dir = Path(__file__).resolve().parent
method_order = ["Imperative", "Declarative (nix develop)"]
subsection_order = [
    "Installation of the Rust Compiler",
    "Jupyter Notebook",
    "Full Stack Environment",
]
color_scale = alt.Scale(
    domain=method_order,
    range=["#4C78A8", "#F58518"],
)

# 1. Combined faceted chart separated by subsection
base_facet = alt.Chart(df).encode(
    x=alt.X(
        "Participant:N",
        title=None,
        scale=alt.Scale(paddingInner=0.26, paddingOuter=0.15),
        axis=alt.Axis(labelAngle=0, labelFontSize=11),
    ),
    xOffset=alt.XOffset(
        "Method:N",
        sort=method_order,
        scale=alt.Scale(paddingInner=0.14),
    ),
    y=alt.Y(
        "Minutes:Q",
        title="Completion Time (Minutes)",
        scale=alt.Scale(domain=[0, 18]),
        axis=alt.Axis(titleFontWeight="bold", labelFontSize=11, titleFontSize=12, grid=True),
    ),
    color=alt.Color(
        "Method:N",
        sort=method_order,
        scale=color_scale,
        title="Onboarding Workflow",
        legend=alt.Legend(
            orient="top",
            titleFontWeight="bold",
            labelFontSize=11,
            titleFontSize=11,
        ),
    ),
)

bars_facet = base_facet.mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
labels_facet = base_facet.mark_text(
    dy=-7,
    fontSize=8.5,
    fontWeight="bold",
).encode(text="TimeLabel:N")

combined_chart = (
    (bars_facet + labels_facet)
    .properties(width=250, height=220)
    .facet(
        column=alt.Column(
            "Subsection:N",
            sort=subsection_order,
            title=None,
            header=alt.Header(labelFontSize=12, labelFontWeight="bold"),
        )
    )
    .configure_view(strokeWidth=0.5, stroke="#CCCCCC")
)

combined_png = figures_dir / "rq3-onboarding-results.png"
combined_pdf = figures_dir / "rq3-onboarding-results.pdf"
combined_svg = figures_dir / "rq3-onboarding-results.svg"
combined_chart.save(str(combined_png), scale_factor=2.0)
combined_chart.save(str(combined_pdf))
combined_chart.save(str(combined_svg))
print(f"Saved {combined_png}, {combined_pdf}, and {combined_svg}")

# 2. Individual charts per task
task_y_domains = {
    "Installation of the Rust Compiler": 8,
    "Jupyter Notebook": 12,
    "Full Stack Environment": 19,
}

for sub in subsection_order:
    sub_df = df[df["Subsection"] == sub]
    slug = sub_df["Slug"].iloc[0]
    max_y = task_y_domains.get(sub, 18)

    single_base = alt.Chart(sub_df).encode(
        x=alt.X(
            "Participant:N",
            title="Participant",
            scale=alt.Scale(paddingInner=0.26, paddingOuter=0.15),
            axis=alt.Axis(labelAngle=0, labelFontSize=11, titleFontWeight="bold"),
        ),
        xOffset=alt.XOffset(
            "Method:N",
            sort=method_order,
            scale=alt.Scale(paddingInner=0.14),
        ),
        y=alt.Y(
            "Minutes:Q",
            title="Completion Time (Minutes)",
            scale=alt.Scale(domain=[0, max_y]),
            axis=alt.Axis(titleFontWeight="bold", labelFontSize=11, titleFontSize=12, grid=True),
        ),
        color=alt.Color(
            "Method:N",
            sort=method_order,
            scale=color_scale,
            title="Onboarding Workflow",
            legend=alt.Legend(
                orient="top",
                titleFontWeight="bold",
                labelFontSize=11,
                titleFontSize=11,
            ),
        ),
    )
    single_bars = single_base.mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
    single_labels = single_base.mark_text(
        dy=-7,
        fontSize=9.5,
        fontWeight="bold",
    ).encode(
        text="TimeLabel:N",
        color=alt.Color("Method:N", sort=method_order, scale=color_scale, legend=None),
    )

    single_chart = (
        (single_bars + single_labels)
        .properties(
            title=alt.TitleParams(
                text=sub,
                fontSize=13,
                fontWeight="bold",
                anchor="middle",
            ),
            width=340,
            height=220,
        )
        .configure_view(strokeWidth=0)
    )

    task_png = figures_dir / f"{slug}.png"
    task_pdf = figures_dir / f"{slug}.pdf"
    task_svg = figures_dir / f"{slug}.svg"
    single_chart.save(str(task_png), scale_factor=2.0)
    single_chart.save(str(task_pdf))
    single_chart.save(str(task_svg))
    print(f"Saved {task_png}, {task_pdf}, and {task_svg}")

# 3. Average Time Delta per Subsection (Clean bar graph)
pivoted = df.pivot(index=["Subsection", "Participant"], columns="Method", values="Seconds").reset_index()
pivoted["DeltaSeconds"] = pivoted["Declarative (nix develop)"] - pivoted["Imperative"]
pivoted["DeltaMinutes"] = pivoted["DeltaSeconds"] / 60.0

# Styling configuration matching publication standards
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.5,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 10.5,
    "figure.titlesize": 13,
})

fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=300)

x_indices = np.arange(len(subsection_order))
bar_width = 0.48

# Palette: distinct elegant muted tones matching the thesis
bar_colors = ["#4C78A8", "#72B7B2", "#F58518"]
bar_edges = ["#2b527d", "#4b8782", "#b85d09"]

for i, sub in enumerate(subsection_order):
    sub_df = pivoted[pivoted["Subsection"] == sub]
    mean_sec = float(sub_df["DeltaSeconds"].mean())
    mean_min = float(sub_df["DeltaMinutes"].mean())

    # Plot bar
    ax.bar(
        x_indices[i],
        mean_min,
        width=bar_width,
        color=bar_colors[i],
        edgecolor=bar_edges[i],
        linewidth=1.2,
        zorder=3,
    )

    # Format text label above each bar
    sign = "+" if mean_sec > 0 else "-"
    abs_s = abs(mean_sec)
    mm = int(abs_s // 60)
    ss = abs_s - mm * 60
    time_str = f"{sign}{mm}:{ss:05.2f} ({mean_sec:+.1f}s)"
    ax.text(
        x_indices[i],
        mean_min + 0.08,
        time_str,
        ha="center",
        va="bottom",
        fontsize=10.0,
        fontweight="bold",
        color="#222222",
        zorder=5,
    )

# Baseline
ax.axhline(0, color="#333333", linestyle="-", linewidth=1.0, zorder=4)

# Gridlines
ax.grid(axis="y", color="#e0e0e0", linestyle="--", linewidth=0.7, zorder=1)
ax.set_axisbelow(True)

# Y-axis styling
ax.set_ylabel("Mean Time Delta (Minutes, Declarative − Imperative)", fontweight="bold", labelpad=8)
ax.set_ylim(0, 2.6)
y_ticks = np.arange(0, 2.6, 0.5)
ax.set_yticks(y_ticks)

def format_ytick(val, pos):
    mins = int(val)
    secs = int(round((val - mins) * 60))
    return f"{mins}:{secs:02d}"

ax.yaxis.set_major_formatter(FuncFormatter(format_ytick))

# X-axis styling
ax.set_xticks(x_indices)
ax.set_xticklabels(subsection_order, fontweight="bold")
ax.set_xlabel("Coursework Environment Task", fontweight="bold", labelpad=8)

# Spines cleanup
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.tight_layout()

delta_png = figures_dir / "rq3-avg-time-delta.png"
delta_pdf = figures_dir / "rq3-avg-time-delta.pdf"
delta_svg = figures_dir / "rq3-avg-time-delta.svg"
fig.savefig(delta_png, dpi=300)
fig.savefig(delta_pdf)
fig.savefig(delta_svg)
print(f"Saved {delta_png}, {delta_pdf}, and {delta_svg}")
