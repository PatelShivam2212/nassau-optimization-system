# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# # Configuration
# st.set_page_config(page_title="Nassau Candy Optimization", layout="wide")
# API_BASE = "http://127.0.0.1:8000/optimization"
#
# # --- SIDEBAR: User Capabilities ---
# st.sidebar.header("🕹️ Control Panel")
# product_id = st.sidebar.number_input("Product ID", min_value=1, value=1)
# priority = st.sidebar.slider("Optimization Priority (Profit vs. Speed)", 0.0, 1.0, 0.5)
#
# st.sidebar.markdown("""
# **Priority Guide:**
# - 0.0: Maximize Profit (Stay at current factory)
# - 1.0: Maximize Speed (Closest factory)
# """)
#
# # --- MAIN DASHBOARD ---
# st.title("🍭 Nassau Candy Decision Intelligence")
# st.markdown("---")
#
# tab1, tab2, tab3 = st.tabs(["🚀 Optimization Simulator", "📊 Route Clustering", "⚠️ Risk & Impact"])
#
# # --- TAB 1: Factory Optimization Simulator ---
# with tab1:
#     st.header("Scenario Simulation Engine")
#     if st.button("Run Simulation Analysis"):
#         rec_res = requests.get(f"{API_BASE}/recommend/", params={"product_id": product_id, "priority": priority})
#         sim_res = requests.get(f"{API_BASE}/simulate/{product_id}/")
#
#         if rec_res.status_code == 200 and sim_res.status_code == 200:
#             rec_data = rec_res.json()
#             sim_data = sim_res.json()
#
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Recommended Site", rec_data['recommended_factory'])
#             c2.metric("Confidence Score", rec_data['kpi_metrics']['scenario_confidence'])
#             c3.metric("Profit Impact", rec_data['kpi_metrics']['profit_impact'])
#
#             st.subheader("Predicted Lead Times Across All Sites")
#             df = pd.DataFrame(sim_data['simulations'])
#             st.dataframe(df.style.highlight_max(axis=0, subset=['predicted_lead_time'], color='red'))
#         else:
#             st.error("Backend Error: Ensure Django server is running.")
#
# # --- TAB 2: Route Clustering ---
# with tab2:
#     st.header("Performance Clustering Analysis")
#     if st.button("Analyze Route Performance"):
#         clust_res = requests.get(f"{API_BASE}/clusters/")
#         if clust_res.status_code == 200:
#             clusters = clust_res.json()['clusters']
#             df_clust = pd.DataFrame(clusters)
#             fig = px.bar(df_clust, x='region', y='avg_lead_time', color='performance_label',
#                          title="Lead Time by Region Cluster", barmode='group')
#             st.plotly_chart(fig, use_container_width=True)
#             st.table(df_clust)
#         else:
#             st.error("Could not fetch clustering data.")
#
# # --- TAB 3: Risk & Impact Panel ---
# with tab3:
#     st.header("Executive Risk Panel")
#     st.markdown("### High-Risk Reassignment Warnings")
#     if priority > 0.8:
#         st.error("🚨 **WARNING:** High Optimization Priority for Speed may erode margins by over 5% due to logistics costs.")
#     elif priority < 0.2:
#         st.info("ℹ️ **INFO:** Profit-focused strategy is maintaining current legacy assignments.")
#     else:
#         st.success("✅ Balanced strategy: Optimization score is within safe financial bounds.")
#
# # --- NEW SECTION: Master Data Reference (Requirement Compliance) ---
# st.markdown("---")
# st.header("📋 Technical Reference & Master Data")
#
# col_ref1, col_ref2 = st.columns(2)
#
# with col_ref1:
#     with st.expander("📍 Factory Coordinates (Geospatial Master)"):
#         factory_data = [
#             {"Factory": "Lot's O' Nuts", "Latitude": 32.881893, "Longitude": -111.768036},
#             {"Factory": "Wicked Choccy's", "Latitude": 32.076176, "Longitude": -81.088371},
#             {"Factory": "Sugar Shack", "Latitude": 48.119140, "Longitude": -96.181150},
#             {"Factory": "Secret Factory", "Latitude": 41.446333, "Longitude": -90.565487},
#             {"Factory": "The Other Factory", "Latitude": 35.117500, "Longitude": -89.971107}
#         ]
#         st.table(pd.DataFrame(factory_data))
#
# with col_ref2:
#     with st.expander("🔗 Product-to-Factory Correlation (Legacy Rules)"):
#         correlation_data = [
#             {"Division": "Chocolate", "Product": "Wonka Bar - Nutty Crunch", "Factory": "Lot's O' Nuts"},
#             {"Division": "Chocolate", "Product": "Wonka Bar - Milk Chocolate", "Factory": "Wicked Choccy's"},
#             {"Division": "Sugar", "Product": "Laffy Taffy", "Factory": "Sugar Shack"},
#             {"Division": "Sugar", "Product": "Everlasting Gobstopper", "Factory": "Secret Factory"},
#             {"Division": "Other", "Product": "Kazookles", "Factory": "The Other Factory"}
#         ]
#         st.table(pd.DataFrame(correlation_data))

# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# # Configuration
# st.set_page_config(page_title="Nassau Candy Optimization", layout="wide")
# API_BASE = "http://127.0.0.1:8000/optimization"
#
# # --- SIDEBAR: User Capabilities ---
# st.sidebar.header("🕹️ Control Panel")
# product_id = st.sidebar.number_input("Product ID", min_value=1, value=1)
# priority = st.sidebar.slider("Optimization Priority (Profit vs. Speed)", 0.0, 1.0, 0.5)
#
# st.sidebar.markdown("""
# **Priority Guide:**
# - 0.0: Maximize Profit (Stay at current factory)
# - 1.0: Maximize Speed (Closest factory)
# """)
#
# # --- MAIN DASHBOARD ---
# st.title("🍭 Nassau Candy Decision Intelligence")
# st.markdown("---")
#
# tab1, tab2, tab3 = st.tabs(["🚀 Optimization Simulator", "📊 Route Clustering", "⚠️ Risk & Impact"])
#
# # --- TAB 1: Factory Optimization Simulator ---
# with tab1:
#     st.header("Scenario Simulation Engine")
#     if st.button("Run Simulation Analysis"):
#         # 1. Get Recommendation
#         rec_res = requests.get(f"{API_BASE}/recommend/", params={"product_id": product_id, "priority": priority})
#         # 2. Get All Factory Simulations
#         sim_res = requests.get(f"{API_BASE}/simulate/{product_id}/")
#
#         if rec_res.status_code == 200 and sim_res.status_code == 200:
#             rec_data = rec_res.json()
#             sim_data = sim_res.json()
#
#             # KPI Cards
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Recommended Site", rec_data['recommended_factory'])
#             c2.metric("Confidence Score", rec_data['kpi_metrics']['scenario_confidence'])
#             c3.metric("Profit Impact", rec_data['kpi_metrics']['profit_impact'])
#
#             # Results Table
#             st.subheader("Predicted Lead Times Across All Sites")
#             df = pd.DataFrame(sim_data['simulations'])
#             st.dataframe(df.style.highlight_max(axis=0, subset=['predicted_lead_time'], color='red'))
#         else:
#             st.error("Backend Error: Ensure Django server is running and Product ID exists.")
#
# # --- TAB 2: Route Clustering ---
# with tab2:
#     st.header("Performance Clustering Analysis")
#     if st.button("Analyze Route Performance"):
#         clust_res = requests.get(f"{API_BASE}/clusters/")
#         if clust_res.status_code == 200:
#             clusters = clust_res.json()['clusters']
#             df_clust = pd.DataFrame(clusters)
#
#             # Visualization
#             fig = px.bar(df_clust, x='region', y='avg_lead_time', color='performance_label',
#                          title="Lead Time by Region Cluster", barmode='group')
#             st.plotly_chart(fig, use_container_width=True)
#
#             st.table(df_clust)
#         else:
#             st.error("Could not fetch clustering data.")
#
# # --- TAB 3: Risk & Impact Panel ---
# with tab3:
#     st.header("Executive Risk Panel")
#     st.markdown("### High-Risk Reassignment Warnings")
#
#     # Logic to show alerts based on priority
#     if priority > 0.8:
#         st.error(
#             "🚨 **WARNING:** High Optimization Priority for Speed may erode margins by over 5% due to logistics costs.")
#     elif priority < 0.2:
#         st.info(
#             "ℹ️ **INFO:** Profit-focused strategy is maintaining current legacy assignments. Shipping times may remain high.")
#     else:
#         st.success("✅ Balanced strategy: Optimization score is within safe financial bounds.")
#
# # --- NEW SECTION: Master Data Reference (Dynamic Requirements Compliance) ---
# st.markdown("---")
# st.header("📋 Technical Reference & Master Data")
#
# col_ref1, col_ref2 = st.columns(2)
#
# with col_ref1:
#     with st.expander("📍 Factory Coordinates (Live Geospatial Master)"):
#         try:
#             f_res = requests.get(f"{API_BASE}/factories/")
#             if f_res.status_code == 200:
#                 st.table(pd.DataFrame(f_res.json()))
#             else:
#                 st.warning("Factory endpoint not found on server.")
#         except Exception as e:
#             st.error("Failed to connect to Factory Master Data.")
#
# with col_ref2:
#     with st.expander("🔗 Product-to-Factory Correlation (Live Database)"):
#         try:
#             c_res = requests.get(f"{API_BASE}/correlations/")
#             if c_res.status_code == 200:
#                 st.table(pd.DataFrame(c_res.json()))
#             else:
#                 st.warning("Correlation endpoint not found on server.")
#         except Exception as e:
#             st.error("Failed to connect to Correlation Data.")






# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
#
# # Configuration
# st.set_page_config(page_title="Nassau Candy Optimization", layout="wide")
# API_BASE = "http://127.0.0.1:8000/optimization"
#
# # Helper function to safely fetch data from API
# def safe_fetch(endpoint, params=None, default=None):
#     try:
#         resp = requests.get(f"{API_BASE}/{endpoint}/", params=params, timeout=5)
#         if resp.status_code == 200:
#             return resp.json()
#         else:
#             return default
#     except Exception as e:
#         st.warning(f"Could not connect to backend: {e}")
#         return default
#
# # --- SIDEBAR: User Capabilities ---
# st.sidebar.header("🕹️ Control Panel")
# product_id = st.sidebar.number_input("Product ID", min_value=1, value=1)
# priority = st.sidebar.slider("Optimization Priority (Profit vs. Speed)", 0.0, 1.0, 0.5)
#
# st.sidebar.markdown("""
# **Priority Guide:**
# - 0.0: Maximize Profit (Stay at current factory)
# - 1.0: Maximize Speed (Closest factory)
# """)
#
# # Fetch filter options safely
# regions = safe_fetch("regions", default=[])
# ship_modes = safe_fetch("ship_modes", default=[])
#
# selected_region = st.sidebar.selectbox("Region", regions if regions else ["Interior"])
# selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_modes if ship_modes else ["Standard Class"])
#
# # Coverage KPI – safe fetch
# coverage_data = safe_fetch("coverage")
# coverage = coverage_data['coverage'] if coverage_data else 0
# st.sidebar.metric("Recommendation Coverage", f"{coverage}%")
#
# # --- MAIN DASHBOARD ---
# st.title("🍭 Nassau Candy Decision Intelligence")
# st.markdown("---")
#
# tab1, tab2, tab3 = st.tabs(["🚀 Optimization Simulator", "📊 Route Clustering", "⚠️ Risk & Impact"])
#
# # --- TAB 1: Factory Optimization Simulator ---
# with tab1:
#     st.header("Scenario Simulation Engine")
#     if st.button("Run Simulation Analysis"):
#         rec_data = safe_fetch("recommend", params={"product_id": product_id, "priority": priority})
#         sim_data = safe_fetch(f"simulate/{product_id}", params={"region": selected_region, "ship_mode": selected_ship_mode})
#
#         if rec_data and sim_data:
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Recommended Site", rec_data.get('recommended_factory', 'N/A'))
#             c2.metric("Confidence Score", rec_data.get('kpi_metrics', {}).get('scenario_confidence', 'N/A'))
#             c3.metric("Profit Impact", rec_data.get('kpi_metrics', {}).get('profit_impact', 'N/A'))
#
#             st.subheader("Predicted Lead Times Across All Sites")
#             df = pd.DataFrame(sim_data.get('simulations', []))
#             if not df.empty:
#                 st.dataframe(df.style.highlight_max(axis=0, subset=['predicted_lead_time'], color='red'))
#             else:
#                 st.info("No simulation data available.")
#
#             if 'ranked_recommendations' in rec_data:
#                 st.subheader("Top Factory Recommendations")
#                 rec_df = pd.DataFrame(rec_data['ranked_recommendations'])
#                 st.dataframe(rec_df)
#         else:
#             st.error("Failed to fetch data. Make sure the Django backend is running (python manage.py runserver).")
#
# # --- TAB 2: Route Clustering ---
# with tab2:
#     st.header("Performance Clustering Analysis")
#     if st.button("Analyze Route Performance"):
#         clusters_data = safe_fetch("clusters")
#         if clusters_data and 'clusters' in clusters_data:
#             df_clust = pd.DataFrame(clusters_data['clusters'])
#             if not df_clust.empty:
#                 fig = px.bar(df_clust, x='region', y='avg_lead_time', color='performance_label',
#                              title="Lead Time by Region Cluster", barmode='group')
#                 st.plotly_chart(fig, use_container_width=True)
#                 st.table(df_clust)
#             else:
#                 st.info("No clustering data available.")
#         else:
#             st.error("Could not fetch clustering data. Ensure backend is running.")
#
# # --- TAB 3: Risk & Impact Panel ---
# with tab3:
#     st.header("Executive Risk Panel")
#     st.markdown("### High-Risk Reassignment Warnings")
#     if priority > 0.8:
#         st.error("🚨 **WARNING:** High Optimization Priority for Speed may erode margins by over 5% due to logistics costs.")
#     elif priority < 0.2:
#         st.info("ℹ️ **INFO:** Profit-focused strategy is maintaining current legacy assignments. Shipping times may remain high.")
#     else:
#         st.success("✅ Balanced strategy: Optimization score is within safe financial bounds.")
#
# # --- Master Data Reference (Dynamic) ---
# st.markdown("---")
# st.header("📋 Technical Reference & Master Data")
#
# col_ref1, col_ref2 = st.columns(2)
#
# with col_ref1:
#     with st.expander("📍 Factory Coordinates (Live Geospatial Master)"):
#         factories = safe_fetch("factories")
#         if factories:
#             st.table(pd.DataFrame(factories))
#         else:
#             st.warning("Could not fetch factory data. Backend may be unavailable.")
#
# with col_ref2:
#     with st.expander("🔗 Product-to-Factory Correlation (Live Database)"):
#         correlations = safe_fetch("correlations")
#         if correlations:
#             st.table(pd.DataFrame(correlations))
#         else:
#             st.warning("Could not fetch correlation data. Backend may be unavailable.")



