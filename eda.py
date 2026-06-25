from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "retail_orders.csv"
OUT_DIR = ROOT / "outputs"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["net_sales"] = df["gross_sales"] * (1 - df["discount"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def save_tables(df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(exist_ok=True)

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_order_ids": int(df["order_id"].duplicated(keep=False).sum()),
        "missing_values": int(df.isna().sum().sum()),
        "negative_quantities": int((df["quantity"] < 0).sum()),
        "total_net_sales": round(df["net_sales"].sum(), 2),
        "average_order_value": round(df["net_sales"].mean(), 2),
        "median_order_value": round(df["net_sales"].median(), 2),
        "return_rate": round((df["returned"].eq("Yes").mean()) * 100, 2),
    }
    pd.Series(summary).to_csv(OUT_DIR / "summary_metrics.csv", header=["value"])

    df.groupby("category", as_index=False)["net_sales"].sum().sort_values(
        "net_sales", ascending=False
    ).to_csv(OUT_DIR / "category_sales.csv", index=False)

    df.groupby("customer_segment", as_index=False)["net_sales"].agg(
        ["count", "mean", "median", "sum"]
    ).round(2).to_csv(OUT_DIR / "segment_sales.csv")

    quality = pd.DataFrame(
        {
            "check": [
                "duplicate_order_ids",
                "missing_delivery_days",
                "negative_quantities",
                "discount_outside_0_1",
            ],
            "count": [
                df["order_id"].duplicated(keep=False).sum(),
                df["delivery_days"].isna().sum(),
                (df["quantity"] < 0).sum(),
                (~df["discount"].between(0, 1)).sum(),
            ],
        }
    )
    quality.to_csv(OUT_DIR / "data_quality_checks.csv", index=False)


def save_charts(df: pd.DataFrame) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    monthly = df.groupby("month", as_index=False)["net_sales"].sum()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="net_sales", marker="o")
    plt.title("Monthly Net Sales")
    plt.xlabel("Month")
    plt.ylabel("Net sales")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "monthly_net_sales.png", dpi=160)
    plt.close()

    category = df.groupby("category", as_index=False)["net_sales"].sum()
    category = category.sort_values("net_sales", ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=category, x="category", y="net_sales", hue="category", legend=False)
    plt.title("Net Sales By Category")
    plt.xlabel("Category")
    plt.ylabel("Net sales")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "category_net_sales.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x="customer_segment", y="net_sales")
    plt.title("Order Value Distribution By Segment")
    plt.xlabel("Customer segment")
    plt.ylabel("Net sales")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "segment_order_value_boxplot.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="discount", y="net_sales", hue="category")
    plt.title("Discount vs Net Sales")
    plt.xlabel("Discount rate")
    plt.ylabel("Net sales")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "discount_vs_net_sales.png", dpi=160)
    plt.close()


def run_hypothesis_tests(df: pd.DataFrame) -> None:
    segment_groups = [
        group["net_sales"].dropna().values
        for _, group in df.groupby("customer_segment")
        if len(group) > 1
    ]
    h_stat, h_pvalue = stats.kruskal(*segment_groups)

    corr = stats.spearmanr(df["discount"], df["net_sales"], nan_policy="omit")

    return_rates = pd.crosstab(df["category"], df["returned"], normalize="index")
    return_rates = return_rates.rename(columns={"No": "not_returned_rate", "Yes": "returned_rate"})

    results = pd.DataFrame(
        {
            "test": [
                "Kruskal-Wallis: net_sales by customer_segment",
                "Spearman correlation: discount vs net_sales",
            ],
            "statistic": [round(h_stat, 4), round(corr.statistic, 4)],
            "p_value": [round(h_pvalue, 4), round(corr.pvalue, 4)],
            "interpretation": [
                "Tests whether median order value differs by customer segment.",
                "Tests whether discount rate changes monotonically with net sales.",
            ],
        }
    )
    results.to_csv(OUT_DIR / "hypothesis_tests.csv", index=False)
    return_rates.round(3).to_csv(OUT_DIR / "category_return_rates.csv")


def main() -> None:
    df = load_data()
    save_tables(df)
    save_charts(df)
    run_hypothesis_tests(df)
    print(f"EDA outputs written to: {OUT_DIR}")


if __name__ == "__main__":
    main()

