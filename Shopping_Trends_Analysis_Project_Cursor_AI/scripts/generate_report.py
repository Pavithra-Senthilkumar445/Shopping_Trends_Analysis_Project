import duckdb
from pathlib import Path

OUTPUT = Path("reports/executive_report.md")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(database=":memory:")
conn.execute(open("sql/schema.sql", "r", encoding="utf-8").read())

row_count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
cols = conn.execute("PRAGMA table_info('sales')").df()["name"].tolist()

nulls = conn.execute(
    """
SELECT * FROM (
  SELECT 'customer_id' AS column_name, SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_count FROM sales
  UNION ALL SELECT 'age', SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'gender', SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'item_purchased', SUM(CASE WHEN item_purchased IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'category', SUM(CASE WHEN category IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'purchase_amount', SUM(CASE WHEN purchase_amount IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'location', SUM(CASE WHEN location IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'size', SUM(CASE WHEN size IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'color', SUM(CASE WHEN color IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'season', SUM(CASE WHEN season IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'review_rating', SUM(CASE WHEN review_rating IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'subscription_status', SUM(CASE WHEN subscription_status IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'payment_method', SUM(CASE WHEN payment_method IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'shipping_type', SUM(CASE WHEN shipping_type IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'discount_applied', SUM(CASE WHEN discount_applied IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'promo_code_used', SUM(CASE WHEN promo_code_used IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'previous_purchases', SUM(CASE WHEN previous_purchases IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'preferred_payment_method', SUM(CASE WHEN preferred_payment_method IS NULL THEN 1 ELSE 0 END) FROM sales
  UNION ALL SELECT 'frequency_of_purchases', SUM(CASE WHEN frequency_of_purchases IS NULL THEN 1 ELSE 0 END) FROM sales
) ORDER BY column_name
"""
).df()

total_sales = conn.execute("SELECT SUM(purchase_amount) FROM sales").fetchone()[0] or 0
aov = conn.execute("SELECT AVG(purchase_amount) FROM sales").fetchone()[0] or 0
customers = conn.execute("SELECT COUNT(DISTINCT customer_id) FROM sales").fetchone()[0] or 0
repeat_rate = conn.execute(
    """
    WITH c AS (SELECT customer_id, COUNT(*) n FROM sales GROUP BY customer_id)
    SELECT SUM(CASE WHEN n>1 THEN 1 ELSE 0 END)::DOUBLE/COUNT(*) FROM c
    """
).fetchone()[0] or 0

sales_by_location = conn.execute(
    "SELECT location, SUM(purchase_amount) AS sales FROM sales GROUP BY location ORDER BY sales DESC"
).df()

top_categories = conn.execute(
    "SELECT category, SUM(purchase_amount) AS sales FROM sales GROUP BY category ORDER BY sales DESC"
).df()

seasonal = conn.execute(
    "SELECT season, SUM(purchase_amount) AS sales FROM sales GROUP BY season ORDER BY sales DESC"
).df()

# CLV by Segment (frequency x tenure)
clv = conn.execute(
    """
    WITH segments AS (
      SELECT
        customer_id,
        CASE
          WHEN LOWER(COALESCE(frequency_of_purchases,'')) IN ('weekly','bi-weekly') THEN 'High Frequency'
          WHEN LOWER(COALESCE(frequency_of_purchases,'')) IN ('fortnightly','monthly') THEN 'Medium Frequency'
          ELSE 'Low Frequency'
        END AS freq_segment,
        CASE
          WHEN previous_purchases >= 40 THEN 'Loyal'
          WHEN previous_purchases BETWEEN 20 AND 39 THEN 'Established'
          ELSE 'New'
        END AS tenure_segment
      FROM sales
      GROUP BY customer_id, frequency_of_purchases, previous_purchases
    ), clv AS (
      SELECT s.customer_id, SUM(s.purchase_amount) AS customer_revenue
      FROM sales s
      GROUP BY s.customer_id
    )
    SELECT CONCAT(freq_segment, ' / ', tenure_segment) AS segment,
           COUNT(*) AS customers,
           AVG(customer_revenue) AS avg_clv,
           SUM(customer_revenue) AS segment_revenue
    FROM clv c
    JOIN segments sg ON c.customer_id = sg.customer_id
    GROUP BY segment
    ORDER BY avg_clv DESC
    """
).df()

# Churn proxy by Segment
churn = conn.execute(
    """
    WITH base AS (
      SELECT
        customer_id,
        CASE WHEN LOWER(frequency_of_purchases) IN ('annually') THEN 'High Risk'
             WHEN LOWER(frequency_of_purchases) IN ('every 3 months','quarterly') THEN 'Medium Risk'
             ELSE 'Low Risk' END AS churn_risk,
        previous_purchases
      FROM sales
      GROUP BY customer_id, frequency_of_purchases, previous_purchases
    ), label AS (
      SELECT customer_id, churn_risk,
             CASE WHEN churn_risk='High Risk' AND previous_purchases < 10 THEN 1 ELSE 0 END AS is_churn_proxy
      FROM base
    )
    SELECT churn_risk AS segment, AVG(is_churn_proxy)::DOUBLE AS churn_rate
    FROM label
    GROUP BY segment
    ORDER BY churn_rate DESC
    """
).df()

