import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Unemployment Analysis India", layout="wide")

st.title("📊 Unemployment Analysis in India")
st.markdown("Analyzing the trends, regional disparities, and the impact of COVID-19 on unemployment rates.")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Unemployment in India.csv")
        # Clean column names
        df.columns = df.columns.str.strip()
        # Clean Date
        df["Date"] = pd.to_datetime(df["Date"].str.strip(), format="%d-%m-%Y")
        # Drop nulls
        df.dropna(inplace=True)
        # Extract features
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month_name()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar Filters
    st.sidebar.header("Filter Data")
    
    # Year Filter
    years = df["Year"].unique()
    selected_years = st.sidebar.multiselect("Select Year", years, default=years)
    
    # Area Filter
    areas = df["Area"].unique()
    selected_area = st.sidebar.multiselect("Select Area (Rural/Urban)", areas, default=areas)
    
    # Region Filter
    regions = df["Region"].unique()
    selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)

    # Filter Logic
    filtered_df = df[
        (df["Year"].isin(selected_years)) &
        (df["Area"].isin(selected_area)) &
        (df["Region"].isin(selected_region))
    ]
    
    # KPI Section
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    avg_unemp = filtered_df["Estimated Unemployment Rate (%)"].mean()
    avg_emp = filtered_df["Estimated Employed"].mean()
    avg_labour = filtered_df["Estimated Labour Participation Rate (%)"].mean()
    
    col1.metric("Avg Unemployment Rate", f"{avg_unemp:.2f}%")
    col2.metric("Avg Employed Count", f"{avg_emp:,.0f}")
    col3.metric("Avg Labour Participation", f"{avg_labour:.2f}%")
    
    st.divider()

    # Visualizations
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Unemployment Rate Trend")
        if not filtered_df.empty:
            fig_trend = px.line(filtered_df, x="Date", y="Estimated Unemployment Rate (%)", color="Region", title="Unemployment Rate Over Time")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("No data to display based on filters.")
            
    with col_chart2:
        st.subheader("Region-wise Average Unemployment")
        if not filtered_df.empty:
            avg_by_region = filtered_df.groupby("Region")["Estimated Unemployment Rate (%)"].mean().reset_index().sort_values(by="Estimated Unemployment Rate (%)", ascending=False)
            fig_bar = px.bar(avg_by_region, x="Estimated Unemployment Rate (%)", y="Region", orientation="h", title="Average Unemployment by Region", color="Region")
            st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.subheader("Area Distribution")
        if not filtered_df.empty:
            fig_pie = px.pie(filtered_df, values="Estimated Unemployment Rate (%)", names="Area", title="Unemployment Share by Area")
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart4:
        st.subheader("Correlation Heatmap")
        if not filtered_df.empty:
            corr = filtered_df[["Estimated Unemployment Rate (%)", "Estimated Employed", "Estimated Labour Participation Rate (%)"]].corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Feature Correlation")
            st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()
    
    st.subheader("Detailed Data View")
    st.dataframe(filtered_df)
    
    st.markdown("""
    ### Key Insights
    - **COVID-19 Impact:** Look for spikes in 2020 to understand the pandemic effect.
    - **Regional Trends:** Identify which states suffer most from unemployment.
    - **Urban vs Rural:** Compare the resilience of different areas.
    """)
    
else:
    st.warning("Please ensure the dataset file is present.")
