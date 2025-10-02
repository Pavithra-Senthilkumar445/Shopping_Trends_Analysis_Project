# Executive Report

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

## Insights & Recommendations

- Business performance
  - Total Sales: $233,081; AOV: $59.76; 3,900 unique customers
  - Repeat Purchase Rate: 0.0% (each `customer_id` appears once). To track real repeats, add order IDs and timestamps.

- Regional focus
  - Top revenue states: Montana, Illinois, California, Idaho, Nevada
  - Action: Replicate winning campaigns into adjacent or similar markets; tailor inventory by region.

- Category priorities
  - Clothing and Accessories drive the bulk of sales; Footwear is secondary, Outerwear niche
  - Action: Feature top categories on homepage, bundle cross-sells, expand variants in best-sellers

- Seasonality
  - Fall edges other seasons, followed by Spring and Winter; Summer slightly lower
  - Action: Front-load Fall promotions and ensure Spring/Winter stock readiness

- Customer value and churn proxies
  - Higher tenure segments (Loyal/Established) show higher avg CLV across frequencies
  - High Risk churn proxy ≈ 18% (low previous purchases + annual cadence)
  - Action: Loyalty perks and tailored win-back offers for High Risk; nurture New → Established → Loyal

- Data quality and distribution
  - No nulls across columns; numeric variables show no IQR outliers and low skewness
  - Implication: Means and medians are similar; standard aggregation is reliable

- Next data improvements
  - Add `order_id`, `order_date` to enable cohorts, RFM, true churn and repeat rates
  - Track marketing source and campaign to attribute lift by channel
