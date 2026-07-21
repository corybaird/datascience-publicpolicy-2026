import os
import pandas as pd
import statsmodels.api as sm


def run_india_ols_regression():
    """final_cleaned_dataset.csv を用いてインド（2015-2025）の実データで OLS 回帰分析を実行する関数"""
    print("【model.py】 インドの実データを用いたOLS回帰分析を開始します...")
    print("-" * 75)

    # 1. データの読み込みとチェック
    final_path = "final_cleaned_dataset.csv"
    if not os.path.exists(final_path):
        print(f"【エラー】 {final_path} が見つかりません。先に manipulate.py を実行してください。")
        return None

    df = pd.read_csv(final_path)

    # 分析に必要な列の欠損値を排除
    df_model = df.dropna(subset=["value", "co2_per_gdp"])

    if len(df_model) < 3:
        print(f"【エラー】分析に必要なデータ数が足りません（現在の有効データ: {len(df_model)}件）。")
        print("国連APIからデータが正しくマージされているか確認してください。")
        return None

    # 2. 変数の明確な指定 (Specify dependent and independent variables clearly)
    # 従属変数 (Y): 国連APIから取得した、インドのSDG Goal 13 指標の達成数値
    Y = df_model["value"]
    
    # 独立変数 (X): CSVから取得した、インドの経済環境指標 "co2_per_gdp"
    X = df_model["co2_per_gdp"]
    
    # 回帰分析の切片（定数項）を明示的に追加
    X_with_constant = sm.add_constant(X)

    print(f"◎ 従属変数 (Dependent Variable): SDG Goal 13 Indicator Value ('value')")
    print(f"◎ 独立変数 (Independent Variable): CO2 Emissions per GDP ('co2_per_gdp')")
    print(f"◎ 分析対象期間: {int(df_model['year'].min())}年 〜 {int(df_model['year'].max())}年")
    print(f"◎ サンプルサイズ (Observations): {len(df_model)} 件")
    print("-" * 75)

    # 3. OLS回帰分析の実行とフルサマリーの印刷 (Print out the full model summary)
    model = sm.OLS(Y, X_with_constant)
    results = model.fit()

    print("【1】 Full OLS Regression Summary")
    print(results.summary())
    print("-" * 75)

    # 4. モデルの分析結果と初期仮説の検証サマリー (Summarize findings and state hypothesis support)
    p_value = results.pvalues["co2_per_gdp"]
    coef = results.params["co2_per_gdp"]
    r_squared = results.rsquared

    print("【2】 Model Findings & Hypothesis Verification")
    print(f"  ・モデル適合度 (R-squared): {r_squared:.4f}")
    print(f"  ・co2_per_gdp の係数 (Coefficient): {coef:.4f} (標準誤差: {results.bse['co2_per_gdp']:.4f})")
    print(f"  ・t統計量 (t-Statistic): {results.tvalues['co2_per_gdp']:.4f}")
    # P>|t| (p値) の抽出
    print(f"  ・p値 (p-value): {p_value:.4f}")
    print("")
    print("【結論と考察】")
    
    # 初期仮説：一般的に「GDPあたりのCO2排出量(co2_per_gdp)が低下するほど、環境負荷が下がりSDG 13の達成スコア(value)は上昇する（＝負の相関関係）」と仮定します。
    if p_value < 0.05:
        print("  ・[統計的有意性]: p値が 0.05 未満であるため、co2_per_gdp は統計的に有意な影響を与えています。")
        if coef < 0:
            print("  ・[仮説の検証]: 係数が負の値（マイナス）です。これは『CO2排出効率が改善する（数値が下がる）ほど、SDG13の達成スコアが向上する』という初期仮説を【強く支持する】結果です。")
        else:
            print("  ・[仮説の検証]: 係数が正の値（プラス）です。排出量の推移とSDG指標が正の相関を示しており、初期仮説とは異なる動向、あるいは指標の定義特有の挙動である可能性があります。")
    else:
        print("  ・[統計的有意性]: p値が 0.05 以上であるため、今回のモデルにおいては統計的に有意な関係性は認められませんでした。")
        print("  ・[仮説の検証]: 2015〜2025年という短い期間のデータによる限定されたサンプルサイズ（小標本）であるため、初期仮説を統計的に支持（または棄却）する十分な証拠は得られませんでした。")
        print("    （今後の研究において、より長期のタイムシリーズデータを用いた再検証が必要です）")
    print("-" * 75)

    return results


if __name__ == "__main__":
    run_india_ols_regression()