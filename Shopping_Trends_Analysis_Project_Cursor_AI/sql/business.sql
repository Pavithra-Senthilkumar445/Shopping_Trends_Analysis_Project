-- Business analysis queries

-- Sales by Location
SELECT location, SUM(purchase_amount) AS sales, COUNT(*) AS orders
FROM sales
GROUP BY location
ORDER BY sales DESC;

-- Sales by Size & Color
SELECT size, color, SUM(purchase_amount) AS sales, COUNT(*) AS orders
FROM sales
GROUP BY size, color
ORDER BY sales DESC;

-- Top-Selling Categories
SELECT category, SUM(purchase_amount) AS sales, COUNT(*) AS orders
FROM sales
GROUP BY category
ORDER BY sales DESC;

-- Seasonal Sales Trends (using provided Season categorical column)
SELECT season, SUM(purchase_amount) AS sales, COUNT(*) AS orders
FROM sales
GROUP BY season
ORDER BY sales DESC;

-- Customer Lifetime Value (CLV) by Segment
-- Define segments from frequency and previous_purchases
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
SELECT
  CONCAT(freq_segment, ' / ', tenure_segment) AS segment,
  COUNT(*) AS customers,
  AVG(customer_revenue) AS avg_clv,
  SUM(customer_revenue) AS segment_revenue
FROM clv c
JOIN segments sg ON c.customer_id = sg.customer_id
GROUP BY segment
ORDER BY avg_clv DESC;

-- Repeat Purchase Rate (business view)
WITH customer_orders AS (
  SELECT customer_id, COUNT(*) AS orders_per_customer
  FROM sales
  GROUP BY customer_id
)
SELECT
  SUM(CASE WHEN orders_per_customer > 1 THEN 1 ELSE 0 END)::DOUBLE / COUNT(*) AS repeat_purchase_rate
FROM customer_orders;

-- Churn Rate by Segment (proxy):
-- Without dates, proxy churn as customers with 'Annually' or 'Every 3 Months' frequency and low previous purchases
WITH base AS (
  SELECT
    customer_id,
    CASE
      WHEN LOWER(frequency_of_purchases) IN ('annually') THEN 'High Risk'
      WHEN LOWER(frequency_of_purchases) IN ('every 3 months','quarterly') THEN 'Medium Risk'
      ELSE 'Low Risk'
    END AS churn_risk,
    previous_purchases
  FROM sales
  GROUP BY customer_id, frequency_of_purchases, previous_purchases
), label AS (
  SELECT customer_id,
    churn_risk,
    CASE WHEN churn_risk = 'High Risk' AND previous_purchases < 10 THEN 1 ELSE 0 END AS is_churn_proxy
  FROM base
)
SELECT churn_risk AS segment, AVG(is_churn_proxy)::DOUBLE AS churn_rate
FROM label
GROUP BY segment
ORDER BY churn_rate DESC;







