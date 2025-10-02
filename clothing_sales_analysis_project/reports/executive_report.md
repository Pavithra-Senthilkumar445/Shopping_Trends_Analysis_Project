# Shopping Trend Analysis - Executive Report

## Dataset Overview
- Rows: 3900
- Columns: 19
- Column Names: customer_id, age, gender, item_purchased, category, purchase_amount, location, size, color, season, review_rating, subscription_status, payment_method, shipping_type, discount_applied, promo_code_used, previous_purchases, preferred_payment_method, frequency_of_purchases

## Data Quality
| column_name              |   null_count |
|:-------------------------|-------------:|
| age                      |            0 |
| category                 |            0 |
| color                    |            0 |
| customer_id              |            0 |
| discount_applied         |            0 |
| frequency_of_purchases   |            0 |
| gender                   |            0 |
| item_purchased           |            0 |
| location                 |            0 |
| payment_method           |            0 |
| preferred_payment_method |            0 |
| previous_purchases       |            0 |
| promo_code_used          |            0 |
| purchase_amount          |            0 |
| review_rating            |            0 |
| season                   |            0 |
| shipping_type            |            0 |
| size                     |            0 |
| subscription_status      |            0 |

## Core KPIs
- Total Sales: $233,081
- Average Order Value: $59.76
- Total Customers: 3900
- Repeat Purchase Rate: 0.0%

## Sales by Location (Top 10)
| location      |   sales |
|:--------------|--------:|
| Montana       |    5784 |
| Illinois      |    5617 |
| California    |    5605 |
| Idaho         |    5587 |
| Nevada        |    5514 |
| Alabama       |    5261 |
| New York      |    5257 |
| North Dakota  |    5220 |
| West Virginia |    5174 |
| Nebraska      |    5172 |

## Top Categories
| category    |   sales |
|:------------|--------:|
| Clothing    |  104264 |
| Accessories |   74200 |
| Footwear    |   36093 |
| Outerwear   |   18524 |

## Seasonal Sales (Categorical Season)
| season   |   sales |
|:---------|--------:|
| Fall     |   60018 |
| Spring   |   58679 |
| Winter   |   58607 |
| Summer   |   55777 |

## CLV by Segment
| segment                        |   customers |   avg_clv |   segment_revenue |
|:-------------------------------|------------:|----------:|------------------:|
| Low Frequency / Loyal          |         397 |   60.8312 |             24150 |
| Low Frequency / New            |         647 |   60.1036 |             38887 |
| High Frequency / Loyal         |         234 |   59.8632 |             14008 |
| High Frequency / Established   |         431 |   59.8353 |             25789 |
| High Frequency / New           |         421 |   59.8314 |             25189 |
| Low Frequency / Established    |         675 |   59.6163 |             40241 |
| Medium Frequency / Loyal       |         216 |   59.6157 |             12877 |
| Medium Frequency / New         |         410 |   59.1098 |             24235 |
| Medium Frequency / Established |         469 |   59.0725 |             27705 |

## Churn Rate by Segment (Proxy)
| segment     |   churn_rate |
|:------------|-------------:|
| High Risk   |      0.18007 |
| Medium Risk |      0       |
| Low Risk    |      0       |

## Outlier Rates (IQR)
|   age_outlier_rate |   amount_outlier_rate |   rating_outlier_rate |   previous_purchases_outlier_rate |
|-------------------:|----------------------:|----------------------:|----------------------------------:|
|                  0 |                     0 |                     0 |                                 0 |

## Skewness (Pearson's 2nd Coefficient)
|   age_skewness |   amount_skewness |   rating_skewness |   previous_purchases_skewness |
|---------------:|------------------:|------------------:|------------------------------:|
|      0.0135071 |        -0.0298502 |          0.209244 |                     0.0730076 |

## Gender & Demographics Analysis

- **Customer Base**: 68% Male (2,652) vs 32% Female (1,248) customers
  - Male sales: $157,890 (67.7% of total)
  - Female sales: $75,191 (32.3% of total)
  - Total sales: $233,081

- **Key Gender Insights**:
  - **Female AOV: $60.25** vs Male AOV: $59.54
  - Females spend more per transaction despite being fewer customers
  - Both genders prefer Clothing and Accessories categories
  - Age range: 18-70 years across both genders

- **Category Breakdown by Gender**:
  - **Female**: Clothing ($33,636), Accessories ($23,819), Footwear ($11,835), Outerwear ($5,901)
  - **Male**: Clothing ($70,628), Accessories ($50,381), Footwear ($24,258), Outerwear ($12,623)

## Payment Method Analysis

