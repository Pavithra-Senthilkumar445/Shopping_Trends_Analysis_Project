-- EDA: structure, nulls, missingness, duplicates, descriptive stats

-- 1) Row/column counts and schema
PRAGMA table_info('sales');
SELECT COUNT(*) AS row_count FROM sales;

-- 2) Null counts per column
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
ORDER BY column_name;

-- 3) Duplicate detection: exact duplicates across key descriptive fields
SELECT customer_id, age, gender, item_purchased, category, purchase_amount, location, size, color, season,
       review_rating, subscription_status, payment_method, shipping_type, discount_applied, promo_code_used,
       previous_purchases, preferred_payment_method, frequency_of_purchases,
       COUNT(*) AS dup_count
FROM sales
GROUP BY ALL
HAVING COUNT(*) > 1
ORDER BY dup_count DESC;

-- 4) Descriptive stats for numeric columns
WITH stats AS (
  SELECT
    COUNT(*) AS n,
    MIN(age) AS age_min, QUANTILE_CONT(age, 0.25) AS age_q1, MEDIAN(age) AS age_median, QUANTILE_CONT(age, 0.75) AS age_q3, MAX(age) AS age_max, AVG(age) AS age_mean, STDDEV_POP(age) AS age_std,
    MIN(purchase_amount) AS amt_min, QUANTILE_CONT(purchase_amount, 0.25) AS amt_q1, MEDIAN(purchase_amount) AS amt_median, QUANTILE_CONT(purchase_amount, 0.75) AS amt_q3, MAX(purchase_amount) AS amt_max, AVG(purchase_amount) AS amt_mean, STDDEV_POP(purchase_amount) AS amt_std,
    MIN(review_rating) AS rating_min, QUANTILE_CONT(review_rating, 0.25) AS rating_q1, MEDIAN(review_rating) AS rating_median, QUANTILE_CONT(review_rating, 0.75) AS rating_q3, MAX(review_rating) AS rating_max, AVG(review_rating) AS rating_mean, STDDEV_POP(review_rating) AS rating_std,
    MIN(previous_purchases) AS prev_min, QUANTILE_CONT(previous_purchases, 0.25) AS prev_q1, MEDIAN(previous_purchases) AS prev_median, QUANTILE_CONT(previous_purchases, 0.75) AS prev_q3, MAX(previous_purchases) AS prev_max, AVG(previous_purchases) AS prev_mean, STDDEV_POP(previous_purchases) AS prev_std
  FROM sales
)
SELECT * FROM stats;