import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration
st.set_page_config(page_title="Nassau Candy Optimization", layout="wide")
API_BASE = "http://127.0.0.1:8000/optimization"

# Helper function to safely fetch data from API
def safe_fetch(endpoint, params=None, default=None):
    try:
        resp = requests.get(f"{API_BASE}/{endpoint}/", params=params, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            return default
    except Exception as e:
        st.warning(f"Could not connect to backend: {e}")
        return default

# --- SIDEBAR: User Capabilities ---
st.sidebar.header("🕹️ Control Panel")
product_id = st.sidebar.number_input("Product ID", min_value=1, value=1)
priority = st.sidebar.slider("Optimization Priority (Profit vs. Speed)", 0.0, 1.0, 0.5)

st.sidebar.markdown("""
**Priority Guide:**
- 0.0: Maximize Profit (Stay at current factory)
- 1.0: Maximize Speed (Closest factory)
""")

# Fetch filter options safely
regions = safe_fetch("regions", default=[])
ship_modes = safe_fetch("ship_modes", default=[])

selected_region = st.sidebar.selectbox("Region", regions if regions else ["Interior"])
selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_modes if ship_modes else ["Standard Class"])

# Coverage KPI – safe fetch
coverage_data = safe_fetch("coverage")
coverage = coverage_data['coverage'] if coverage_data else 0
st.sidebar.metric("Recommendation Coverage", f"{coverage}%")

