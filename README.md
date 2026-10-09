# Retail Revenue Insights Dashboard

A decision-focused retail analytics dashboard built with Python and Streamlit. It follows **Data → Information → Insight → Decision → Action** and includes executive KPIs, sales trends, product/region drivers, customer concentration, discount risk, and recommended actions.

## Features
- Revenue, profit, orders, unique customers, average order value and profit margin
- Monthly revenue/profit trend
- Category and regional performance
- Product profitability watchlist
- Top-customer revenue concentration and discount risk
- CSV upload, filters, and filtered-data export
- Three pages/tabs: Executive Overview, Sales & Product Analysis, Customer & Risk Analysis

## Run locally
1. Install Python 3.10 or newer.
2. Download/clone this repository.
3. Open a terminal in the project folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL shown in the terminal.

## Dataset
The repository includes `sample_retail_sales.csv`, a **synthetic demo dataset** generated for testing and demonstration; do not present it as real business data. To complete an analysis with sourced data, download a permitted dataset such as the UCI Online Retail dataset and upload its CSV in the sidebar:
- UCI Machine Learning Repository — Online Retail: https://archive.ics.uci.edu/dataset/352/online+retail

The UCI file has different column names and does not include cost/profit. Before using it, transform it into the app's expected format (`Order_Date`, `Revenue`, `Profit`) and document any cost/margin assumptions. Alternatively, use a course-approved Kaggle retail sales dataset with revenue, cost and profit fields. Confirm it is not the masterclass dataset.

## Expected CSV columns
Required: `Order_Date`, `Revenue`, `Profit`
Optional: `Order_ID`, `Customer_ID`, `Category`, `Product`, `Region`, `Quantity`, `Discount`, `Cost`

## Business questions
1. How much revenue and profit were generated in the selected period?
2. Which categories and regions contribute most to revenue and profit?
3. Which product combinations have the weakest profit?
4. Is revenue concentrated among a small number of customers?
5. How common are high-discount or loss-making orders?
6. What should the business investigate or do next?

## Limitations
- Demo figures are synthetic and are not evidence of real business performance.
- Growth compares the selected period against the immediately preceding equal-length period when data is available.
- Findings are descriptive, not causal. Validate before making real decisions.

## GitHub submission checklist
- Create a new **public** GitHub repository named `retail-revenue-insights`.
- Upload `app.py`, `requirements.txt`, `README.md`, `sample_retail_sales.csv`, and `project_report.docx`.
- Include your UI screenshots in the report.
- Add the repository URL to your submission form. Do not submit only a ZIP or Drive folder.
