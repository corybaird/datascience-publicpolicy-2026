import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/sheena-pham/processed_gender_ai_exposure.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    # Figure 1: female share vs. GenAI exposure score, by occupation (tests H1)
    def categorize(code):
        if code // 10 == 4:
            return "Clerical support"
        if code in (22, 23, 32, 51, 53):  # health, personal care, teaching professionals
            return "Health, personal care & teaching"
        return "Other occupations"

    df["category"] = df["isco08_code"].apply(categorize)
    category_colors = {
        "Clerical support": "#2a78d6",
        "Health, personal care & teaching": "#008300",
        "Other occupations": "#898781",
    }

    plt.figure(figsize=(10, 7))
    sns.regplot(
        data=df, x="female_share", y="exposure_score",
        scatter=False,
        line_kws={"color": "#c1666b", "linewidth": 2},
    )
    for category, color in category_colors.items():
        subset = df[df["category"] == category]
        plt.scatter(
            subset["female_share"], subset["exposure_score"],
            s=subset["employment_total"] / 8, color=color, alpha=0.85,
            edgecolor="white", linewidth=0.5, label=category, zorder=3,
        )

    # Label the most extreme occupations: high female share paired with either
    # high or low exposure, so the clerical vs. health/care/teaching split reads directly.
    to_label = df[
        (df["female_share"] > 0.65) & ((df["exposure_score"] > 3) | (df["exposure_score"] < 1))
    ].sort_values("exposure_score")

    ax = plt.gca()
    fig = plt.gcf()
    # leave headroom on the right so right-offset labels stay inside the axes frame
    ax.set_xlim(-0.03, 0.92)

    min_gap_pts = 13  # minimum vertical clearance between stacked labels, in points
    last_pts_y = None
    for _, row in to_label.iterrows():
        x, y = row["female_share"], row["exposure_score"]
        # marker position in points (same units as the annotate offset below), so
        # stacked labels can be pushed apart by a fixed on-screen gap regardless
        # of how compressed the data range is
        marker_pts_y = ax.transData.transform((x, y))[1] / fig.dpi * 72
        target_pts_y = marker_pts_y + 6
        if last_pts_y is not None and target_pts_y - last_pts_y < min_gap_pts:
            target_pts_y = last_pts_y + min_gap_pts
        last_pts_y = target_pts_y

        # points near the right edge get their label flipped to the left so the
        # text doesn't run past the axes border
        near_right_edge = x > 0.75
        plt.annotate(
            row["isco08_label"],
            (x, y),
            xytext=(-8 if near_right_edge else 8, target_pts_y - marker_pts_y),
            textcoords="offset points",
            ha="right" if near_right_edge else "left",
            fontsize=8, color="#0b0b0b",
        )

    plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    plt.title("Female Employment Share vs. GenAI Task Exposure, by Occupation (Australia, 2025)")
    plt.xlabel("Female Share of Employment")
    plt.ylabel("Mean GenAI Exposure Score (0 = Not Exposed, 5 = Highest Exposure)")
    plt.legend(title="Occupation group", loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.show()
    plt.close()

    # Figure 2: occupations ranked by female share, colored by exposure score (tests H2)
    df_sorted = df.sort_values("female_share")
    plt.figure(figsize=(10, 6))
    norm = plt.Normalize(df_sorted["exposure_score"].min(), df_sorted["exposure_score"].max())
    colors = plt.cm.Blues(0.3 + 0.6 * norm(df_sorted["exposure_score"]))
    bars = plt.barh(df_sorted["isco08_label"], df_sorted["female_share"], color=colors)
    plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    plt.axvline(0.5, color="#888888", linewidth=1, linestyle="--")
    sm = plt.cm.ScalarMappable(cmap="Blues", norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca())
    cbar.set_label("Mean GenAI Exposure Score")
    plt.title("Female Employment Share by Occupation, Shaded by GenAI Exposure (Australia, 2025)")
    plt.xlabel("Female Share of Employment")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()
    plt.close()