# --- MAIN DASHBOARD ---
st.title("🍭 Nassau Candy Decision Intelligence")
st.markdown("---")

# Add new tab for Geospatial Map
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Optimization Simulator", "📊 Route Clustering", "⚠️ Risk & Impact", "🗺️ Geospatial Map"])

# --- TAB 1: Factory Optimization Simulator ---
with tab1:
    st.header("Scenario Simulation Engine")
    if st.button("Run Simulation Analysis"):
        rec_data = safe_fetch("recommend", params={"product_id": product_id, "priority": priority})
        sim_data = safe_fetch(f"simulate/{product_id}", params={"region": selected_region, "ship_mode": selected_ship_mode})

        if rec_data and sim_data:
            # Store results in session state for later use (export, map)
            st.session_state['rec_data'] = rec_data
            st.session_state['sim_data'] = sim_data
            st.session_state['current_product_id'] = product_id

            c1, c2, c3 = st.columns(3)
            c1.metric("Recommended Site", rec_data.get('recommended_factory', 'N/A'))
            c2.metric("Confidence Score", rec_data.get('kpi_metrics', {}).get('scenario_confidence', 'N/A'))
            c3.metric("Profit Impact", rec_data.get('kpi_metrics', {}).get('profit_impact', 'N/A'))

            st.subheader("Predicted Lead Times Across All Sites")
            df = pd.DataFrame(sim_data.get('simulations', []))
            if not df.empty:
                st.dataframe(df.style.highlight_max(axis=0, subset=['predicted_lead_time'], color='red'))

                # --- CSV Export Button ---
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Simulation Results as CSV",
                    data=csv,
                    file_name=f"simulation_product_{product_id}.csv",
                    mime="text/csv",
                )
            else:
                st.info("No simulation data available.")

            if 'ranked_recommendations' in rec_data:
                st.subheader("Top Factory Recommendations")
                rec_df = pd.DataFrame(rec_data['ranked_recommendations'])
                st.dataframe(rec_df)
        else:
            st.error("Failed to fetch data. Make sure the Django backend is running (python manage.py runserver).")

# --- TAB 2: Route Clustering ---
with tab2:
    st.header("Performance Clustering Analysis")
    if st.button("Analyze Route Performance"):
        clusters_data = safe_fetch("clusters")
        if clusters_data and 'clusters' in clusters_data:
            df_clust = pd.DataFrame(clusters_data['clusters'])
            if not df_clust.empty:
                fig = px.bar(df_clust, x='region', y='avg_lead_time', color='performance_label',
                             title="Lead Time by Region Cluster", barmode='group')
                st.plotly_chart(fig, use_container_width=True)
                st.table(df_clust)
            else:
                st.info("No clustering data available.")
        else:
            st.error("Could not fetch clustering data. Ensure backend is running.")

