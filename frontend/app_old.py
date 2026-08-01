import streamlit as st
import pandas as pd
import plotly.express as px
import requests

def load_css():
    with open("frontend/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="MetricMind",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/sales.csv", encoding="latin1")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
# ==========================
# PROFESSIONAL SIDEBAR
# ==========================

st.sidebar.title("🧠 MetricMind")

st.sidebar.success("🟢 Semantic Layer Active")

st.sidebar.markdown("---")

st.sidebar.subheader("📂 Navigation")

st.sidebar.button("🏠 Dashboard")
st.sidebar.button("🤖 AI Assistant")
st.sidebar.button("📊 Analytics")
st.sidebar.button("📥 Reports")

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Filters")

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]



# -----------------------------
# TITLE
# -----------------------------
st.title("🧠 MetricMind Enterprise")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🤖 AI Assistant",
    "📈 Analytics",
    "📋 Reports"
])
with tab1:
    st.caption("AI Powered Semantic BI Engine")

    st.success("🟢 Agent Online • Semantic Layer Active")

# -----------------------------
# KPI CARDS
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].count()
avg_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background:#1E293B;padding:20px;border-radius:15px;
    border-left:6px solid #22C55E;text-align:center;">
        <h4>💰 Revenue</h4>
        <h2>${total_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#1E293B;padding:20px;border-radius:15px;
    border-left:6px solid #3B82F6;text-align:center;">
        <h4>📈 Profit</h4>
        <h2>${total_profit:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#1E293B;padding:20px;border-radius:15px;
    border-left:6px solid #F59E0B;text-align:center;">
        <h4>📦 Orders</h4>
        <h2>{total_orders}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background:#1E293B;padding:20px;border-radius:15px;
    border-left:6px solid #8B5CF6;text-align:center;">
        <h4>🛒 Avg Sales</h4>
        <h2>${avg_sales:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------
# SALES BY REGION
# -----------------------------
left, right = st.columns(2)

with left:
    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Sales",
    color_continuous_scale="Blues",
    title="📊 Sales by Region"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Sales ($)",
    height=420
)

fig.update_traces(
    marker_line_width=0,
    hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# PROFIT BY CATEGORY
# -----------------------------
with right:
    category_profit = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

fig2 = px.pie(
    category_profit,
    names="Category",
    values="Profit",
    hole=0.55,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="💰 Profit by Category"
)

fig2.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=420
)

fig2.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
filtered_df["Order Date"] = pd.to_datetime(
    filtered_df["Order Date"]
)

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)


fig3 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="📈 Monthly Sales Trend"
)

fig3.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=450
)

fig3.update_traces(
    line_width=4
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# TOP 10 PRODUCTS
# -----------------------------
top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    color_continuous_scale="Viridis",
    title="🏆 Top 10 Products"
)

fig4.update_layout(
    template="plotly_white",
    title_x=0.5,
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_sales.csv",
    "text/csv"
)

st.divider()

# -----------------------------
# AI CHAT
# -----------------------------
# ==========================
# AI ASSISTANT
# ==========================

st.divider()

st.header("🤖 Conversational BI")

st.write("### Suggested Questions")

c1, c2, c3, c4 = st.columns(4)

if c1.button("💰 Total Revenue"):
    st.session_state.question = "What is the total revenue?"

if c2.button("📈 Total Profit"):
    st.session_state.question = "What is the total profit?"

if c3.button("📦 Total Orders"):
    st.session_state.question = "How many orders are there?"

if c4.button("🌍 Best Region"):
    st.session_state.question = "Which region has the highest sales?"

question = st.text_input(
    "Ask about revenue, profit, sales...",
    value=st.session_state.get("question", "")
)

if st.button("🚀 Send"):

    with st.spinner("MetricMind is thinking..."):

        response = requests.get(
            "http://127.0.0.1:8000/ask",
            params={"question": question}
        )

        if response.status_code == 200:

            st.chat_message("user").write(question)

            st.chat_message("assistant").write(
                response.json()["answer"]
            )

        else:
            st.error("API Error")
        st.divider()

st.header("📌 Business Insights")

highest_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

highest_category = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
    .idxmax()
)

st.info(f"🏆 Highest Sales Region: {highest_region}")
st.info(f"💰 Most Profitable Category: {highest_category}")
st.info(f"📦 Total Orders: {total_orders}")
st.info(f"💵 Average Sales: ${avg_sales:.2f}")

st.divider()

st.header("📋 Dashboard Summary")

st.markdown(f"""
### 📊 Current Analysis

- **Total Revenue:** ${total_sales:,.2f}
- **Total Profit:** ${total_profit:,.2f}
- **Total Orders:** {total_orders}
- **Average Sales:** ${avg_sales:.2f}

### 🎯 Key Findings

✅ Best Performing Region: **{highest_region}**

✅ Most Profitable Category: **{highest_category}**

✅ Current Region Filter: **{region}**

✅ Current Category Filter: **{category}**

---
Generated automatically by **MetricMind Enterprise**
""")