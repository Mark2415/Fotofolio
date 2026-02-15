import pandas as pd
import streamlit as st
import plotly.express as px

# page config
st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    layout="wide"
)

# load data
@st.cache_data
def load_data():
    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country"
    ]

    df = pd.read_csv(
        "data.csv",
        header=None,
        names=columns,
        encoding="ISO-8859-1"
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df["sales"] = df["Quantity"] * df["UnitPrice"]
    return df

df = load_data()

# sidebar
st.sidebar.header("Data Filter")

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

country_list = ["ALL"] + sorted(df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox(
    "Select Country",
    country_list
)

# apply filters
filtered_df = df[
    (df["InvoiceDate"].dt.date >= date_range[0]) &
    (df["InvoiceDate"].dt.date <= date_range[1])
]

if selected_country != "ALL":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

# KPIs
total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"£ {total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)
col4.metric("Average Order Value", f"£ {avg_order_value:,.2f}")

st.divider()

# sales per month
monthly_sales = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("M")["sales"]
    .sum()
    .reset_index()
)

fig_monthly_sales = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="sales",
    title="Monthly Sales"
)

st.plotly_chart(fig_monthly_sales, use_container_width=True)

# top products
top_n = st.sidebar.number_input(
    "Number of Top Products",
    min_value=1,
    value=10,
    step=1
)

top_products = (
    filtered_df
    .groupby("Description")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="sales",
    y="Description",
    orientation="h",
    title=f"Top {top_n} Products by Sales"
)

st.plotly_chart(fig_products, use_container_width=True)

# sales by country
top_c = st.sidebar.number_input(
    "Number of Top Countries",
    min_value=1,
    value=10,
    step=1
)

country_sales = (
    filtered_df
    .groupby("Country")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(top_c)
    .reset_index()
)

fig_country_sales = px.bar(
    country_sales,
    x="sales",
    y="Country",
    orientation="h",
    title=f"Top {top_c} Countries by Sales"
)

st.plotly_chart(fig_country_sales, use_container_width=True)

# detail table
st.subheader("Transaction Details")

st.dataframe(
    filtered_df[
        [
            "InvoiceNo",
            "InvoiceDate",
            "Description",
            "Quantity",
            "UnitPrice",
            "sales",
            "Country"
        ]
    ]
    .sort_values(by="InvoiceDate", ascending=False),
    use_container_width=True
)