# Outlier rates (IQR) and skewness
iqr_rates = conn.execute(
    """
    WITH q AS (
      SELECT
        QUANTILE_CONT(age, 0.25) AS age_q1, QUANTILE_CONT(age, 0.75) AS age_q3,
        QUANTILE_CONT(purchase_amount, 0.25) AS amt_q1, QUANTILE_CONT(purchase_amount, 0.75) AS amt_q3,
        QUANTILE_CONT(review_rating, 0.25) AS rating_q1, QUANTILE_CONT(review_rating, 0.75) AS rating_q3,
        QUANTILE_CONT(previous_purchases, 0.25) AS prev_q1, QUANTILE_CONT(previous_purchases, 0.75) AS prev_q3
      FROM sales
    ), b AS (
      SELECT
        age_q1, age_q3, (age_q3-age_q1) AS age_iqr,
        amt_q1, amt_q3, (amt_q3-amt_q1) AS amt_iqr,
        rating_q1, rating_q3, (rating_q3-rating_q1) AS rating_iqr,
        prev_q1, prev_q3, (prev_q3-prev_q1) AS prev_iqr
      FROM q
    ), flags AS (
      SELECT
        CASE WHEN s.age < b.age_q1 - 1.5*b.age_iqr OR s.age > b.age_q3 + 1.5*b.age_iqr THEN 1 ELSE 0 END AS age_outlier,
        CASE WHEN s.purchase_amount < b.amt_q1 - 1.5*b.amt_iqr OR s.purchase_amount > b.amt_q3 + 1.5*b.amt_iqr THEN 1 ELSE 0 END AS amount_outlier,
        CASE WHEN s.review_rating < b.rating_q1 - 1.5*b.rating_iqr OR s.review_rating > b.rating_q3 + 1.5*b.rating_iqr THEN 1 ELSE 0 END AS rating_outlier,
        CASE WHEN s.previous_purchases < b.prev_q1 - 1.5*b.prev_iqr OR s.previous_purchases > b.prev_q3 + 1.5*b.prev_iqr THEN 1 ELSE 0 END AS prev_outlier
      FROM sales s CROSS JOIN b
    )
    SELECT
      AVG(age_outlier)::DOUBLE AS age_outlier_rate,
      AVG(amount_outlier)::DOUBLE AS amount_outlier_rate,
      AVG(rating_outlier)::DOUBLE AS rating_outlier_rate,
      AVG(prev_outlier)::DOUBLE AS previous_purchases_outlier_rate
    FROM flags
    """
).df()

skewness = conn.execute(
    """
    WITH m AS (
      SELECT
        AVG(age) AS age_mean, MEDIAN(age) AS age_median, STDDEV_POP(age) AS age_std,
        AVG(purchase_amount) AS amt_mean, MEDIAN(purchase_amount) AS amt_median, STDDEV_POP(purchase_amount) AS amt_std,
        AVG(review_rating) AS rating_mean, MEDIAN(review_rating) AS rating_median, STDDEV_POP(review_rating) AS rating_std,
        AVG(previous_purchases) AS prev_mean, MEDIAN(previous_purchases) AS prev_median, STDDEV_POP(previous_purchases) AS prev_std
      FROM sales
    )
    SELECT
      CASE WHEN age_std = 0 THEN 0 ELSE 3.0*(age_mean - age_median)/age_std END AS age_skewness,
      CASE WHEN amt_std = 0 THEN 0 ELSE 3.0*(amt_mean - amt_median)/amt_std END AS amount_skewness,
      CASE WHEN rating_std = 0 THEN 0 ELSE 3.0*(rating_mean - rating_median)/rating_std END AS rating_skewness,
      CASE WHEN prev_std = 0 THEN 0 ELSE 3.0*(prev_mean - prev_median)/prev_std END AS previous_purchases_skewness
    FROM m
    """
).df()

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("# Executive Report\n\n")
    f.write("## Dataset Overview\n")
    f.write(f"- Rows: {row_count}\n")
    f.write(f"- Columns: {len(cols)}\n")
    f.write(f"- Column Names: {', '.join(cols)}\n\n")

    f.write("## Data Quality\n")
    f.write(nulls.to_markdown(index=False) + "\n\n")

    f.write("## Core KPIs\n")
    f.write(f"- Total Sales: ${total_sales:,.0f}\n")
    f.write(f"- Average Order Value: ${aov:,.2f}\n")
    f.write(f"- Total Customers: {int(customers)}\n")
    f.write(f"- Repeat Purchase Rate: {repeat_rate*100:.1f}%\n\n")

    f.write("## Sales by Location (Top 10)\n")
    f.write(sales_by_location.head(10).to_markdown(index=False) + "\n\n")

    f.write("## Top Categories\n")
    f.write(top_categories.to_markdown(index=False) + "\n\n")

    f.write("## Seasonal Sales (Categorical Season)\n")
    f.write(seasonal.to_markdown(index=False) + "\n\n")

    f.write("## CLV by Segment\n")
    f.write(clv.to_markdown(index=False) + "\n\n")

    f.write("## Churn Rate by Segment (Proxy)\n")
    f.write(churn.to_markdown(index=False) + "\n\n")

    f.write("## Outlier Rates (IQR)\n")
    f.write(iqr_rates.to_markdown(index=False) + "\n\n")

    f.write("## Skewness (Pearson's 2nd Coefficient)\n")
    f.write(skewness.to_markdown(index=False) + "\n")

print(f"Report written to {OUTPUT}")


