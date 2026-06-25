# Exploratory Data Analysis Report

## 1. Business Context

This EDA studies a retail orders dataset containing sales across regions, customer segments, product categories, payment methods, and delivery outcomes. The goal is to understand sales behavior, detect early patterns, test assumptions, and identify data issues before deeper modeling or dashboarding.

## 2. Questions Before Analysis

1. Which regions, cities, and product categories contribute the most revenue?
2. Are sales increasing over time, or are they concentrated in a few months?
3. Which customer segment has the highest average order value?
4. Are large discounts associated with lower net revenue per order?
5. Which payment methods are most common among customers?
6. Are returns concentrated in certain categories or segments?
7. Are there data quality issues such as missing values, duplicates, invalid quantities, or outliers?

## 3. Data Structure

The dataset has 36 rows and 13 columns.

| Variable | Type | Description |
|---|---:|---|
| `order_id` | categorical | Unique order identifier, expected to be unique |
| `order_date` | date | Date of transaction |
| `region` | categorical | Sales region |
| `city` | categorical | City where order was placed |
| `customer_segment` | categorical | Consumer, Corporate, or Home Office |
| `category` | categorical | Product category |
| `product` | categorical | Product name |
| `quantity` | numeric | Number of units purchased |
| `unit_price` | numeric | Price per unit before discount |
| `discount` | numeric | Discount rate from 0 to 1 |
| `payment_method` | categorical | Payment channel |
| `delivery_days` | numeric | Days required for delivery |
| `returned` | categorical | Whether order was returned |

Derived fields used in analysis:

- `gross_sales = quantity * unit_price`
- `net_sales = gross_sales * (1 - discount)`
- `month = YYYY-MM`

## 4. Initial Findings

Electronics and Furniture are the strongest revenue categories because they contain high-ticket products such as laptops, tablets, smartphones, monitors, and tables. Groceries have high quantity counts but much lower average order value.

Sales are not evenly distributed across months. Revenue rises sharply in months with premium electronics purchases, especially May, July, August, and September. This suggests monthly revenue is sensitive to a few high-value orders.

Corporate customers tend to place larger orders than Consumer and Home Office customers, largely because they purchase electronics and furniture items. Consumer orders are more frequent but generally smaller.

UPI appears frequently among lower and mid-value consumer orders, while Credit Card and Bank Transfer are more common in higher-value corporate transactions.

## 5. Trends, Patterns, And Anomalies

### Trends

- Higher revenue is concentrated in Electronics and Furniture.
- Corporate orders have higher average net sales than other segments.
- Clothing has a higher visible return count than most other categories in this sample.
- Monthly sales show spikes rather than smooth growth.

### Patterns

- Discounts are larger in Clothing and Furniture than in Groceries.
- Delivery time is longer for Furniture and some Electronics orders.
- UPI is common across many small-to-medium orders.

### Anomalies

- `R1017` Laptop order and `R1033` Smartphone order are high-value transactions that strongly affect revenue totals.
- `R1035` appears twice, which violates the expected uniqueness of `order_id`.
- One order has `quantity = -1`, which is invalid for normal sales data.
- One row has a missing `delivery_days` value.

## 6. Hypotheses And Validation Plan

### Hypothesis 1: Corporate customers have higher average order value.

Validation:

- Group by `customer_segment`.
- Compare mean and median `net_sales`.
- Use one-way ANOVA if assumptions are acceptable, otherwise use Kruskal-Wallis.

Expected result from this sample: Corporate orders likely show the highest average order value due to bulkier Electronics and Furniture purchases.

### Hypothesis 2: Electronics generate more revenue than other categories.

Validation:

- Group by `category`.
- Compare total `net_sales`.
- Visualize category revenue with a bar chart.

Expected result from this sample: Electronics should lead total sales.

### Hypothesis 3: Higher discounts reduce net sales per order.

Validation:

- Calculate Pearson or Spearman correlation between `discount` and `net_sales`.
- Use a scatter plot to inspect whether this relationship is linear.

Expected result from this sample: The relationship may be weak because high-value products can still generate high net sales even with discounts.

### Hypothesis 4: Returns are more common in Clothing.

Validation:

- Cross-tabulate `category` against `returned`.
- Compare return rate by category.

Expected result from this sample: Clothing has multiple returned orders and should show a higher return rate.

## 7. Data Issues To Address

| Issue | Example | Why It Matters | Recommended Fix |
|---|---|---|---|
| Duplicate order ID | `R1035` | Breaks uniqueness and may double-count sales | Investigate source record; deduplicate only after confirming business rule |
| Negative quantity | `quantity = -1` | Produces negative sales and invalid summary statistics | Treat as correction/return only if supported; otherwise flag or remove |
| Missing delivery days | Blank value | Affects delivery performance analysis | Impute only if justified, or exclude from delivery analysis |
| Outlier order values | Laptop, Smartphone | Can distort averages and trend lines | Report medians alongside means; consider robust statistics |
| Small sample size | 36 rows | Limits statistical confidence | Avoid overclaiming; validate on larger real data |

## 8. Recommendations

1. Clean invalid and duplicate records before final reporting.
2. Use both mean and median for order value because premium products create strong skew.
3. Separate revenue analysis by category so Electronics does not hide lower-value but frequent categories.
4. Track return rate by category, especially Clothing.
5. Expand the dataset before making firm business decisions or training predictive models.

