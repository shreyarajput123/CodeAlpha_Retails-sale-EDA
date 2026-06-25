# Retail Sales EDA Project

This project is a complete exploratory data analysis (EDA) package for a small retail sales dataset. It is designed for Task 2 requirements:

- ask meaningful questions before analysis
- inspect variables, types, and structure
- identify trends, patterns, and anomalies
- test hypotheses with statistics and visualization
- detect data quality issues for later analysis

## Project Files

```text
EDA/
├── data/
│   └── retail_orders.csv
├── outputs/
│   └── README.md
├── src/
│   └── eda.py
├── index.html
├── REPORT.md
├── requirements.txt
└── README.md
```

## Dataset

The dataset contains 36 retail orders across regions, categories, products, payment methods, and customer segments. It intentionally includes realistic data issues such as missing values, a duplicate order ID, a negative quantity, and an outlier order value so the EDA can discuss problems found during analysis.

## How To View The Dashboard

Open `index.html` in a browser. It runs locally with no installation and shows:

- KPI summary
- monthly revenue trend
- region and category comparisons
- payment method distribution
- anomaly and data quality checks
- hypothesis test summaries

## How To Run The Python Analysis

If Python is available on your machine:

```bash
pip install -r requirements.txt
python src/eda.py
```

The script reads `data/retail_orders.csv` and writes charts plus summary tables into `outputs/`.

## Main EDA Questions

1. Which regions and product categories generate the most revenue?
2. Are monthly sales improving, declining, or unstable?
3. Do customer segments differ in average order value?
4. Are discounts associated with lower or higher revenue per order?
5. Which records look suspicious because of missing values, duplicate IDs, negative quantities, or extreme values?

