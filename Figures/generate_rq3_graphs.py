# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "altair>=5.4.0",
#   "pandas>=2.2.0",
#   "vl-convert-python>=1.6.0",
# ]
# ///

from pathlib import Path
import altair as alt
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

# 3. Average Time Delta per Subsection (Declarative - Imperative)
pivoted = df.pivot(index=["Subsection", "Participant"], columns="Method", values="Seconds").reset_index()
pivoted["DeltaSeconds"] = pivoted["Declarative (nix develop)"] - pivoted["Imperative"]

avg_delta_rows = []
for sub in subsection_order:
    sub_deltas = pivoted[pivoted["Subsection"] == sub]["DeltaSeconds"]
    mean_sec = float(sub_deltas.mean())
    avg_delta_rows.append(
        {
            "Subsection": sub,
            "MeanDeltaSeconds": round(mean_sec, 2),
            "MeanDeltaMinutes": round(mean_sec / 60.0, 3),
            "DeltaLabel": f"{format_seconds_mmss(mean_sec)} ({mean_sec:+.1f}s)",
        }
    )

avg_delta_df = pd.DataFrame(avg_delta_rows)

delta_base = alt.Chart(avg_delta_df).encode(
    x=alt.X(
        "Subsection:N",
        sort=subsection_order,
        title="Coursework Environment Task",
        scale=alt.Scale(paddingInner=0.4, paddingOuter=0.25),
        axis=alt.Axis(labelAngle=0, titleFontWeight="bold", labelFontSize=11, titleFontSize=12, labelLimit=220),
    ),
    y=alt.Y(
        "MeanDeltaMinutes:Q",
        title="Mean Time Delta (Minutes, Declarative − Imperative)",
        scale=alt.Scale(domain=[0, 2.6]),
        axis=alt.Axis(titleFontWeight="bold", labelFontSize=11, titleFontSize=12, grid=True),
    ),
    color=alt.Color(
        "Subsection:N",
        sort=subsection_order,
        scale=alt.Scale(
            domain=subsection_order,
            range=["#4C78A8", "#72B7B2", "#F58518"],
        ),
        legend=None,
    ),
)

delta_bars = delta_base.mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
delta_labels = delta_base.mark_text(
    dy=-9,
    fontSize=10.5,
    fontWeight="bold",
    color="#222222",
).encode(text="DeltaLabel:N")

delta_chart = (
    (delta_bars + delta_labels)
    .properties(
        title=alt.TitleParams(
            text="Average Onboarding Time Delta by Environment Task (Declarative − Imperative)",
            fontSize=13,
            fontWeight="bold",
            anchor="middle",
        ),
        width=520,
        height=240,
    )
    .configure_view(strokeWidth=0)
)

delta_png = figures_dir / "rq3-avg-time-delta.png"
delta_pdf = figures_dir / "rq3-avg-time-delta.pdf"
delta_svg = figures_dir / "rq3-avg-time-delta.svg"
delta_chart.save(str(delta_png), scale_factor=2.0)
delta_chart.save(str(delta_pdf))
delta_chart.save(str(delta_svg))
print(f"Saved {delta_png}, {delta_pdf}, and {delta_svg}")
