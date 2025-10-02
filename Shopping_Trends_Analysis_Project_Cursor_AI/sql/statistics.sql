-- Statistical analysis: outlier detection (IQR and z-score) and skewness (Pearson) per numeric column

-- IQR-based outlier flags
WITH quantiles AS (
  SELECT
    QUANTILE_CONT(age, 0.25) AS age_q1,
    QUANTILE_CONT(age, 0.75) AS age_q3,
    QUANTILE_CONT(purchase_amount, 0.25) AS amt_q1,
    QUANTILE_CONT(purchase_amount, 0.75) AS amt_q3,
    QUANTILE_CONT(review_rating, 0.25) AS rating_q1,
    QUANTILE_CONT(review_rating, 0.75) AS rating_q3,
    QUANTILE_CONT(previous_purchases, 0.25) AS prev_q1,
    QUANTILE_CONT(previous_purchases, 0.75) AS prev_q3
  FROM sales
), bounds AS (
  SELECT
    age_q1, age_q3, (age_q3 - age_q1) AS age_iqr,
    amt_q1, amt_q3, (amt_q3 - amt_q1) AS amt_iqr,
    rating_q1, rating_q3, (rating_q3 - rating_q1) AS rating_iqr,
    prev_q1, prev_q3, (prev_q3 - prev_q1) AS prev_iqr
  FROM quantiles
)
SELECT
  s.customer_id,
  CASE WHEN s.age < b.age_q1 - 1.5*b.age_iqr OR s.age > b.age_q3 + 1.5*b.age_iqr THEN 1 ELSE 0 END AS age_outlier,
  CASE WHEN s.purchase_amount < b.amt_q1 - 1.5*b.amt_iqr OR s.purchase_amount > b.amt_q3 + 1.5*b.amt_iqr THEN 1 ELSE 0 END AS amount_outlier,
  CASE WHEN s.review_rating < b.rating_q1 - 1.5*b.rating_iqr OR s.review_rating > b.rating_q3 + 1.5*b.rating_iqr THEN 1 ELSE 0 END AS rating_outlier,
  CASE WHEN s.previous_purchases < b.prev_q1 - 1.5*b.prev_iqr OR s.previous_purchases > b.prev_q3 + 1.5*b.prev_iqr THEN 1 ELSE 0 END AS prev_purchases_outlier
FROM sales s CROSS JOIN bounds b;

-- z-score flags using population stddev
WITH stats AS (
  SELECT
    AVG(age) AS age_mean, STDDEV_POP(age) AS age_std,
    AVG(purchase_amount) AS amt_mean, STDDEV_POP(purchase_amount) AS amt_std,
    AVG(review_rating) AS rating_mean, STDDEV_POP(review_rating) AS rating_std,
    AVG(previous_purchases) AS prev_mean, STDDEV_POP(previous_purchases) AS prev_std
  FROM sales
)
SELECT
  s.customer_id,
  CASE WHEN stats.age_std = 0 THEN 0 ELSE ABS((s.age - stats.age_mean)/stats.age_std) > 3 END AS age_z_outlier,
  CASE WHEN stats.amt_std = 0 THEN 0 ELSE ABS((s.purchase_amount - stats.amt_mean)/stats.amt_std) > 3 END AS amount_z_outlier,
  CASE WHEN stats.rating_std = 0 THEN 0 ELSE ABS((s.review_rating - stats.rating_mean)/stats.rating_std) > 3 END AS rating_z_outlier,
  CASE WHEN stats.prev_std = 0 THEN 0 ELSE ABS((s.previous_purchases - stats.prev_mean)/stats.prev_std) > 3 END AS prev_purchases_z_outlier
FROM sales s, stats;

-- Skewness direction using Pearson's second coefficient of skewness: 3*(mean - median)/std
WITH moments AS (
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
  CASE WHEN prev_std = 0 THEN 0 ELSE 3.0*(prev_mean - prev_median)/prev_std END AS prev_purchases_skewness;


