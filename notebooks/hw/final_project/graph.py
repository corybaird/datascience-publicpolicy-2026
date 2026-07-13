import pandas as pd
import matplotlib.pyplot as plt

# Graphs for regional revenue analysis

REGION_LABELS = {
    "us_revenue_share": "US",
    "europe_revenue_share": "Europe",
    "asia_revenue_share": "Asia-Pacific",
    "row_revenue_share": "Rest of World"
}

REGION_COLORS = {
    "us_revenue_share": "#9E9E9E",
    "europe_revenue_share": "#0057B8",
    "asia_revenue_share": "#6BAED6",
    "row_revenue_share": "#BDB76B"
}

def load_data():
    df = pd.read_csv("../../../data/final_project/daria-chelyukanova/merged_revenue_gdpr.csv")

    return df

def plot_regional_revenue_and_fines(df, company_name):
    company_data = df[df["company"] == company_name].copy()
    company_data = company_data.sort_values("year")

    fig, ax = plt.subplots(figsize=(10,6))
    
    for column, label in REGION_LABELS.items():
        if column == "europe_revenue_share":
            linewidth = 3
            alpha = 1
        else:
            linewidth = 2
            alpha = 0.6

        ax.plot(
            company_data["year"],
            company_data[column],
            color=REGION_COLORS[column],
            marker="o",
            linewidth=linewidth,
            alpha=alpha,
            label=label
        )

    ax.axvline(x=2018, color="gray", linestyle="--", label="Intro of GDPR")
    ax.axvline(x=2022, color="black", linestyle="--", label="Intro of DSA")

    ax.set_title(f"{company_name}: Regional Revenue Share (%) vs GDPR Fines (EUR)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total Revenue (%)")

    ax.legend(loc="upper left")

    ax2 = ax.twinx()

    ax2.scatter(
        company_data["year"],
        company_data["total_fine_amount"],
        color="red",
        s=60,
        label="GDPR Fine Amount"
    )

    ax2.vlines(
        company_data["year"], 0,
        company_data["total_fine_amount"],
        color="red",
        alpha=0.3
    )

    ax2.set_ylabel("GDPR Fine Amount (EUR)")

    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.show()

# Graphs for advertising revenue share analysis

def plot_advertising_share_and_fines(df, company_name):
    company_data = df[df["company"] == company_name].copy()
    company_data = company_data.sort_values("year")

    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(
        company_data["year"],
        company_data["advertising_revenue_share"],
        color="#6A0DAD",
        marker= "o",
        linewidth=3,
        label="Advertising Revenue Share (%)"
    )

    ax.axvline(x=2018, color="gray", linestyle="--", label="Intro of GDPR")
    ax.axvline(x=2022, color="black", linestyle="--", label="Intro of DSA")

    ax.set_title(f"{company_name}: Gloabl Advertising Revenue Share (%) vs GDPR Fines (EUR)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total Revenue (%)")

    ax.legend(loc="upper left")

    ax2 = ax.twinx()

    ax2.scatter(
        company_data["year"],
        company_data["total_fine_amount"],
        color="red",
        s=60,
        label="GDPR Fine Amount"
    )

    ax2.vlines(
        company_data["year"], 0,
        company_data["total_fine_amount"],
        color="red",
        alpha=0.3
    )

    ax2.set_ylabel("GDPR Fine Amount (EUR)")

    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.show()

# Run both graphs

def run():
    df = load_data()

    plot_regional_revenue_and_fines(df, "Meta")
    plot_regional_revenue_and_fines(df, "Alphabet")

    plot_advertising_share_and_fines(df, "Meta")
    plot_advertising_share_and_fines(df, "Alphabet")

    return df

