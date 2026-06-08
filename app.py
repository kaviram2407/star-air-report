import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page configuration
# Set page configuration
st.set_page_config(
    page_title="Star Air BI Portal",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render Sidebar Title & Logo
st.sidebar.markdown(
    "<div style='text-align: center; padding: 10px 0;'>"
    "<h2 style='color: #00b0ff; margin-bottom: 0;'>STAR AIR</h2>"
    "<p style='font-size: 13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;'>Business Intelligence</p>"
    "</div>", 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Theme selector
theme_mode = st.sidebar.selectbox(
    "🌓 Theme Mode",
    ["System Default", "Dark", "Light"],
    index=0
)

st.sidebar.markdown("---")

# Generate CSS Variables based on Theme Mode selection
theme_css = ""
if theme_mode == "Dark":
    theme_css = """
    :root {
        --bg-color: #0e1117;
        --text-color: #ffffff;
        --sidebar-bg: #080c11;
        --sidebar-text: rgba(255, 255, 255, 0.7);
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.08);
        --metric-header-color: rgba(255, 255, 255, 0.5);
        --metric-value-gradient-start: #ffffff;
        --border-color: rgba(255, 255, 255, 0.05);
        --label-bg: rgba(255, 255, 255, 0.02);
        --label-checked-bg: linear-gradient(135deg, rgba(0, 176, 255, 0.12) 0%, rgba(42, 157, 143, 0.12) 100%);
        --label-checked-border: rgba(0, 176, 255, 0.4);
        --label-hover-bg: rgba(255, 255, 255, 0.06);
        --grid-color: rgba(255, 255, 255, 0.05);
        --info-box-bg: rgba(0, 176, 255, 0.05);
        --text-muted: rgba(255, 255, 255, 0.4);
    }
    """
elif theme_mode == "Light":
    theme_css = """
    :root {
        --bg-color: #ffffff;
        --text-color: #1a1a1a;
        --sidebar-bg: #f8f9fa;
        --sidebar-text: rgba(0, 0, 0, 0.7);
        --card-bg: rgba(0, 0, 0, 0.02);
        --card-border: rgba(0, 0, 0, 0.08);
        --metric-header-color: rgba(0, 0, 0, 0.55);
        --metric-value-gradient-start: #1a1a1a;
        --border-color: rgba(0, 0, 0, 0.08);
        --label-bg: rgba(0, 0, 0, 0.015);
        --label-checked-bg: linear-gradient(135deg, rgba(0, 176, 255, 0.08) 0%, rgba(42, 157, 143, 0.08) 100%);
        --label-checked-border: rgba(0, 176, 255, 0.5);
        --label-hover-bg: rgba(0, 0, 0, 0.04);
        --grid-color: rgba(0, 0, 0, 0.08);
        --info-box-bg: rgba(0, 176, 255, 0.03);
        --text-muted: rgba(0, 0, 0, 0.5);
    }
    """
else:  # System Default
    theme_css = """
    :root {
        --bg-color: #0e1117;
        --text-color: #ffffff;
        --sidebar-bg: #080c11;
        --sidebar-text: rgba(255, 255, 255, 0.7);
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.08);
        --metric-header-color: rgba(255, 255, 255, 0.5);
        --metric-value-gradient-start: #ffffff;
        --border-color: rgba(255, 255, 255, 0.05);
        --label-bg: rgba(255, 255, 255, 0.02);
        --label-checked-bg: linear-gradient(135deg, rgba(0, 176, 255, 0.12) 0%, rgba(42, 157, 143, 0.12) 100%);
        --label-checked-border: rgba(0, 176, 255, 0.4);
        --label-hover-bg: rgba(255, 255, 255, 0.06);
        --grid-color: rgba(255, 255, 255, 0.05);
        --info-box-bg: rgba(0, 176, 255, 0.05);
        --text-muted: rgba(255, 255, 255, 0.4);
    }
    @media (prefers-color-scheme: light) {
        :root {
            --bg-color: #ffffff;
            --text-color: #1a1a1a;
            --sidebar-bg: #f8f9fa;
            --sidebar-text: rgba(0, 0, 0, 0.7);
            --card-bg: rgba(0, 0, 0, 0.02);
            --card-border: rgba(0, 0, 0, 0.08);
            --metric-header-color: rgba(0, 0, 0, 0.55);
            --metric-value-gradient-start: #1a1a1a;
            --border-color: rgba(0, 0, 0, 0.08);
            --label-bg: rgba(0, 0, 0, 0.015);
            --label-checked-bg: linear-gradient(135deg, rgba(0, 176, 255, 0.08) 0%, rgba(42, 157, 143, 0.08) 100%);
            --label-checked-border: rgba(0, 176, 255, 0.5);
            --label-hover-bg: rgba(0, 0, 0, 0.04);
            --grid-color: rgba(0, 0, 0, 0.08);
            --info-box-bg: rgba(0, 176, 255, 0.03);
            --text-muted: rgba(0, 0, 0, 0.5);
        }
    }
    """

# Custom CSS for Premium Design & Sidebar Animations with Variables
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

{theme_css}

/* Main font styling */
html, body, [data-testid="stSidebar"], .stMarkdown, p, div, label {{
    font-family: 'Outfit', sans-serif !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}}

/* Force background and text colors */
.stApp, html, body {{
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
}}

/* Glassmorphism card utility with smooth transitions & hover glow */
.card-container {{
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    color: var(--text-color) !important;
}}

.card-container:hover {{
    transform: translateY(-5px) !important;
    border-color: rgba(0, 176, 255, 0.3) !important;
    box-shadow: 0 12px 40px rgba(0, 176, 255, 0.15) !important;
}}

/* Metric styling inside cards */
.metric-header {{
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--metric-header-color) !important;
    margin-bottom: 8px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}

.metric-value {{
    font-size: 34px !important;
    font-weight: 750 !important;
    margin-bottom: 4px !important;
    letter-spacing: -0.01em !important;
    background: linear-gradient(135deg, var(--metric-value-gradient-start) 0%, #00b0ff 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}}

.metric-delta {{
    font-size: 13px !important;
    font-weight: 500;
}}

.delta-up {{
    color: #00e676 !important;
}}

.delta-down {{
    color: #ff1744 !important;
}}

/* Sidebar Styling & Custom Layout */
[data-testid="stSidebar"] {{
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border-color) !important;
}}

/* Ensure all labels and form/selectbox texts inside sidebar are highly visible */
[data-testid="stSidebar"] label, [data-testid="stSidebar"] label * {{
    color: var(--sidebar-text) !important;
}}

/* Beautiful navigation tabs styling */
[data-testid="stSidebar"] div[role="radiogroup"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    padding-top: 10px !important;
}}

[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background: var(--label-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    color: var(--sidebar-text) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    margin: 0 !important;
    width: 100% !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
}}

/* Force all radio list option texts to inherit selected color variables */
[data-testid="stSidebar"] div[role="radiogroup"] label * {{
    color: inherit !important;
}}

/* Hide native streamlit checkmark elements */
[data-testid="stSidebar"] div[role="radiogroup"] label div[role="presentation"],
[data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stFiberManualRecord"] {{
    display: none !important;
}}

/* Selection state */
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background: var(--label-checked-bg) !important;
    border: 1px solid var(--label-checked-border) !important;
    border-left: 5px solid #00b0ff !important;
    color: var(--text-color) !important;
    font-weight: 600 !important;
    box-shadow: 0 8px 24px rgba(0, 176, 255, 0.15) !important;
    transform: scale(1.03) translateX(8px) !important;
}}