# --- TAB 3: Risk & Impact Panel ---
with tab3:
    st.header("Executive Risk Panel")
    st.markdown("### High-Risk Reassignment Warnings")
    if priority > 0.8:
        st.error("🚨 **WARNING:** High Optimization Priority for Speed may erode margins by over 5% due to logistics costs.")
    elif priority < 0.2:
        st.info("ℹ️ **INFO:** Profit-focused strategy is maintaining current legacy assignments. Shipping times may remain high.")
    else:
        st.success("✅ Balanced strategy: Optimization score is within safe financial bounds.")

# --- TAB 4: Geospatial Map ---
with tab4:
    st.header("📍 Factory Locations & Recommendations")

    # Fetch all factories for mapping
    factories = safe_fetch("factories")
    if factories:
        df_factories = pd.DataFrame(factories)
        df_factories.rename(columns={'name': 'Factory', 'latitude': 'lat', 'longitude': 'lon'}, inplace=True)

        # Base map
        fig = px.scatter_mapbox(
            df_factories,
            lat='lat',
            lon='lon',
            hover_name='Factory',
            zoom=3,
            height=500,
            title="Factory Locations",
            color_discrete_sequence=['blue']
        )

        # If we have simulation results in session state, highlight the current and recommended factories
        if 'rec_data' in st.session_state and st.session_state['rec_data']:
            rec_data = st.session_state['rec_data']
            current_factory = rec_data.get('current_factory')
            recommended_factory = rec_data.get('recommended_factory')

            # Add markers for current and recommended factories
            current_factory_info = df_factories[df_factories['Factory'] == current_factory]
            if not current_factory_info.empty:
                fig.add_trace(px.scatter_mapbox(
                    current_factory_info,
                    lat='lat', lon='lon',
                    text='Factory',
                    hover_name='Factory',
                    color_discrete_sequence=['red']
                ).data[0])
                # Add a legend manually (optional)
                fig.update_traces(marker=dict(size=12, symbol='circle'), selector=dict(marker_color='red'))
                fig.update_layout(legend_title_text="Factory Type")
                fig.add_annotation(
                    x=current_factory_info['lon'].iloc[0],
                    y=current_factory_info['lat'].iloc[0],
                    text="Current Factory",
                    showarrow=True,
                    arrowhead=1
                )

            recommended_factory_info = df_factories[df_factories['Factory'] == recommended_factory]
            if not recommended_factory_info.empty:
                fig.add_trace(px.scatter_mapbox(
                    recommended_factory_info,
                    lat='lat', lon='lon',
                    text='Factory',
                    hover_name='Factory',
                    color_discrete_sequence=['green']
                ).data[0])
                fig.update_traces(marker=dict(size=12, symbol='star'), selector=dict(marker_color='green'))
                fig.add_annotation(
                    x=recommended_factory_info['lon'].iloc[0],
                    y=recommended_factory_info['lat'].iloc[0],
                    text="Recommended Factory",
                    showarrow=True,
                    arrowhead=1
                )

        # Update map style
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

        # Additional note
        st.info("Note: The map shows the location of all factories. After running a simulation, the current and recommended factories are highlighted.")
    else:
        st.warning("Could not fetch factory data. Backend may be unavailable.")

# --- Master Data Reference (Dynamic) ---
st.markdown("---")
st.header("📋 Technical Reference & Master Data")

col_ref1, col_ref2 = st.columns(2)

with col_ref1:
    with st.expander("📍 Factory Coordinates (Live Geospatial Master)"):
        factories = safe_fetch("factories")
        if factories:
            st.table(pd.DataFrame(factories))
        else:
            st.warning("Could not fetch factory data. Backend may be unavailable.")

with col_ref2:
    with st.expander("🔗 Product-to-Factory Correlation (Live Database)"):
        correlations = safe_fetch("correlations")
        if correlations:
            st.table(pd.DataFrame(correlations))
        else:
            st.warning("Could not fetch correlation data. Backend may be unavailable.")