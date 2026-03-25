import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Literacy Dashboard", layout="wide")

# Load data
df = pd.read_csv("../data/final_dataset.csv")

# Title
st.title("📊 Global Literacy & Education Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filters")
country = st.sidebar.selectbox("Select Country", sorted(df["country"].unique()))
year = st.sidebar.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

# Filter data
filtered = df[(df["country"] == country) & (df["year"] <= year)]

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

latest = filtered.sort_values("year").iloc[-1]

col1.metric("📖 Literacy Rate", f"{latest['adult_literacy']:.2f}")
col2.metric("💰 GDP per Capita", f"{latest['gdp_per_capita']:.2f}")
col3.metric("🎓 Avg Schooling", f"{latest['avg_years_schooling']:.2f}")

# ---------------- CHARTS ----------------

colA, colB = st.columns(2)

# Literacy Trend
with colA:
    st.subheader("📈 Literacy Trend")
    st.line_chart(filtered.set_index("year")["adult_literacy"])

# GDP vs Literacy
with colB:
    st.subheader("📊 GDP vs Literacy")
    st.scatter_chart(filtered[["gdp_per_capita", "adult_literacy"]])

# ---------------- EXTRA VISUALS ----------------

colC, colD = st.columns(2)

# Gender Gap
with colC:
    st.subheader("⚖️ Gender Gap")
    if "literacy_gender_gap" in df.columns:
        st.bar_chart(filtered.set_index("year")["literacy_gender_gap"])

# Youth Literacy
with colD:
    st.subheader("👦 Youth Literacy Avg")
    if "youth_literacy_avg" in df.columns:
        st.line_chart(filtered.set_index("year")["youth_literacy_avg"])

# ---------------- CORRELATION ----------------

st.subheader("🔗 Correlation Matrix")
st.dataframe(df.corr(numeric_only=True))

# ---------------- INSIGHTS ----------------

st.subheader("💡 Key Insights")

st.write("""
📌 Higher literacy is strongly linked with higher GDP per capita.  

📌 Countries with more schooling years show better literacy outcomes.  

📌 Gender gap still exists in some developing regions.  

📌 Youth literacy is improving faster than adult literacy → positive trend.  

📌 Education investment directly impacts economic growth.  
""")

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("📊 Project by Winston Raj | Education Analytics")