/* Hover state */
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background: var(--label-hover-bg) !important;
    border-color: rgba(0, 176, 255, 0.25) !important;
    color: var(--text-color) !important;
    transform: scale(1.02) translateX(4px) !important;
}}

/* Native streamlit metrics upgrade */
div[data-testid="stMetric"] {{
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-3px) !important;
    border-color: rgba(0, 176, 255, 0.2) !important;
    box-shadow: 0 8px 25px rgba(0, 176, 255, 0.1) !important;
}}
div[data-testid="stMetric"] label p, div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: var(--text-color) !important;
}}

/* Custom badges */
.badge {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}}
.badge-success {{ background-color: rgba(0, 230, 118, 0.15); color: #00e676; }}
.badge-danger {{ background-color: rgba(255, 23, 68, 0.15); color: #ff1744; }}
.badge-warning {{ background-color: rgba(255, 235, 59, 0.15); color: #ffeb3b; }}
.badge-info {{ background-color: rgba(0, 176, 255, 0.15); color: #00b0ff; }}

/* Custom alerts */
.info-box {{
    background: var(--info-box-bg) !important;
    border-left: 4px solid #00b0ff;
    padding: 16px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 20px;
    color: var(--text-color) !important;
}}

/* Keep header container transparent */
header[data-testid="stHeader"] {{
    background-color: transparent !important;
    border-bottom: none !important;
}}

/* Hide default streamlit MainMenu, Deploy button, and other header action elements */
#MainMenu {{
    display: none !important;
}}
div[data-testid="stHeaderActionElements"] {{
    display: none !important;
}}
footer {{
    display: none !important;
}}

/* Hide all buttons inside the header EXCEPT the sidebar collapse button */
header[data-testid="stHeader"] button {{
    display: none !important;
}}
header[data-testid="stHeader"] button[data-testid="collapsedControl"] {{
    display: inline-flex !important;
    color: var(--text-color) !important;
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border-color) !important;
    border-bottom: 1px solid var(--border-color) !important;
    border-radius: 0 0 12px 0 !important;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1) !important;
}}
header[data-testid="stHeader"] button[data-testid="collapsedControl"] svg {{
    fill: var(--text-color) !important;
}}

/* st.tabs styling - forces tabs text color to respect theme variables */
button[data-baseweb="tab"] {{
    color: var(--text-muted) !important;
    background-color: transparent !important;
}}
button[data-baseweb="tab"] * {{
    color: inherit !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--text-color) !important;
    border-bottom-color: #00b0ff !important;
}}
button[data-baseweb="tab"][aria-selected="true"] * {{
    color: inherit !important;
    font-weight: 600 !important;
}}

/* Forms & Input fields styling */
div[data-testid="stForm"] {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
}}

/* Custom styles for Streamlit widgets to match the selected theme */
div[data-baseweb="input"] {{
    background-color: var(--bg-color) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--text-color) !important;
}}

div[data-baseweb="input"] input {{
    color: var(--text-color) !important;
}}

div[data-baseweb="select"] > div {{
    background-color: var(--bg-color) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--text-color) !important;
}}

div[data-baseweb="select"] span {{
    color: var(--text-color) !important;
}}

div[role="listbox"] {{
    background-color: var(--bg-color) !important;
    border: 1px solid var(--card-border) !important;
}}

div[role="listbox"] * {{
    color: var(--text-color) !important;
}}

div[role="listbox"] li {{
    background-color: var(--bg-color) !important;
}}

div[role="listbox"] li:hover {{
    background-color: var(--label-hover-bg) !important;
}}

/* Custom styling for multiselect elements to ensure readability */
div[data-baseweb="select"] div[role="button"] {{
    background-color: var(--label-hover-bg) !important;
    color: var(--text-color) !important;
}}

/* Multiselect tags */
span[data-baseweb="tag"] {{
    background-color: var(--label-hover-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--card-border) !important;
}}

/* Buttons */
.stButton>button {{
    background-color: var(--card-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--card-border) !important;
    transition: all 0.3s ease !important;
}}

.stButton>button:hover {{
    border-color: #00b0ff !important;
    color: #00b0ff !important;
}}