| Payment Method | Transactions | Total Sales | Usage % |
|:---------------|-------------:|------------:|--------:|
| Credit Card    | 792          | $47,234     | 20.3%   |
| Debit Card     | 784          | $46,892     | 20.1%   |
| PayPal         | 775          | $46,348     | 19.9%   |
| Cash           | 650          | $31,203     | 16.7%   |
| Venmo          | 549          | $30,802     | 14.1%   |
| Bank Transfer  | 350          | $30,602     | 8.9%    |

## Sales by Size & Color (Top 10)

| Size | Color     | Orders | Total Sales | Avg Order Value |
|:-----|:----------|-------:|------------:|----------------:|
| M    | Olive     | 12     | $728        | $60.67          |
| L    | Yellow    | 11     | $715        | $65.00          |
| S    | Silver    | 10     | $692        | $69.20          |
| M    | Turquoise | 11     | $689        | $62.64          |
| L    | Lavender  | 10     | $675        | $67.50          |

## Repeat Purchase Rate Explanation

**Why 0.0% Repeat Purchase Rate:**
- Each customer_id appears exactly once in the dataset (3,900 unique customers = 3,900 total transactions)
- This indicates the dataset is a cross-sectional snapshot rather than longitudinal transaction data
- No customer has multiple purchase records, making repeat rate calculation impossible
- For true repeat analysis, need order_id and transaction_date fields to track customer behavior over time

## Statistical Quality Explanation

**IQR 0.0% Outlier Rate Means:**
- **No extreme values** detected using standard statistical methods
- All data points fall within 1.5 × IQR from Q1 and Q3 quartiles
- **High data quality** with consistent customer behavior patterns
- Safe to use mean/average calculations without outlier distortion
- Indicates well-bounded dataset with no unusual spikes or anomalies

## Interactive Dashboard Features

- **Enhanced Filters**: Location, Category, Season, Size, Age Group, Gender
- **Gender Analysis**: Complete breakdown of spending by demographics with charts
- **Payment Method Analysis**: Distribution across 6 payment types with usage percentages
- **Size & Color Analysis**: Top-performing combinations with order volumes
- **Category Details**: Total sales amounts and percentages for each category
- **Professional UI**: Clean, modern interface with 6 interactive chart types

## Insights & Recommendations

- **Business Performance**
  - Total Sales: $233,081; Overall AOV: $59.76; 3,900 customers (68% Male, 32% Female)
  - Repeat Purchase Rate: 0.0% (each `customer_id` appears once). To track real repeats, add order IDs and timestamps.

- **Gender Strategy Opportunity**
  - **Key Finding**: Female customers have higher AOV ($60.25 vs $59.54) but represent only 32% of customer base
  - Action: Increase female customer acquisition while maintaining their higher spending patterns

- **Regional Focus**
  - Top revenue states: Montana, Illinois, California, Idaho, Nevada
  - Action: Replicate winning campaigns into adjacent or similar markets; tailor inventory by region.

- **Category Priorities**
  - Clothing ($104,264 - 44.7%) and Accessories ($74,200 - 31.8%) drive 76.5% of sales
  - Footwear ($36,093 - 15.5%) and Outerwear ($18,524 - 7.9%) are secondary
  - Action: Feature top categories prominently, bundle cross-sells, expand variants in best-sellers

- **Demographic Strategy**
  - **Female customers**: Higher AOV but underrepresented - focus on acquisition
  - **Male customers**: Larger volume but slightly lower AOV - optimize conversion
  - Both genders show similar category preferences - leverage cross-selling opportunities
  - Consider gender-specific product recommendations and targeted marketing campaigns

- **Data Quality Excellence**
  - No nulls across columns; numeric variables show no IQR outliers and low skewness
  - Excellent data quality enables reliable statistical analysis and business decisions

- **Payment Strategy**
  - Balanced payment method usage (Credit Card 20.3%, Debit Card 20.1%, PayPal 19.9%)
  - No single payment method dominates - good diversification
  - Consider payment method-specific promotions and incentives

- **Product Strategy**  
  - Size & Color combinations show clear preferences (Medium Olive, Large Yellow top performers)
  - XL Brown has highest AOV ($73.89) despite fewer orders - premium opportunity
  - Use size/color data for inventory optimization and targeted marketing

- **Data Structure Insights**
  - Cross-sectional dataset (each customer appears once) limits longitudinal analysis
  - 0.0% repeat rate is data structure limitation, not business performance issue
  - Current data excellent for demographic and preference analysis

- **Technology Improvements**
  - Add `order_id`, `order_date` to enable cohorts, RFM, true churn and repeat rates
  - Implement real-time filtering and dynamic dashboard updates
  - Track marketing source and campaign attribution
  - Consider A/B testing framework for payment method optimization
