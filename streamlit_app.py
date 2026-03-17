import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Nassau Candy Optimization", layout="wide")
API_BASE = "http://127.0.0.1:8000/optimization"

# --- SIDEBAR: User Capabilities ---
st.sidebar.header("🕹️ Control Panel")
product_id = st.sidebar.number_input("Product ID", min_value=1, value=1)
priority = st.sidebar.slider("Optimization Priority (Profit vs. Speed)", 0.0, 1.0, 0.5)

st.sidebar.markdown("""
**Priority Guide:**
- 0.0: Maximize Profit (Stay at current factory)
- 1.0: Maximize Speed (Closest factory)
""")

# --- MAIN DASHBOARD ---
st.title("🍭 Nassau Candy Decision Intelligence")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🚀 Optimization Simulator", "📊 Route Clustering", "⚠️ Risk & Impact"])

# --- TAB 1: Factory Optimization Simulator ---
with tab1:
    st.header("Scenario Simulation Engine")
    if st.button("Run Simulation Analysis"):
        # 1. Get Recommendation
        rec_res = requests.get(f"{API_BASE}/recommend/", params={"product_id": product_id, "priority": priority})
        # 2. Get All Factory Simulations
        sim_res = requests.get(f"{API_BASE}/simulate/{product_id}/")

        if rec_res.status_code == 200 and sim_res.status_code == 200:
            rec_data = rec_res.json()
            sim_data = sim_res.json()

            # KPI Cards
            c1, c2, c3 = st.columns(3)
            c1.metric("Recommended Site", rec_data['recommended_factory'])
            c2.metric("Confidence Score", rec_data['kpi_metrics']['scenario_confidence'])
            c3.metric("Profit Impact", rec_data['kpi_metrics']['profit_impact'])

            # Results Table
            st.subheader("Predicted Lead Times Across All Sites")
            df = pd.DataFrame(sim_data['simulations'])
            st.dataframe(df.style.highlight_max(axis=0, subset=['predicted_lead_time'], color='red'))
        else:
            st.error("Backend Error: Ensure Django server is running.")

# --- TAB 2: Route Clustering ---
with tab2:
    st.header("Performance Clustering Analysis")
    if st.button("Analyze Route Performance"):
        clust_res = requests.get(f"{API_BASE}/clusters/")
        if clust_res.status_code == 200:
            clusters = clust_res.json()['clusters']
            df_clust = pd.DataFrame(clusters)

            # Visualization
            fig = px.bar(df_clust, x='region', y='avg_lead_time', color='performance_label',
                         title="Lead Time by Region Cluster", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            st.table(df_clust)
        else:
            st.error("Could not fetch clustering data.")

# --- TAB 3: Risk & Impact Panel ---
with tab3:
    st.header("Executive Risk Panel")
    st.markdown("### High-Risk Reassignment Warnings")

    # Logic to show alerts based on priority
    if priority > 0.8:
        st.error(
            "🚨 **WARNING:** High Optimization Priority for Speed may erode margins by over 5% due to logistics costs.")
    elif priority < 0.2:
        st.info(
            "ℹ️ **INFO:** Profit-focused strategy is maintaining current legacy assignments. Shipping times may remain high.")
    else:
        st.success("✅ Balanced strategy: Optimization score is within safe financial bounds.")