import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Executive Ecommerce Analytics & ML Dashboard",
    layout="wide"
)
# -------------------------------------------------
# Background Image (Ecommerce Theme)
# -------------------------------------------------
# -------------------------------------------------
# Ecommerce Background
# -------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: 
        linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
        url("https://png.pngtree.com/background/20230611/original/pngtree-ecommerce-development-at-a-glance-on-the-internet-with-all-of-picture-image_3171281.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Database connection
# -------------------------------------------------
@st.cache_resource
def get_engine():
    return create_engine(
        "mysql+pymysql://root:qXFFWJWhuTIPBdFPgLjHNFXDGUSTwbPC@gondola.proxy.rlwy.net:34879/railway",
        pool_pre_ping=True
    )

engine = get_engine()

# -------------------------------------------------
# Load sales data
# -------------------------------------------------
@st.cache_data
def load_sales():
    query = """
        SELECT order_id, product_name, category,
            city, region, customer_type, quantity, discount_pct,
            discount_amount, net_amount, order_date, order_hour
        FROM sales_events
    """
    engine = get_engine()
    df = pd.read_sql(query, engine)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

sales_df = load_sales()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.title("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "City",
    options=sorted(sales_df["city"].dropna().unique())
)

product_filter = st.sidebar.multiselect(
    "Product",
    options=sorted(sales_df["product_name"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    options=sorted(sales_df["category"].dropna().unique())
)

customer_filter = st.sidebar.multiselect(
    "Customer Type",
    options=sorted(sales_df["customer_type"].dropna().unique())
)

date_min = sales_df["order_date"].min().date()
date_max = sales_df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

discount_range = st.sidebar.slider(
    "Discount %",
    0, 100, (0, 100)
)

# -------------------------------------------------
# Apply filters
# -------------------------------------------------
st.sidebar.markdown("## ⚙️ Filter Controls")
st.sidebar.caption("Refine dashboard insights dynamically")
filtered_df = sales_df.copy()

if city_filter:
    filtered_df = filtered_df[filtered_df["city"].isin(city_filter)]

if product_filter:
    filtered_df = filtered_df[filtered_df["product_name"].isin(product_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

if customer_filter:
    filtered_df = filtered_df[filtered_df["customer_type"].isin(customer_filter)]

filtered_df = filtered_df[
    (filtered_df["order_date"].dt.date >= date_range[0]) &
    (filtered_df["order_date"].dt.date <= date_range[1]) &
    (filtered_df["discount_pct"].between(discount_range[0], discount_range[1]))
]

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🛒 Executive Ecommerce Analytics & ML Dashboard")

tabs = st.tabs([
    "📊 Overview",
    "🏙 City & Product",
    "⏰ Time Insights",
    "💸 Discount Intelligence",
    "👥 Customer Behavior"
])

# -------------------------------------------------
# TAB 1 — Executive Overview
# -------------------------------------------------
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Orders", f"{len(filtered_df):,}")
    col2.metric("💰 Total Revenue", f"₹{filtered_df['net_amount'].sum():,.0f}")
    col3.metric("🧾 Avg Order Value", f"₹{filtered_df['net_amount'].mean():,.0f}")
    col4.metric(
        "🏷 Discounted Orders %",
        f"{(filtered_df['discount_pct'] > 0).mean() * 100:.1f}%"
    )

    daily_revenue = (
        filtered_df
        .groupby("order_date", as_index=False)["net_amount"]
        .sum()
    )

    fig = px.line(
        daily_revenue,
        x="order_date",
        y="net_amount",
        title="Daily Revenue Trend"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# TAB 2 — City & Product Insights
# -------------------------------------------------
with tabs[1]:
    col1, col2 = st.columns(2)

    city_sales = (
        filtered_df
        .groupby("city", as_index=False)["net_amount"]
        .sum()
        .sort_values("net_amount", ascending=False)
    )

    fig_city = px.bar(
        city_sales,
        x="city",
        y="net_amount",
        title="Revenue by City"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    col1.plotly_chart(fig_city, use_container_width=True)

    product_sales = (
        filtered_df
        .groupby("product_name", as_index=False)["net_amount"]
        .sum()
        .sort_values("net_amount", ascending=False)
        .head(10)
    )

    fig_prod = px.bar(
        product_sales,
        x="net_amount",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Revenue"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    col2.plotly_chart(fig_prod, use_container_width=True)

# -------------------------------------------------
# TAB 3 — Time-based Insights
# -------------------------------------------------
with tabs[2]:
    col1, col2 = st.columns(2)

    hourly_sales = (
        filtered_df
        .groupby("order_hour", as_index=False)["net_amount"]
        .sum()
    )

    fig_hour = px.line(
        hourly_sales,
        x="order_hour",
        y="net_amount",
        title="Revenue by Hour"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    col1.plotly_chart(fig_hour, use_container_width=True)

    day_sales = (
        filtered_df
        .assign(day=filtered_df["order_date"].dt.day_name())
        .groupby("day", as_index=False)["net_amount"]
        .sum()
    )

    fig_day = px.bar(
        day_sales,
        x="day",
        y="net_amount",
        title="Revenue by Day of Week"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    col2.plotly_chart(fig_day, use_container_width=True)

# -------------------------------------------------
# TAB 4 — Discount Intelligence
# -------------------------------------------------
with tabs[3]:
    discount_products = (
        filtered_df
        .groupby("product_name", as_index=False)["discount_amount"]
        .sum()
        .sort_values("discount_amount", ascending=False)
        .head(10)
    )

    fig_disc = px.bar(
        discount_products,
        x="discount_amount",
        y="product_name",
        orientation="h",
        title="Top Discounted Products"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_disc, use_container_width=True)

# -------------------------------------------------
# TAB 5 — Customer Behavior
# -------------------------------------------------
with tabs[4]:
    cust_sales = (
        filtered_df
        .groupby("customer_type", as_index=False)["net_amount"]
        .sum()
    )

    fig_cust = px.pie(
        cust_sales,
        names="customer_type",
        values="net_amount",
        title="Revenue by Customer Type"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18)
    )
    st.plotly_chart(fig_cust, use_container_width=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption("© 2026 Executive Ecommerce Analytics Platform | Built with Streamlit & ML")