/* Custom styled charts fonts & grids via variables */
.js-plotly-plot .gtitle, .js-plotly-plot .xtitle, .js-plotly-plot .ytitle, .js-plotly-plot .legendtext, .js-plotly-plot .tick text {{
    fill: var(--text-color) !important;
}}
.js-plotly-plot .gridpath {{
    stroke: var(--grid-color) !important;
}}
</style>
""", unsafe_allow_html=True)

# Import Data Loader functions and utilities
from data_loader import (
    load_route_profitability_data,
    load_uplift_data,
    load_billing_data,
    load_overall_revenue,
    load_settlement_reconciliation_data,
    get_active_connection_details,
    filter_dataframe
)

# Check connection credentials
connection = get_active_connection_details()
local_csvs_exist = (
    os.path.exists("gold_overall_revenue_in1725.csv") or
    os.path.exists("gold_flight_class_occupancy_IN1725.csv") or
    os.path.exists("gold_inward_billing_in1725.csv")
)

if connection is None and not local_csvs_exist:
    st.title("✈️ Star Air BI Portal Connection")
    st.markdown("### ⚠️ Database Connection Required")
    st.markdown(
        "To view the dashboard metrics and charts, please connect to your **Databricks SQL Warehouse** or **Snowflake Data Warehouse**."
    )
    
    conn_type = st.selectbox("Select Database Source", ["Databricks", "Snowflake"])
    
    if conn_type == "Databricks":
        with st.form("databricks_form"):
            host = st.text_input("Server Hostname", placeholder="xxx.cloud.databricks.com")
            path = st.text_input("HTTP Path", placeholder="/sql/1.0/warehouses/xxx")
            token = st.text_input("Personal Access Token (PAT)", type="password")
            submit = st.form_submit_button("Connect & Launch Dashboard")
            if submit:
                if host and path and token:
                    st.session_state["db_credentials"] = {
                        "DATABRICKS_SERVER_HOSTNAME": host,
                        "DATABRICKS_HTTP_PATH": path,
                        "DATABRICKS_ACCESS_TOKEN": token
                    }
                    st.success("Credentials saved! Connecting...")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Please fill in all Databricks fields.")
    else:
        with st.form("snowflake_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            acct = st.text_input("Account ID", placeholder="xy12345.us-east-2.aws")
            wh = st.text_input("Warehouse", value="COMPUTE_WH")
            db = st.text_input("Database", value="STAR_AIR_DB")
            sch = st.text_input("Schema", value="GOLD")
            submit = st.form_submit_button("Connect & Launch Dashboard")
            if submit:
                if user and pwd and acct and wh and db:
                    st.session_state["db_credentials"] = {
                        "SNOWFLAKE_USER": user,
                        "SNOWFLAKE_PASSWORD": pwd,
                        "SNOWFLAKE_ACCOUNT": acct,
                        "SNOWFLAKE_WAREHOUSE": wh,
                        "SNOWFLAKE_DATABASE": db,
                        "SNOWFLAKE_SCHEMA": sch
                    }
                    st.success("Credentials saved! Connecting...")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Please fill in all Snowflake fields.")
                    
    st.markdown("---")
    st.info("💡 Tip: You can also specify these credentials using environment variables or Streamlit secrets for automatic silent logins.")
    st.stop()

# Load data safely
@st.cache_data
def get_all_data():
    try:
        route_df = load_route_profitability_data()
        uplift_df = load_uplift_data()
        billing_df = load_billing_data()
        overall_rev_df = load_overall_revenue()
        settlement_df = load_settlement_reconciliation_data()
        return route_df, uplift_df, billing_df, overall_rev_df, settlement_df
    except Exception as e:
        st.error(f"Error connecting/querying database: {e}")
        if "db_credentials" in st.session_state:
            if st.button("Reset Saved Session Credentials"):
                del st.session_state["db_credentials"]
                st.cache_data.clear()
                st.rerun()
        return None, None, None, None, None

route_raw, uplift_raw, billing_raw, overall_rev_raw, settlement_raw = get_all_data()

if overall_rev_raw is None:
    st.stop()

# Define Plotly template based on active theme
plotly_template = 'plotly_white' if theme_mode == "Light" else 'plotly_dark'
grid_color = 'rgba(0, 0, 0, 0.08)' if theme_mode == "Light" else 'rgba(255, 255, 255, 0.05)'

page = st.sidebar.radio(
    "Navigation Modules",
    [
        "📊 KPI Dashboard",
        "✈️ Route Performance & Capacity",
        "🔍 Inward Billing Audit"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# Global Year Filter
years = sorted(overall_rev_raw['year'].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)

# Global Month Filter
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
all_months = sorted(overall_rev_raw['month_name'].unique(), key=lambda m: month_order.index(m) if m in month_order else 0)
selected_months = st.sidebar.multiselect("Months", all_months, default=all_months)

# Filter all datasets dynamically
overall_rev_df = filter_dataframe(overall_rev_raw, selected_years, selected_months)
billing_df = filter_dataframe(billing_raw, selected_years, selected_months, year_col='year', month_col='month_name')
route_df = filter_dataframe(route_raw, selected_years, selected_months)
uplift_df = filter_dataframe(uplift_raw, selected_years, selected_months)
settlement_df = filter_dataframe(settlement_raw, selected_years, selected_months, year_col='year', month_col='month_name')

# Sidebar Sync Control
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Data Sync Panel")
sync_source = st.sidebar.selectbox("Sync Target", ["Databricks", "Snowflake"])
if st.sidebar.button("Trigger Cloud Fetch"):
    with st.spinner(f"Connecting and loading from {sync_source}..."):
        try:
            from data_injector import run_sync
            success, msg = run_sync(source=sync_source.lower())
            if success:
                st.sidebar.success(f"Successfully loaded fresh views from {sync_source}!")
                st.cache_data.clear()
                st.rerun()
            else:
                st.sidebar.error(msg)
        except Exception as e:
            st.sidebar.error(f"Sync integration failed: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<div style='font-size: 11px; color: var(--text-muted); text-align: center;'>"
    f"Active Revenue Records: {len(overall_rev_df):,}<br>"
    f"Cloud Views Synchronized"
    f"</div>", 
    unsafe_allow_html=True
)

# ----------------- PAGE 1: KPI DASHBOARD -----------------
if page == "📊 KPI Dashboard":
    st.title("Executive BI Dashboard")
    st.markdown("Overview of key performance indicators, interline revenue, and capacity profiles.")
    
    # Compute executive metrics from filtered overall revenue and billing data
    total_rev = overall_rev_df['Ticket_Amount_AED'].sum()
    total_net_rev = overall_rev_df['Revenue_Per_Ticket_AED'].sum()
    total_tickets = overall_rev_df['Ticket_Count'].sum()
    
    total_passengers = route_df['Passenger_Count'].sum()
    total_seats = route_df['Total_Seats_Available'].sum()
    load_factor = (total_passengers * 100.0) / total_seats if total_seats > 0 else 0
    
    # Billing metrics
    billed_amount = billing_df['Billed_Amount'].sum()
    accepted_amount = billing_df['Accepted_Amount'].sum()
    billing_efficiency = (accepted_amount * 100.0) / billed_amount if billed_amount > 0 else 0

    # KPI Cards Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Gross Ticket Sales</div>"
            f"<div class='metric-value'>AED {total_rev/1e6:.2f}M</div>"
            f"<div class='metric-delta'><span class='delta-up'>▲ Volume: {total_tickets:,.0f} tkts</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Actual Net Revenue</div>"
            f"<div class='metric-value'>AED {total_net_rev/1e6:.2f}M</div>"
            f"<div class='metric-delta'><span class='delta-up'>▲ Net conversion: {(total_net_rev*100.0/total_rev) if total_rev > 0 else 0:.1f}%</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Flown Passengers</div>"
            f"<div class='metric-value'>{total_passengers:,.0f} pax</div>"
            f"<div class='metric-delta'><span class='delta-up'>Load Factor: {load_factor:.2f}%</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Billing Efficiency</div>"
            f"<div class='metric-value'>{billing_efficiency:.1f}%</div>"
            f"<div class='metric-delta'>Inward Interline Audit</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Visualization Row
    c_left, c_right = st.columns([3, 2])
    with c_left:
        # Monthly Revenue Trend Line
        monthly_sales = overall_rev_df.groupby(['year', 'month_name', 'month_num']).agg({
            'Ticket_Amount_AED': 'sum',
            'Revenue_Per_Ticket_AED': 'sum'
        }).reset_index().sort_values(by=['year', 'month_num'])
        monthly_sales['Period'] = monthly_sales['month_name'] + " " + monthly_sales['year'].astype(str)

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=monthly_sales['Period'], 
            y=monthly_sales['Ticket_Amount_AED'],
            mode='lines+markers',
            name='Gross Ticket Sales',
            line=dict(color='#00b0ff', width=3),
            marker=dict(size=8)
        ))
        fig_line.add_trace(go.Scatter(
            x=monthly_sales['Period'], 
            y=monthly_sales['Revenue_Per_Ticket_AED'],
            mode='lines+markers',
            name='Actual Net Revenue',
            line=dict(color='#2a9d8f', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig_line.update_layout(
            title=dict(
                text="<b>Monthly Revenue Trend: Gross Sales vs. Realized Net Revenue</b>",
                font=dict(size=14, color="#00b0ff")
            ),
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=grid_color, title="Amount (AED)"),
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            transition_duration=500
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c_right:
        # Net Revenue Funnel Waterfall
        tax = overall_rev_df['Tax_AED'].sum()
        agent_comm = overall_rev_df['Agent_Commission_AED'].sum()
        discount = overall_rev_df['Discount_AED'].sum()
        inward_billed = overall_rev_df['Inward_Billed_Amount'].sum()
        inward_comm = overall_rev_df['Inward_Commission_Received'].sum()

        fig_wf = go.Figure(go.Waterfall(
            name="Net Revenue Funnel",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x=["Gross Fare Sales", "Taxes Paid", "Agent Commissions", "Discounts Allowed", "Inward Billing (Partner Share)", "Inward Commission Earned", "Actual Net Revenue"],
            textposition="outside",
            text=[
                f"AED {total_rev/1e6:.2f}M",
                f"-AED {tax/1e6:.2f}M",
                f"-AED {agent_comm/1e6:.2f}M",
                f"-AED {discount/1e6:.2f}M",
                f"-AED {inward_billed/1e6:.2f}M",
                f"+AED {inward_comm/1e6:.2f}M",
                f"AED {total_net_rev/1e6:.2f}M"
            ],
            y=[total_rev, -tax, -agent_comm, -discount, -inward_billed, inward_comm, total_net_rev],
            connector=dict(line=dict(color="rgba(128, 128, 128, 0.3)", width=2)),
            decreasing={"marker":{"color":"#ff1744"}},
            increasing={"marker":{"color":"#00e676"}},
            totals={"marker":{"color":"#00b0ff"}}
        ))
        
        fig_wf.update_layout(
            title=dict(
                text="<b>Net Revenue Funnel: Margin Leakages to Partners and Agents</b>",
                font=dict(size=13, color="#00b0ff")
            ),
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor=grid_color, title="Amount (AED)"),
            margin=dict(l=20, r=20, t=50, b=20),
            transition_duration=500
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    # Narrative Insight Section
    st.subheader("Data Highlights & Actionable Insights")
    top_route = route_df.groupby('Route')['Revenue_AED'].sum().idxmax()
    top_route_rev = route_df.groupby('Route')['Revenue_AED'].sum().max()
    
    st.markdown(f"""
    <div class='info-box'>
        <h4 style='color: #00b0ff; margin-top:0;'>💡 Network Profitability Summary</h4>
        <ul>
            <li><b>Star Route:</b> Route <b>{top_route}</b> is the leading sales driver, generating a gross revenue of <b>AED {top_route_rev:,.2f}</b>.</li>
            <li><b>Interline Revenue Impact:</b> Out of AED {total_rev/1e6:.2f}M gross ticket bookings, interline inward billing fees paid to partner airlines (<b>AED {inward_billed/1e6:.2f}M</b>) represent the single largest margin drain.</li>
            <li><b>Billing Auditing Health:</b> Outward interline claims have an acceptance rate of <span class='badge badge-success'>{billing_efficiency:.1f}%</span>. Commercially resolving rejected claims represents a direct recovery opportunity.</li>
            <li><b>Operational Capacity:</b> Flown load factor stands at <b>{load_factor:.2f}%</b>, reflecting solid seating utilization across the route network.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----------------- PAGE 2: ROUTE PERFORMANCE & CAPACITY -----------------
