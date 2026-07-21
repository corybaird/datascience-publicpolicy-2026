# graph.py の中身
import matplotlib.pyplot as plt
import pandas as pd


def plot_india_sdg_trends():
    print("【graph.py】 グラフを作成しています...")

    try:
        df = pd.read_csv("final_cleaned_dataset.csv")
    except FileNotFoundError:
        print("【エラー】ファイルが見つかりません。")
        return

    if df.empty:
        print("【エラー】データが空っぽです。")
        return

    # 実際に含まれている指標名を取得
    indicator_name = "SDG Goal 13 Indicator"
    if "seriesDescription" in df.columns:
        valid_names = df["seriesDescription"].dropna().unique()
        if len(valid_names) > 0:
            # グラフに収まるように長い指標名は50文字でカット
            indicator_name = (
                valid_names[0][:50] + "..."
                if len(valid_names[0]) > 50
                else valid_names[0]
            )

    plt.rcParams["font.size"] = 11
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)

    # 左軸: 自動選択されたSDG指標
    color1 = "#1f77b4"
    ax1.set_xlabel("Year", labelpad=10)
    ax1.set_ylabel(indicator_name, color=color1, labelpad=10)

    df_clean_sdg = df.dropna(subset=["value"])
    if not df_clean_sdg.empty:
        line1 = ax1.plot(
            df_clean_sdg["year"],
            df_clean_sdg["value"],
            color=color1,
            linewidth=2.5,
            marker="o",
            markersize=8,
            label="SDG 13 Indicator Value",
        )
        print(f"【graph.py】 青い点を {len(df_clean_sdg)} 件プロットしました。")
    else:
        line1 = ax1.plot([], [], color=color1, marker="o", label="SDG 13 (No Data)")
        print("【注意】プロットできるSDGデータがありませんでした。")

    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 右軸: CO2 Emissions per GDP
    ax2 = ax1.twinx()
    color2 = "#d62728"
    ax2.set_ylabel("CO2 Emissions per GDP (co2_per_gdp)", color=color2, labelpad=10)

    line2 = ax2.plot(
        df["year"],
        df["co2_per_gdp"],
        color=color2,
        linewidth=2.5,
        marker="s",
        linestyle="--",
        label="CO2 per GDP",
    )
    ax2.tick_params(axis="y", labelcolor=color2)

    plt.title(
        "India: SDG Goal 13 and CO2 Intensity Trends (2015-2025)",
        pad=20,
        fontweight="bold",
    )

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=True)

    plt.xticks(df["year"].unique())
    plt.tight_layout()

    plt.savefig("india_sdg13_dynamic_trends.png", dpi=300)
    plt.show()