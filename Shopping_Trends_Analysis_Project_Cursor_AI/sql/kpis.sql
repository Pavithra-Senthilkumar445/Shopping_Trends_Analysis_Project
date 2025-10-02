-- Core KPIs in absence of explicit order ids:
-- Treat each row as a transaction. Customer-level repeats inferred by multiple rows per customer.

-- Total Sales
SELECT SUM(purchase_amount) AS total_sales FROM sales;

-- Average Order Value (AOV)
SELECT AVG(purchase_amount) AS average_order_value FROM sales;

-- Total Customers
SELECT COUNT(DISTINCT customer_id) AS total_customers FROM sales;

-- Repeat Purchase Rate = customers with >1 orders / total customers
WITH customer_orders AS (
  SELECT customer_id, COUNT(*) AS orders_per_customer
  FROM sales
  GROUP BY customer_id
)
SELECT
  SUM(CASE WHEN orders_per_customer > 1 THEN 1 ELSE 0 END)::DOUBLE / COUNT(*) AS repeat_purchase_rate
FROM customer_orders;







