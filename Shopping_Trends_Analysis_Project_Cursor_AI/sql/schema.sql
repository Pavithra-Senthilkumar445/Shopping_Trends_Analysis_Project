-- Create a clean, analysis-ready table from the raw CSV using DuckDB
-- This script assumes the CSV exists at data/Clothing_Sales_Project_Cursor_AI.csv
-- It creates a database table with sanitized column names and appropriate types.

CREATE OR REPLACE TABLE sales_raw AS
SELECT * FROM read_csv_auto('data/Clothing_Sales_Project_Cursor_AI.csv', header=true);

-- Create a cleaned table with standardized column names and types
CREATE OR REPLACE TABLE sales AS
SELECT
    CAST("Customer ID" AS INTEGER)                       AS customer_id,
    CAST("Age" AS INTEGER)                               AS age,
    CAST("Gender" AS VARCHAR)                            AS gender,
    CAST("Item Purchased" AS VARCHAR)                    AS item_purchased,
    CAST("Category" AS VARCHAR)                          AS category,
    CAST("Purchase Amount (USD)" AS DOUBLE)              AS purchase_amount,
    CAST("Location" AS VARCHAR)                          AS location,
    CAST("Size" AS VARCHAR)                              AS size,
    CAST("Color" AS VARCHAR)                             AS color,
    CAST("Season" AS VARCHAR)                            AS season,
    CAST("Review Rating" AS DOUBLE)                      AS review_rating,
    CAST("Subscription Status" AS VARCHAR)               AS subscription_status,
    CAST("Payment Method" AS VARCHAR)                    AS payment_method,
    CAST("Shipping Type" AS VARCHAR)                     AS shipping_type,
    CAST("Discount Applied" AS VARCHAR)                  AS discount_applied,
    CAST("Promo Code Used" AS VARCHAR)                   AS promo_code_used,
    CAST("Previous Purchases" AS INTEGER)                AS previous_purchases,
    CAST("Preferred Payment Method" AS VARCHAR)          AS preferred_payment_method,
    CAST("Frequency of Purchases" AS VARCHAR)            AS frequency_of_purchases
FROM sales_raw;

-- Convenience view with boolean-like flags coerced to 0/1
CREATE OR REPLACE VIEW sales_enriched AS
SELECT
    *,
    CASE LOWER(COALESCE(subscription_status, '')) WHEN 'yes' THEN 1 ELSE 0 END AS is_subscribed,
    CASE LOWER(COALESCE(discount_applied, ''))   WHEN 'yes' THEN 1 ELSE 0 END AS discount_flag,
    CASE LOWER(COALESCE(promo_code_used, ''))    WHEN 'yes' THEN 1 ELSE 0 END AS promo_flag
FROM sales;







