import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Clothing Sales Analysis", layout="wide")

@st.cache_resource
def get_conn():
    conn = duckdb.connect(database=":memory:")
    conn.execute(open("sql/schema.sql", "r", encoding="utf-8").read())
    return conn

conn = get_conn()

st.title("Clothing Sales Analysis Dashboard")
st.caption("Interactive portfolio project powered by DuckDB + Streamlit")

with st.sidebar:
    st.header("Filters")
    locations = [r[0] for r in conn.execute("SELECT DISTINCT location FROM sales ORDER BY location").fetchall()]
    categories = [r[0] for r in conn.execute("SELECT DISTINCT category FROM sales ORDER BY category").fetchall()]
    seasons = [r[0] for r in conn.execute("SELECT DISTINCT season FROM sales ORDER BY season").fetchall()]
    sizes = [r[0] for r in conn.execute("SELECT DISTINCT size FROM sales ORDER BY size").fetchall()]
    colors = [r[0] for r in conn.execute("SELECT DISTINCT color FROM sales ORDER BY color").fetchall()]

    loc_sel = st.multiselect("Location", options=locations, default=locations)
    cat_sel = st.multiselect("Category", options=categories, default=categories)
    season_sel = st.multiselect("Season", options=seasons, default=seasons)
    size_sel = st.multiselect("Size", options=sizes, default=sizes)
    color_sel = st.multiselect("Color", options=colors, default=colors)

def in_clause(column: str, values: list[str]):
    if not values:
        return "1=0", []
    placeholders = ",".join(["?"] * len(values))
    return f"{column} IN ({placeholders})", list(values)

where_clauses = []
params_list: list = []
for col, vals in [
    ("location", loc_sel),
    ("category", cat_sel),
    ("season", season_sel),
    ("size", size_sel),
    ("color", color_sel),
]:
    clause, p = in_clause(col, vals)
    where_clauses.append(clause)
    params_list.extend(p)

where_sql = " WHERE " + " AND ".join(where_clauses)

# KPIs
kpi_total_sales = conn.execute("SELECT SUM(purchase_amount) FROM sales" + where_sql, params_list).fetchone()[0]
kpi_aov = conn.execute("SELECT AVG(purchase_amount) FROM sales" + where_sql, params_list).fetchone()[0]
kpi_customers = conn.execute("SELECT COUNT(DISTINCT customer_id) FROM sales" + where_sql, params_list).fetchone()[0]
repeat_rate = conn.execute(
    """
    WITH customer_orders AS (
      SELECT customer_id, COUNT(*) AS n FROM sales%s GROUP BY customer_id
    )
    SELECT SUM(CASE WHEN n>1 THEN 1 ELSE 0 END)::DOUBLE/COUNT(*) FROM customer_orders
    """ % where_sql,
    params_list,
).fetchone()[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${kpi_total_sales:,.0f}" if kpi_total_sales else "$0")
col2.metric("Average Order Value", f"${kpi_aov:,.2f}" if kpi_aov else "$0.00")
col3.metric("Total Customers", int(kpi_customers or 0))
col4.metric("Repeat Purchase Rate", f"{(repeat_rate or 0)*100:.1f}%")

# Sales by Location
sales_by_location = conn.execute(
    "SELECT location, SUM(purchase_amount) AS sales FROM sales%s GROUP BY location ORDER BY sales DESC" % where_sql,
    params_list,
).df()

# Sales by Size & Color
sales_by_size_color = conn.execute(
    "SELECT size, color, SUM(purchase_amount) AS sales FROM sales%s GROUP BY size, color ORDER BY sales DESC" % where_sql,
    params_list,
).df()

# Top Categories
top_categories = conn.execute(
    "SELECT category, SUM(purchase_amount) AS sales FROM sales%s GROUP BY category ORDER BY sales DESC" % where_sql,
    params_list,
).df()

# Seasonal Trends
seasonal = conn.execute(
    "SELECT season, SUM(purchase_amount) AS sales FROM sales%s GROUP BY season ORDER BY sales DESC" % where_sql,
    params_list,
).df()

tab1, tab2, tab3, tab4 = st.tabs(["Sales by Location", "Size & Color", "Top Categories", "Seasonal Trends"])
with tab1:
    st.bar_chart(sales_by_location, x="location", y="sales")
with tab2:
    st.dataframe(sales_by_size_color)
with tab3:
    st.bar_chart(top_categories, x="category", y="sales")
with tab4:
    st.bar_chart(seasonal, x="season", y="sales")

# CLV by Segment - simplified to avoid parameter issues
try:
    clv_df = conn.execute(
        """
        WITH segments AS (
          SELECT customer_id,
            CASE WHEN LOWER(COALESCE(frequency_of_purchases,'')) IN ('weekly','bi-weekly') THEN 'High Frequency'
                 WHEN LOWER(COALESCE(frequency_of_purchases,'')) IN ('fortnightly','monthly') THEN 'Medium Frequency'
                 ELSE 'Low Frequency' END AS freq_segment,
            CASE WHEN previous_purchases >= 40 THEN 'Loyal'
                 WHEN previous_purchases BETWEEN 20 AND 39 THEN 'Established'
                 ELSE 'New' END AS tenure_segment
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
    
    st.subheader("Customer Lifetime Value (CLV) by Segment")
    st.dataframe(clv_df)
except Exception as e:
    st.error(f"CLV calculation error: {e}")

# Churn proxy by Segment
try:
    churn_df = conn.execute(
        """
        WITH base AS (
          SELECT customer_id,
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
    
    st.subheader("Churn Rate by Segment (Proxy)")
    st.bar_chart(churn_df, x="segment", y="churn_rate")
except Exception as e:
    st.error(f"Churn calculation error: {e}")

st.caption("Note: No dates available; season is categorical and used for seasonal breakdowns. Repeat and churn are proxied.")