elif page == "✈️ Route Performance & Capacity":
    st.title("Route Performance & Capacity Analysis")
    st.markdown("Detailed view of route profitability ledgers, capacity utilizations, and route comparisons.")
    
    tab1, tab2, tab3 = st.tabs(["Route Performance Explorer", "Capacity & Operational Trends", "Route Profitability Comparison"])
    
    with tab1:
        st.subheader("Route Financial Ledger & Profitability Rankings")
        
        # Monthly Revenue Rank Trend for Top 5 routes
        route_monthly = route_df.groupby(['Route', 'year', 'month_name'])['Revenue_AED'].sum().reset_index()
        route_monthly['month_num'] = route_monthly['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
        route_monthly = route_monthly.sort_values(by=['year', 'month_num', 'Revenue_AED'], ascending=[True, True, False])
        route_monthly['Rank'] = route_monthly.groupby(['year', 'month_num'])['Revenue_AED'].rank(ascending=False, method='first')
        
        top_routes = route_df.groupby('Route')['Revenue_AED'].sum().nlargest(5).index.tolist()
        rank_trend_df = route_monthly[route_monthly['Route'].isin(top_routes)].copy()
        rank_trend_df['Period'] = rank_trend_df['month_name'] + " " + rank_trend_df['year'].astype(str)
        
        fig_rank = px.line(
            rank_trend_df,
            x='Period',
            y='Rank',
            color='Route',
            markers=True,
            title='Monthly Revenue Ranking Trend (Top 5 Routes)',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig_rank.update_layout(
            template=plotly_template,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(autorange='reversed', tickmode='linear', dtick=1, title="Revenue Rank"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_rank, use_container_width=True)
        
        # Route ledger
        st.subheader("Detailed Route Profitability Ledger")
        display_route_df = route_df.groupby('Route').agg({
            'Total_Tickets_Sold': 'sum',
            'Revenue_AED': 'sum',
            'Net_Revenue_AED': 'sum',
            'Passenger_Count': 'sum',
            'Total_Flights': 'sum',
            'Total_Seats_Available': 'sum'
        }).reset_index()
        
        display_route_df['Avg_Fare_AED'] = (display_route_df['Revenue_AED'] / display_route_df['Total_Tickets_Sold']).round(2)
        display_route_df['Load_Factor_Pct'] = ((display_route_df['Passenger_Count'] * 100.0) / display_route_df['Total_Seats_Available']).round(2)
        display_route_df = display_route_df.sort_values(by='Revenue_AED', ascending=False)
        
        styled_df = display_route_df.copy()
        styled_df['Revenue_AED'] = styled_df['Revenue_AED'].map(lambda x: f"AED {x:,.2f}")
        styled_df['Net_Revenue_AED'] = styled_df['Net_Revenue_AED'].map(lambda x: f"AED {x:,.2f}")
        styled_df['Avg_Fare_AED'] = styled_df['Avg_Fare_AED'].map(lambda x: f"AED {x:,.2f}" if not pd.isna(x) else "AED 0.00")
        styled_df['Load_Factor_Pct'] = styled_df['Load_Factor_Pct'].map(lambda x: f"{x:.2f}%" if not pd.isna(x) else "0.00%")
        styled_df['Total_Tickets_Sold'] = styled_df['Total_Tickets_Sold'].map('{:,.0f}'.format)
        styled_df['Passenger_Count'] = styled_df['Passenger_Count'].map('{:,.0f}'.format)
        styled_df['Total_Flights'] = styled_df['Total_Flights'].map('{:,.0f}'.format)
        
        st.dataframe(
            styled_df[['Route', 'Total_Tickets_Sold', 'Revenue_AED', 'Net_Revenue_AED', 'Avg_Fare_AED', 'Passenger_Count', 'Total_Flights', 'Load_Factor_Pct']],
            hide_index=True,
            use_container_width=True
        )

    with tab2:
        st.subheader("Capacity & Seating Efficiencies")
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("Traffic Profiling: Weekend vs Weekday")
            weekend_df = uplift_df.groupby('is_weekend').agg({
                'Passenger_Count': 'sum',
                'Total_Seats': 'sum'
            }).reset_index()
            weekend_df['Load_Factor_Pct'] = (weekend_df['Passenger_Count'] * 100.0) / weekend_df['Total_Seats']
            weekend_df['Day_Type'] = weekend_df['is_weekend'].map({True: 'Weekend Flights', False: 'Weekday Flights'})
            
            fig_day = px.bar(
                weekend_df,
                x='Day_Type',
                y='Load_Factor_Pct',
                color='Day_Type',
                text=weekend_df['Load_Factor_Pct'].map(lambda x: f"{x:.2f}%"),
                color_discrete_map={'Weekend Flights': '#ffeb3b', 'Weekday Flights': '#00b0ff'}
            )
            fig_day.update_layout(
                template=plotly_template,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title='Load Factor (%)', range=[0, 100], gridcolor=grid_color),
                xaxis=dict(title=''),
                showlegend=False,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_day, use_container_width=True)
            
        with c_right:
            st.subheader("Capacity Scatter Profile")
            route_cap = uplift_df.groupby('Route').agg({
                'Total_Seats': 'sum',
                'Passenger_Count': 'sum',
                'Flight_no': 'count'
            }).reset_index()
            route_cap['Load_Factor'] = (route_cap['Passenger_Count'] * 100.0) / route_cap['Total_Seats']
            
            fig_scat = px.scatter(
                route_cap,
                x='Total_Seats',
                y='Passenger_Count',
                size='Flight_no',
                color='Load_Factor',
                hover_name='Route',
                color_continuous_scale='Viridis',
                labels={'Total_Seats': 'Total Seats Offered', 'Passenger_Count': 'Total Flown Passengers', 'Load_Factor': 'Avg Load Factor (%)'}
            )
            fig_scat.update_layout(
                template=plotly_template,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor=grid_color),
                yaxis=dict(gridcolor=grid_color),
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_scat, use_container_width=True)

    with tab3:
        st.subheader("Side-by-Side Route Comparison")
        c1, c2 = st.columns(2)
        all_routes = sorted(route_df['Route'].unique())
        with c1:
            route_a = st.selectbox("Select Route A", all_routes, index=0)
        with c2:
            route_b = st.selectbox("Select Route B", all_routes, index=min(1, len(all_routes)-1))
            
        if route_a == route_b:
            st.warning("Please select two different routes for comparison.")
        else:
            stats_a = display_route_df[display_route_df['Route'] == route_a].iloc[0]
            stats_b = display_route_df[display_route_df['Route'] == route_b].iloc[0]
            
            metrics_list = [
                ('Gross Revenue', stats_a['Revenue_AED'], stats_b['Revenue_AED'], 'currency'),
                ('Net Revenue', stats_a['Net_Revenue_AED'], stats_b['Net_Revenue_AED'], 'currency'),
                ('Tickets Sold', stats_a['Total_Tickets_Sold'], stats_b['Total_Tickets_Sold'], 'numeric'),
                ('Passengers Flown', stats_a['Passenger_Count'], stats_b['Passenger_Count'], 'numeric'),
                ('Average Fare', stats_a['Avg_Fare_AED'], stats_b['Avg_Fare_AED'], 'currency'),
                ('Load Factor (%)', stats_a['Load_Factor_Pct'], stats_b['Load_Factor_Pct'], 'percentage'),
                ('Flight Count', stats_a['Total_Flights'], stats_b['Total_Flights'], 'numeric')
            ]
            
            col_a, col_metric, col_b = st.columns([2, 2, 2])
            with col_metric:
                st.markdown("<div style='text-align: center; font-weight: bold; margin-bottom:10px;'>METRIC</div>", unsafe_allow_html=True)
                for label, _, _, _ in metrics_list:
                    st.markdown(f"<div style='text-align: center; padding: 10px; font-weight: 500; border-bottom: 1px solid var(--border-color);'>{label}</div>", unsafe_allow_html=True)
            
            with col_a:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #00b0ff; margin-bottom:10px;'>{route_a}</div>", unsafe_allow_html=True)
                for _, val_a, val_b, m_type in metrics_list:
                    is_better = val_a > val_b if "Load Factor" in label or val_a != 0 else val_a > val_b
                    color = "#00e676" if is_better else "var(--text-color)"
                    
                    if m_type == 'currency':
                        disp = f"AED {val_a:,.2f}"
                    elif m_type == 'percentage':
                        disp = f"{val_a:.2f}%"
                    else:
                        disp = f"{val_a:,.0f}"
                    st.markdown(f"<div style='text-align: center; padding: 10px; color: {color}; border-bottom: 1px solid var(--border-color); font-weight: 600;'>{disp}</div>", unsafe_allow_html=True)
                    
            with col_b:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #2a9d8f; margin-bottom:10px;'>{route_b}</div>", unsafe_allow_html=True)
                for _, val_a, val_b, m_type in metrics_list:
                    is_better = val_b > val_a
                    color = "#00e676" if is_better else "var(--text-color)"
                    
                    if m_type == 'currency':
                        disp = f"AED {val_b:,.2f}"
                    elif m_type == 'percentage':
                        disp = f"{val_b:.2f}%"
                    else:
                        disp = f"{val_b:,.0f}"
                    st.markdown(f"<div style='text-align: center; padding: 10px; color: {color}; border-bottom: 1px solid var(--border-color); font-weight: 600;'>{disp}</div>", unsafe_allow_html=True)

# ----------------- PAGE 3: INWARD BILLING AUDIT -----------------
elif page == "🔍 Inward Billing Audit":
    st.title("Inward Billing & Rejection Audit")
    st.markdown("Reconciling passenger billing claims, carrier rejections, and direct interline partner settlement margins.")
    
    tab1, tab2 = st.tabs(["Outward Claims & Rejections", "Partner Settlement (Sales vs. Billed)"])
    
    with tab1:
        total_billed = billing_df['Billed_Amount'].sum()
        total_accepted = billing_df['Accepted_Amount'].sum()
        total_rejected = billing_df['Rejected_Amount'].sum()
        settlement_gap = total_billed - total_accepted
        billing_eff = (total_accepted * 100.0) / total_billed if total_billed > 0 else 0
        rej_rate = (total_rejected * 100.0) / total_billed if total_billed > 0 else 0
        
        # Audit highlights cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"<div class='card-container'>"
                f"<div class='metric-header'>Total Billed Claims</div>"
                f"<div class='metric-value'>AED {total_billed/1e6:.2f}M</div>"
                f"<div class='metric-delta'>Claimed Amount</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div class='card-container'>"
                f"<div class='metric-header'>Accepted & Settled</div>"
                f"<div class='metric-value'>AED {total_accepted/1e6:.2f}M</div>"
                f"<div class='metric-delta'><span class='delta-up'>Eff: {billing_eff:.2f}%</span></div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"<div class='card-container'>"
                f"<div class='metric-header'>Rejected Claims</div>"
                f"<div class='metric-value'>AED {total_rejected/1e6:.2f}M</div>"
                f"<div class='metric-delta'><span class='delta-down'>Rej Rate: {rej_rate:.2f}%</span></div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f"<div class='card-container'>"
                f"<div class='metric-header'>Outstanding Gap</div>"
                f"<div class='metric-value'>AED {settlement_gap/1e6:.2f}M</div>"
                f"<div class='metric-delta'>Outstanding Variance</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            
        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("Billing Efficiency & Rejection Trends")
            billing_monthly = billing_df.groupby(['year', 'month_name']).agg({
                'Billed_Amount': 'sum',
                'Accepted_Amount': 'sum',
                'Rejected_Amount': 'sum'
            }).reset_index()
            billing_monthly['month_num'] = billing_monthly['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
            billing_monthly = billing_monthly.sort_values(by=['year', 'month_num'])
            billing_monthly['Period'] = billing_monthly['month_name'] + " " + billing_monthly['year'].astype(str)
            billing_monthly['Rejection_Rate'] = (billing_monthly['Rejected_Amount'] * 100.0) / billing_monthly['Billed_Amount']
            billing_monthly['Efficiency_Rate'] = (billing_monthly['Accepted_Amount'] * 100.0) / billing_monthly['Billed_Amount']
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=billing_monthly['Period'],
                y=billing_monthly['Efficiency_Rate'],
                mode='lines+markers',
                name='Billing Efficiency Pct',
                line=dict(color='#2a9d8f', width=3),
                marker=dict(size=8)
            ))
            fig_trend.add_trace(go.Scatter(
                x=billing_monthly['Period'],
                y=billing_monthly['Rejection_Rate'],
                mode='lines+markers',
                name='Rejection Rate Pct',
                line=dict(color='#ff1744', width=3),
                marker=dict(size=8)
            ))
            fig_trend.update_layout(
                template=plotly_template,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor=grid_color, title='Percentage (%)', range=[0, 100]),
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with c_right:
            st.subheader("Billed Amount vs. Accepted vs. Rejected (AED)")
            fig_bars = go.Figure()
            fig_bars.add_trace(go.Bar(
                x=billing_monthly['Period'],
                y=billing_monthly['Billed_Amount'],
                name='Billed Amount',
                marker_color='#00b0ff'
            ))
            fig_bars.add_trace(go.Bar(
                x=billing_monthly['Period'],
                y=billing_monthly['Accepted_Amount'],
                name='Accepted Amount',
                marker_color='#2a9d8f'
            ))
            fig_bars.add_trace(go.Bar(
                x=billing_monthly['Period'],
                y=billing_monthly['Rejected_Amount'],
                name='Rejected Amount',
                marker_color='#ff1744'
            ))
            fig_bars.update_layout(
                template=plotly_template,
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor=grid_color, title='AED'),
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_bars, use_container_width=True)

        # Detailed Audit Ledger
        st.subheader("Detailed Billing Audit Ledger")
        audit_table = billing_df.groupby(['Billed_Carrier_Name', 'Billed_Currency']).agg({
            'Ticket_Count': 'sum',
            'Billed_Amount': 'sum',
            'Accepted_Amount': 'sum',
            'Rejected_Amount': 'sum'
        }).reset_index()
        
        audit_table['Settlement_Gap'] = audit_table['Billed_Amount'] - audit_table['Accepted_Amount']
        audit_table['Efficiency_Rate'] = ((audit_table['Accepted_Amount'] * 100.0) / audit_table['Billed_Amount']).round(2)
        audit_table = audit_table.sort_values(by='Billed_Amount', ascending=False)
        
        styled_audit = audit_table.copy()
        styled_audit['Billed_Amount'] = styled_audit['Billed_Amount'].map(lambda x: f"AED {x:,.2f}")
        styled_audit['Accepted_Amount'] = styled_audit['Accepted_Amount'].map(lambda x: f"AED {x:,.2f}")
        styled_audit['Rejected_Amount'] = styled_audit['Rejected_Amount'].map(lambda x: f"AED {x:,.2f}")
        styled_audit['Settlement_Gap'] = styled_audit['Settlement_Gap'].map(lambda x: f"AED {x:,.2f}")
        styled_audit['Efficiency_Rate'] = styled_audit['Efficiency_Rate'].map(lambda x: f"{x:.2f}%")
        styled_audit['Ticket_Count'] = styled_audit['Ticket_Count'].map('{:,.0f}'.format)
        
        st.dataframe(styled_audit, hide_index=True, use_container_width=True)

        # Inward Billing Story commentary
        st.markdown(f"""
        <div class='info-box'>
            <h4 style='color: #00b0ff; margin-top:0;'>🔍 Inward Billing Leakage Findings</h4>
            <ul>
                <li><b>Billing Gap Drivers:</b> Out of <b>AED {total_billed/1e6:.2f}M</b> total outward interline bills, partner airlines rejected <b>AED {total_rejected/1e6:.2f}M</b> (<b>{rej_rate:.1f}%</b> of claims).</li>
                <li><b>Carrier Behavior:</b> The detailed carrier ledger exposes that claims routed under specific currencies or carriers undergo different audit scrutiny. Specific carriers with efficiency rates under 85% must be targeted for claims audits.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Interline Partner Billing vs. Sales Reconciliation")
        st.markdown(
            "When Star Air books a ticket (Sales) but the passenger is flown by a partner airline, the partner carrier "
            "bills Star Air (Inward Billing) to settle. Star Air audits these claims, accepting some amount to pay (Settled Value) "
            "and rejecting any incorrect billing (Rejections)."
        )
        
        if len(settlement_df) == 0:
            st.warning("No settlement reconciliation records match the active global filters.")
        else:
            total_sales_val = settlement_df['Sales_Value'].sum()
            total_billed_val = settlement_df['Billing_Value'].sum()
            total_settled_val = settlement_df['Settlement_Value'].sum()
            total_rejected_val = settlement_df['Rejected_Value'].sum()
            net_retention = total_sales_val - total_settled_val
            retention_margin_pct = (net_retention * 100.0) / total_sales_val if total_sales_val > 0 else 0
            acceptance_rate = (total_settled_val * 100.0) / total_billed_val if total_billed_val > 0 else 0
            rejection_rate = (total_rejected_val * 100.0) / total_billed_val if total_billed_val > 0 else 0
            
            # KPI Cards
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(
                    f"<div class='card-container'>"
                    f"<div class='metric-header'>Star Air Sale Value</div>"
                    f"<div class='metric-value'>AED {total_sales_val/1e6:.2f}M</div>"
                    f"<div class='metric-delta'>Original Bookings</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    f"<div class='card-container'>"
                    f"<div class='metric-header'>Partner Billed Value</div>"
                    f"<div class='metric-value'>AED {total_billed_val/1e6:.2f}M</div>"
                    f"<div class='metric-delta'>Inward Claims</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with c3:
                st.markdown(
                    f"<div class='card-container'>"
                    f"<div class='metric-header'>Accepted to Pay</div>"
                    f"<div class='metric-value'>AED {total_settled_val/1e6:.2f}M</div>"
                    f"<div class='metric-delta'><span class='delta-up'>Acceptance: {acceptance_rate:.2f}%</span></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with c4:
                color_class = "delta-up" if net_retention >= 0 else "delta-down"
                sign = "▲ Surplus" if net_retention >= 0 else "▼ Deficit"
                val_color = "#a5d6a7" if net_retention >= 0 else "#ff8a80"
                st.markdown(
                    f"<div class='card-container'>"
                    f"<div class='metric-header'>Net Retention Surplus</div>"
                    f"<div class='metric-value' style='background: linear-gradient(135deg, #ffffff 0%, {val_color} 100%) !important;'>AED {net_retention/1e6:.2f}M</div>"
                    f"<div class='metric-delta'><span class='{color_class}'>{sign} ({retention_margin_pct:.2f}%)</span></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
            # Monthly comparison plots
            c_left, c_right = st.columns(2)
            with c_left:
                st.subheader("Monthly Sales vs. Billed vs. Accepted Claims (AED)")
                monthly_settlement = settlement_df.groupby(['year', 'month_name']).agg({
                    'Sales_Value': 'sum',
                    'Billing_Value': 'sum',
                    'Settlement_Value': 'sum',
                    'Rejected_Value': 'sum'
                }).reset_index()
                monthly_settlement['month_num'] = monthly_settlement['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
                monthly_settlement = monthly_settlement.sort_values(by=['year', 'month_num'])
                monthly_settlement['Period'] = monthly_settlement['month_name'] + " " + monthly_settlement['year'].astype(str)
                
                fig_monthly = go.Figure()
                fig_monthly.add_trace(go.Bar(
                    x=monthly_settlement['Period'],
                    y=monthly_settlement['Sales_Value'],
                    name='Star Air Sale Value',
                    marker_color='#00b0ff'
                ))
                fig_monthly.add_trace(go.Bar(
                    x=monthly_settlement['Period'],
                    y=monthly_settlement['Billing_Value'],
                    name='Partner Billed Value',
                    marker_color='#ff8a80'
                ))
                fig_monthly.add_trace(go.Bar(
                    x=monthly_settlement['Period'],
                    y=monthly_settlement['Settlement_Value'],
                    name='Accepted to Pay',
                    marker_color='#2a9d8f'
                ))
                fig_monthly.update_layout(
                    template=plotly_template,
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor=grid_color, title='AED'),
                    margin=dict(l=20, r=20, t=30, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
                
            with c_right:
                st.subheader("Monthly Acceptance & Rejection Rates (%)")
                monthly_settlement['Acceptance_Rate'] = (monthly_settlement['Settlement_Value'] * 100.0) / monthly_settlement['Billing_Value']
                monthly_settlement['Rejection_Rate'] = (monthly_settlement['Rejected_Value'] * 100.0) / monthly_settlement['Billing_Value']
                
                fig_rates = go.Figure()
                fig_rates.add_trace(go.Scatter(
                    x=monthly_settlement['Period'],
                    y=monthly_settlement['Acceptance_Rate'],
                    mode='lines+markers',
                    name='Acceptance Rate (%)',
                    line=dict(color='#2a9d8f', width=3),
                    marker=dict(size=8)
                ))
                fig_rates.add_trace(go.Scatter(
                    x=monthly_settlement['Period'],
                    y=monthly_settlement['Rejection_Rate'],
                    mode='lines+markers',
                    name='Rejection Rate (%)',
                    line=dict(color='#ff1744', width=3),
                    marker=dict(size=8)
                ))
                fig_rates.update_layout(
                    template=plotly_template,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor=grid_color, title='Percentage (%)', range=[0, 100]),
                    margin=dict(l=20, r=20, t=30, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_rates, use_container_width=True)
                
            # Detailed Settlement Ledger
            st.subheader("Detailed Settlement Ledger")
            settlement_ledger = settlement_df.groupby('year').agg({
                'Sales_Value': 'sum',
                'Billing_Value': 'sum',
                'Settlement_Value': 'sum',
                'Rejected_Value': 'sum'
            }).reset_index()
            settlement_ledger['Net_Retention'] = settlement_ledger['Sales_Value'] - settlement_ledger['Settlement_Value']
            settlement_ledger['Acceptance_Rate'] = ((settlement_ledger['Settlement_Value'] * 100.0) / settlement_ledger['Billing_Value']).round(2)
            
            styled_settle = settlement_ledger.copy()
            styled_settle['Sales_Value'] = styled_settle['Sales_Value'].map(lambda x: f"AED {x:,.2f}")
            styled_settle['Billing_Value'] = styled_settle['Billing_Value'].map(lambda x: f"AED {x:,.2f}")
            styled_settle['Settlement_Value'] = styled_settle['Settlement_Value'].map(lambda x: f"AED {x:,.2f}")
            styled_settle['Rejected_Value'] = styled_settle['Rejected_Value'].map(lambda x: f"AED {x:,.2f}")
            styled_settle['Net_Retention'] = styled_settle['Net_Retention'].map(lambda x: f"AED {x:,.2f}")
            styled_settle['Acceptance_Rate'] = styled_settle['Acceptance_Rate'].map(lambda x: f"{x:.2f}%")
            
            styled_settle.rename(columns={'year': 'Year'}, inplace=True)
            
            st.dataframe(styled_settle, hide_index=True, use_container_width=True)
            
            # Route-level comparison ledger
            st.subheader("Route-level Interline Settlement Deficit Audit (AED)")
            st.markdown("Reconciling ticket sales with estimated partner billing settlement at the route level to identify leakage sectors.")
            
            interline_df = overall_rev_df[overall_rev_df['Inward_Available_Flag'] == 'Yes'].copy()
            if len(interline_df) == 0:
                st.warning("No route interline records match the active global filters.")
            else:
                route_interline = interline_df.groupby('Route').agg({
                    'Ticket_Count': 'sum',
                    'Ticket_Amount_AED': 'sum',
                    'Inward_Billed_Amount': 'sum'
                }).reset_index()
                
                # Apply the overall historical acceptance rate to estimate settlement
                hist_acc_rate = total_settled_val / total_billed_val if total_billed_val > 0 else 0.846
                
                route_interline['Est_Accepted_Pay'] = route_interline['Inward_Billed_Amount'] * hist_acc_rate
                route_interline['Est_Rejected_Amount'] = route_interline['Inward_Billed_Amount'] - route_interline['Est_Accepted_Pay']
                route_interline['Net_Retention_Surplus'] = route_interline['Ticket_Amount_AED'] - route_interline['Est_Accepted_Pay']
                route_interline['Retention_Margin_Pct'] = (route_interline['Net_Retention_Surplus'] * 100.0) / route_interline['Ticket_Amount_AED']
                
                route_interline = route_interline.sort_values(by='Net_Retention_Surplus', ascending=True) # Biggest losses first
                
                styled_route_interline = route_interline.copy()
                styled_route_interline['Ticket_Amount_AED'] = styled_route_interline['Ticket_Amount_AED'].map(lambda x: f"AED {x:,.2f}")
                styled_route_interline['Inward_Billed_Amount'] = styled_route_interline['Inward_Billed_Amount'].map(lambda x: f"AED {x:,.2f}")
                styled_route_interline['Est_Accepted_Pay'] = styled_route_interline['Est_Accepted_Pay'].map(lambda x: f"AED {x:,.2f}")
                styled_route_interline['Est_Rejected_Amount'] = styled_route_interline['Est_Rejected_Amount'].map(lambda x: f"AED {x:,.2f}")
                styled_route_interline['Net_Retention_Surplus'] = styled_route_interline['Net_Retention_Surplus'].map(lambda x: f"AED {x:,.2f}")
                styled_route_interline['Retention_Margin_Pct'] = styled_route_interline['Retention_Margin_Pct'].map(lambda x: f"{x:.2f}%")
                styled_route_interline['Ticket_Count'] = styled_route_interline['Ticket_Count'].map('{:,.0f}'.format)
                
                st.dataframe(
                    styled_route_interline[['Route', 'Ticket_Count', 'Ticket_Amount_AED', 'Inward_Billed_Amount', 'Est_Accepted_Pay', 'Est_Rejected_Amount', 'Net_Retention_Surplus', 'Retention_Margin_Pct']],
                    hide_index=True,
                    use_container_width=True
                )
            
            # Narrative insights card
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #00b0ff; margin-top:0;'>💡 Settlement Audit & Pricing Insight</h4>
                <ul>
                    <li><b>Pricing Discrepancy & Leakage:</b> Comparing partner billing with Star Air's sales shows that our passenger ticket fares cover partner codeshare costs. The net retention surplus (Sale Value - Accepted Payment) is positive on average, meaning Star Air retains margin.</li>
                    <li><b>Auditing Efficiency:</b> By rejecting billing discrepancies (average rejection rate: <b>{rejection_rate:.2f}%</b>), Star Air has saved <b>AED {total_rejected_val/1e6:.2f}M</b> from partner claims.</li>
                    <li><b>Actionable Remedy:</b> The Commercial team must audit routes with low retention margins (indicated in red/negative surplus) and renegotiate interline codeshare rates or adjust our passenger ticket pricing.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer credits (rendered at the bottom of every page)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding: 15px 0; font-size: 13px; color: var(--text-muted); font-weight: 500; letter-spacing: 0.05em;'>"
    "Star Air BI Portal | Dashboard done by <b>Kaviram</b>"
    "</div>",
    unsafe_allow_html=True
)
