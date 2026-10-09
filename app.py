"""
Retail Revenue Insights Dashboard
Run: streamlit run app.py
This project includes a synthetic demo CSV so it runs immediately.
Replace it with your own permitted dataset using the upload control.
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Retail Revenue Insights", page_icon="📊", layout="wide")
st.title("📊 Retail Revenue Insights")
st.caption("Turn sales data into decisions • KPIs → Trends → Drivers → Risk & Opportunity → Action")

REQUIRED = ["Order_Date", "Revenue", "Profit"]
uploaded = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])
if uploaded is not None:
    raw = pd.read_csv(uploaded)
    source_name = uploaded.name
else:
    raw = pd.read_csv("sample_retail_sales.csv")
    source_name = "Included synthetic demo data"

st.sidebar.markdown("---")
st.sidebar.caption(f"Data source: {source_name}")
st.sidebar.caption("Expected columns: Order_Date, Revenue, Profit. Optional: Order_ID, Customer_ID, Category, Product, Region, Quantity, Discount, Cost.")
if not all(c in raw.columns for c in REQUIRED):
    st.error("Your CSV must include Order_Date, Revenue and Profit columns.")
    st.stop()

raw["Order_Date"] = pd.to_datetime(raw["Order_Date"], errors="coerce")
for c in ["Revenue","Profit","Quantity","Discount","Cost"]:
    if c in raw.columns:
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
raw = raw.dropna(subset=["Order_Date","Revenue","Profit"]).copy()
if raw.empty:
    st.error("No valid rows found. Check dates and numeric Revenue/Profit values.")
    st.stop()
raw["Month"] = raw["Order_Date"].dt.to_period("M").dt.to_timestamp()
if "Order_ID" not in raw: raw["Order_ID"] = raw.index.astype(str)
if "Customer_ID" not in raw: raw["Customer_ID"] = "Unknown"
if "Category" not in raw: raw["Category"] = "Uncategorized"
if "Product" not in raw: raw["Product"] = "Unknown product"
if "Region" not in raw: raw["Region"] = "Unknown"
if "Quantity" not in raw: raw["Quantity"] = 1
if "Discount" not in raw: raw["Discount"] = 0

st.sidebar.subheader("Filters")
min_date, max_date = raw["Order_Date"].min().date(), raw["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
categories = sorted(raw["Category"].astype(str).unique())
chosen_categories = st.sidebar.multiselect("Category", categories, default=categories)
regions = sorted(raw["Region"].astype(str).unique())
chosen_regions = st.sidebar.multiselect("Region", regions, default=regions)

if isinstance(date_range, tuple) and len(date_range)==2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
    data = raw[(raw.Order_Date >= start) & (raw.Order_Date < end)]
else:
    data = raw.copy()
data = data[data.Category.astype(str).isin(chosen_categories) & data.Region.astype(str).isin(chosen_regions)]
if data.empty:
    st.warning("No rows match these filters. Adjust the date range, category or region.")
    st.stop()

revenue = data.Revenue.sum()
profit = data.Profit.sum()
orders = data.Order_ID.nunique()
customers = data.Customer_ID.nunique()
aov = revenue / orders if orders else 0
margin = profit / revenue * 100 if revenue else 0
prev_start = data.Order_Date.min() - (data.Order_Date.max()-data.Order_Date.min()+pd.Timedelta(days=1))
prev_end = data.Order_Date.min()
previous = raw[(raw.Order_Date >= prev_start) & (raw.Order_Date < prev_end)]
growth = ((revenue - previous.Revenue.sum()) / previous.Revenue.sum() * 100) if len(previous) and previous.Revenue.sum() else np.nan

tab1, tab2, tab3 = st.tabs(["Executive Overview", "Sales & Product Analysis", "Customer & Risk Analysis"])
with tab1:
    st.subheader("Executive Overview")
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Revenue", f"${revenue:,.0f}")
    c2.metric("Profit", f"${profit:,.0f}")
    c3.metric("Orders", f"{orders:,}")
    c4.metric("Customers", f"{customers:,}")
    c5.metric("Average order value", f"${aov:,.2f}")
    st.caption(f"Profit margin: {margin:.1f}%  •  Period-over-period growth: {growth:.1f}%" if pd.notna(growth) else f"Profit margin: {margin:.1f}%  •  Growth: not available for the selected period")
    monthly = data.groupby("Month", as_index=False).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"))
    st.markdown("#### Trend: revenue and profit by month")
    st.line_chart(monthly.set_index("Month")[["Revenue","Profit"]])
    st.markdown("#### Decision summary")
    if margin < 15:
        st.warning("Margin is below 15%. Review discounting and product costs before increasing promotion spend.")
    else:
        st.success("Margin is at least 15%. Protect profitable categories while testing targeted growth.")
    if pd.notna(growth) and growth < 0:
        st.warning("Revenue is down versus the immediately preceding equal-length period. Investigate category and regional changes.")
    else:
        st.info("Compare category and regional contributions before allocating additional budget.")
with tab2:
    st.subheader("Sales & Product Analysis")
    left,right=st.columns(2)
    with left:
        st.markdown("#### Revenue by category")
        by_cat=data.groupby("Category").agg(Revenue=("Revenue","sum"), Profit=("Profit","sum")).sort_values("Revenue",ascending=False)
        st.bar_chart(by_cat[["Revenue"]])
    with right:
        st.markdown("#### Profit by region")
        by_region=data.groupby("Region").agg(Profit=("Profit","sum")).sort_values("Profit",ascending=False)
        st.bar_chart(by_region)
    st.markdown("#### Product drivers")
    product=data.groupby(["Category","Product"]).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"), Units=("Quantity","sum")).sort_values("Profit")
    st.dataframe(product.reset_index().sort_values("Profit",ascending=False), use_container_width=True, hide_index=True)
    low=product.head(5)
    if len(low):
        st.markdown("**Actionable watchlist:** Review the five lowest-profit product/category combinations for pricing, returns, costs or discount leakage.")
with tab3:
    st.subheader("Customer & Risk Analysis")
    left,right=st.columns(2)
    with left:
        cust=data.groupby("Customer_ID").agg(Revenue=("Revenue","sum"), Orders=("Order_ID","nunique"), Profit=("Profit","sum")).sort_values("Revenue",ascending=False)
        st.markdown("#### Top 10 customers by revenue")
        st.dataframe(cust.head(10).reset_index(), use_container_width=True, hide_index=True)
        concentration = cust.head(10).Revenue.sum()/revenue*100 if revenue else 0
        st.metric("Revenue from top 10 customers", f"{concentration:.1f}%")
    with right:
        st.markdown("#### Discount and margin risk")
        data["Profit_Margin_Pct"] = np.where(data.Revenue != 0, data.Profit/data.Revenue*100, 0)
        st.metric("Rows with discount ≥ 20%", f"{(data.Discount >= .20).mean()*100:.1f}%")
        st.metric("Loss-making rows", f"{(data.Profit < 0).sum():,}")
        st.markdown("**Recommended actions**")
        st.write("1. Check high-discount orders for low or negative profit.")
        st.write("2. Avoid depending on a small set of customers; track repeat orders and concentration monthly.")
        st.write("3. Investigate low-profit products before expanding their promotions.")
    st.markdown("#### Filtered data preview")
    st.dataframe(data.head(100), use_container_width=True, hide_index=True)
    st.download_button("Download filtered data as CSV", data.to_csv(index=False).encode("utf-8"), "filtered_retail_sales.csv", "text/csv")

st.markdown("---")
st.caption("Decision caveat: this dashboard is descriptive, not causal. Validate recommendations with operational context before acting.")
