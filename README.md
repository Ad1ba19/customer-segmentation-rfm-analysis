# Customer Segmentation & RFM Analysis

A Python-based customer analytics project that analyzes transaction data, evaluates purchasing behaviour, and segments customers using Recency, Frequency, and Monetary (RFM) analysis.

## Project Overview

Customer segmentation helps businesses understand customer purchasing patterns, identify high-value customers, and recognize customers who may require retention or re-engagement strategies.

This project uses transaction-level data to calculate customer-level RFM metrics and categorize customers into behavioural segments.

## Business Objectives

- Identify high-value and frequent customers.
- Understand customer purchasing behaviour.
- Identify customers with declining engagement.
- Support targeted customer retention strategies.
- Convert transaction data into actionable business insights.

## Technology Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Environment:** Jupyter Notebook

## Methodology

1. **Data Cleaning:** Inspect transaction data, handle missing values, and prepare consistent records.
2. **Data Transformation:** Aggregate transaction records at customer level.
3. **RFM Calculation:** Calculate Recency, Frequency, and Monetary values.
4. **RFM Scoring:** Assign customer scores based on purchasing behaviour.
5. **Segmentation:** Classify customers using defined RFM scoring rules.
6. **Visualization:** Analyze customer distribution and spending patterns.

## RFM Metrics

| Metric | Description |
|---|---|
| Recency | Days since the customer's last purchase |
| Frequency | Number of purchases made |
| Monetary | Total amount spent |

## Customer Segmentation

The analysis can identify customer groups such as:

- Champions
- Loyal Customers
- Potential Loyalists
- At-Risk Customers
- Customers Needing Attention
- Hibernating Customers

*Final segment definitions depend on the scoring rules implemented in the analysis.*

## Repository Structure

- `data/` — Dataset files, where redistribution is permitted.
- `notebooks/` — Data preparation and analysis.
- `src/` — Reusable Python modules.
- `outputs/` — Generated reports and visualizations.
- `tests/` — Validation and unit tests.

## Key Insights

Add actual findings from the analysis here, including:
- Total customers analyzed.
- Customer distribution across segments.
- Revenue contribution by segment.
- High-value and at-risk customer observations.

## How to Run

```bash
git clone https://github.com/Ad1ba19/customer-segmentation-rfm-analysis.git

cd customer-segmentation-rfm-analysis

python -m venv venv

pip install -r requirements.txt

jupyter notebook
```

## Future Enhancements

- Automated data processing pipeline.
- Interactive customer segmentation dashboard.
- Automated customer segment reporting.
- Additional clustering techniques, if validated against the RFM baseline.

## Author

**Adiba Khan**

Software Engineer | Backend Engineering, Data Engineering & AI Systems

[LinkedIn](https://www.linkedin.com/in/adiba-khan-20ba57230/)
