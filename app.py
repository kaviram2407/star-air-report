import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="Star Air Business Intelligence Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Main font styling */
html, body, [data-testid="stSidebar"], .stMarkdown, p, div, label {
    font-family: 'Outfit', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

/* Glassmorphism card utility */
.card-container {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.metric-header {
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}

.metric-delta {
    font-size: 13px;
    font-weight: 500;
}

.delta-up {
    color: #00e676;
}

.delta-down {
    color: #ff1744;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #0c1017 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Custom badges */
.badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}
.badge-success { background-color: rgba(0, 230, 118, 0.15); color: #00e676; }
.badge-danger { background-color: rgba(255, 23, 68, 0.15); color: #ff1744; }
.badge-warning { background-color: rgba(255, 235, 59, 0.15); color: #ffeb3b; }
.badge-info { background-color: rgba(0, 176, 255, 0.15); color: #00b0ff; }

/* Custom alerts */
.info-box {
    background: rgba(0, 176, 255, 0.05);
    border-left: 4px solid #00b0ff;
    padding: 16px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 20px;
}

/* Hide default streamlit headers and footer */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Import Data Loader functions
from data_loader import (
    load_sales_data,
    load_route_profitability_data,
    load_uplift_data,
    load_billing_data,
    load_date_dimension,
    AIRPORT_COORDS,
    AIRPORT_GEOGRAPHY,
    get_active_connection_details
)

# Check connection credentials
connection = get_active_connection_details()

if connection is None:
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
        sales_df = load_sales_data()
        route_df = load_route_profitability_data()
        uplift_df = load_uplift_data()
        billing_df = load_billing_data()
        date_df = load_date_dimension()
        return sales_df, route_df, uplift_df, billing_df, date_df
    except Exception as e:
        st.error(f"Error connecting/querying database: {e}")
        if "db_credentials" in st.session_state:
            if st.button("Reset Saved Session Credentials"):
                del st.session_state["db_credentials"]
                st.cache_data.clear()
                st.rerun()
        return None, None, None, None, None

sales_raw, route_raw, uplift_raw, billing_raw, date_raw = get_all_data()

if sales_raw is None:
    st.stop()

# Helper function to generate clean date columns if needed
def clean_date_filters(df, date_col):
    df_sorted = df.sort_values(by=date_col)
    years = sorted(df_sorted[date_col].dt.year.unique())
    months = sorted(df_sorted[date_col].dt.strftime('%B').unique(), key=lambda m: datetime.strptime(m, '%B').month)
    return years, months

# Sidebar Controls & Global Filters
st.sidebar.markdown(
    "<div style='text-align: center; padding: 10px 0;'>"
    "<h2 style='color: #00b0ff; margin-bottom: 0;'>STAR AIR</h2>"
    "<p style='font-size: 13px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.1em;'>Business Intelligence</p>"
    "</div>", 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Navigation Selector
page = st.sidebar.radio(
    "Navigation Modules",
    [
        "📊 KPI Dashboard",
        "✈️ Revenue & Routes",
        "📈 Occupancy & Operations",
        "👥 Agent Performance",
        "🌍 Geographic Segmentation",
        "🔍 Settlement & Billing Audit"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# Carrier Selection (Offline Mode displays Star Air)
carriers = ["All", "Star Air"]
selected_carrier = st.sidebar.selectbox("Carrier", carriers)

# Year Filter
years = sorted(sales_raw['year'].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)

# Month Filter
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
all_months = sorted(sales_raw['month_name'].unique(), key=lambda m: month_order.index(m) if m in month_order else 0)
selected_months = st.sidebar.multiselect("Months", all_months, default=all_months)

# Apply global filtering function
def filter_dataframe(df, date_col=None, year_col='year', month_col='month_name'):
    filtered_df = df.copy()
    if selected_carrier != "All" and "Carrier_Name" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Carrier_Name'] == selected_carrier]
    
    if selected_years:
        filtered_df = filtered_df[filtered_df[year_col].isin(selected_years)]
        
    if selected_months:
        filtered_df = filtered_df[filtered_df[month_col].isin(selected_months)]
        
    return filtered_df

# Filter all datasets dynamically
sales_df = filter_dataframe(sales_raw)
route_df = filter_dataframe(route_raw)
uplift_df = filter_dataframe(uplift_raw)
billing_df = filter_dataframe(billing_raw, year_col='year', month_col='month_name')

# Sidebar Context Summary & Cloud Sync Controls
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
                st.cache_data.clear() # Clear streamlit cache to reload the updated data!
                st.rerun() # Force page refresh to update all visualizations
            else:
                st.sidebar.error(msg)
        except Exception as e:
            st.sidebar.error(f"Sync integration failed: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<div style='font-size: 12px; color: rgba(255,255,255,0.4); text-align: center;'>"
    f"Active Filter Records: {len(sales_df):,}<br>"
    f"Cloud Views Synchronized"
    f"</div>", 
    unsafe_allow_html=True
)

# ----------------- PAGE 1: KPI DASHBOARD -----------------
if page == "📊 KPI Dashboard":
    st.title("Executive BI Dashboard")
    st.markdown("Overview of key performance indicators, revenue, operations, and settlement tracking.")
    
    # Calculate global metrics based on filtered datasets
    total_rev = sales_df['Gross_Fare_AED'].sum()
    total_net_rev = sales_df['Net_Fare_AED'].sum()
    total_tickets = sales_df['Total_Tickets_Sold'].sum()
    total_passengers = uplift_df['Passenger_Count'].sum()
    avg_ticket_value = sales_df['Gross_Fare_AED'].sum() / sales_df['Total_Tickets_Sold'].sum() if sales_df['Total_Tickets_Sold'].sum() > 0 else 0
    
    total_seats = uplift_df['Total_Seats'].sum()
    weighted_load_factor = (uplift_df['Passenger_Count'].sum() * 100.0) / total_seats if total_seats > 0 else 0
    
    # Billing KPIs
    billed_amount = billing_df['Billed_Amount'].sum()
    accepted_amount = billing_df['Accepted_Amount'].sum()
    rejected_amount = billing_df['Rejected_Amount'].sum()
    billing_efficiency = (accepted_amount * 100.0) / billed_amount if billed_amount > 0 else 0
    rejection_pct = (rejected_amount * 100.0) / billed_amount if billed_amount > 0 else 0

    # Layout: Top Row Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Gross Revenue (AED)</div>"
            f"<div class='metric-value'>AED {total_rev/1e6:.2f}M</div>"
            f"<div class='metric-delta'><span class='delta-up'>▲ Net: AED {total_net_rev/1e6:.2f}M</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Tickets Sold</div>"
            f"<div class='metric-value'>{total_tickets:,.0f}</div>"
            f"<div class='metric-delta'><span class='delta-up'>Avg Fare: AED {avg_ticket_value:.2f}</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Passengers Flown</div>"
            f"<div class='metric-value'>{total_passengers:,.0f}</div>"
            f"<div class='metric-delta'><span class='delta-up'>Load Factor: {weighted_load_factor:.2f}%</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f"<div class='card-container'>"
            f"<div class='metric-header'>Billing Efficiency</div>"
            f"<div class='metric-value'>{billing_efficiency:.1f}%</div>"
            f"<div class='metric-delta'><span class='delta-down'>Rejections: {rejection_pct:.1f}%</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
    # Second Row: Visualizations
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.subheader("Monthly Sales Trend")
        # Aggregate monthly sales
        monthly_sales = sales_df.groupby(['year', 'month_name'])[['Gross_Fare_AED', 'Net_Fare_AED']].sum().reset_index()
        # Sort by month order
        monthly_sales['month_num'] = monthly_sales['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
        monthly_sales = monthly_sales.sort_values(by=['year', 'month_num'])
        monthly_sales['Period'] = monthly_sales['month_name'] + " " + monthly_sales['year'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_sales['Period'], 
            y=monthly_sales['Gross_Fare_AED'],
            mode='lines+markers',
            name='Gross Fare (AED)',
            line=dict(color='#00b0ff', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=monthly_sales['Period'], 
            y=monthly_sales['Net_Fare_AED'],
            mode='lines+markers',
            name='Net Fare (AED)',
            line=dict(color='#2a9d8f', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Amount (AED)"),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_right:
        st.subheader("Revenue by Class of Travel")
        class_rev = sales_df.groupby('Class_of_Travel')['Gross_Fare_AED'].sum().reset_index()
        class_map = {'Y': 'Economy (Y)', 'J': 'Business (J)', 'F': 'First (F)'}
        class_rev['Class_Name'] = class_rev['Class_of_Travel'].map(class_map)
        
        fig = px.pie(
            class_rev, 
            values='Gross_Fare_AED', 
            names='Class_Name',
            hole=0.4,
            color_discrete_sequence=['#00b0ff', '#2a9d8f', '#ffeb3b']
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.8)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Third Row: Top Routes & Quick Insights
    c_bottom_left, c_bottom_right = st.columns([1, 1])
    
    with c_bottom_left:
        st.subheader("Top 10 Routes by Revenue")
        route_rev = sales_df.groupby('Route')['Gross_Fare_AED'].sum().reset_index()
        route_rev = route_rev.sort_values(by='Gross_Fare_AED', ascending=True).tail(10)
        
        fig = px.bar(
            route_rev,
            x='Gross_Fare_AED',
            y='Route',
            orientation='h',
            color='Gross_Fare_AED',
            color_continuous_scale='Blues',
            labels={'Gross_Fare_AED': 'Revenue (AED)', 'Route': 'Route'}
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_bottom_right:
        st.subheader("Data Highlights & Actionable Insights")
        
        # Calculate some data-driven findings
        top_route = sales_df.groupby('Route')['Gross_Fare_AED'].sum().idxmax()
        top_route_revenue = sales_df.groupby('Route')['Gross_Fare_AED'].sum().max()
        top_agent = sales_df.groupby('Agent_Name')['Gross_Fare_AED'].sum().idxmax()
        top_agent_revenue = sales_df.groupby('Agent_Name')['Gross_Fare_AED'].sum().max()
        
        st.markdown(f"""
        <div class='info-box'>
            <h4 style='color: #00b0ff; margin-top:0;'>💡 Network Sales Summary</h4>
            <ul>
                <li><b>Network Star Route:</b> The best-performing route is <b>{top_route}</b> generating a gross revenue of <b>AED {top_route_revenue:,.2f}</b> in the selected period.</li>
                <li><b>Leading Agent Channel:</b> <b>{top_agent}</b> is the largest sales contributor, attribution totals <b>AED {top_agent_revenue:,.2f}</b>.</li>
                <li><b>Billing Audit Health:</b> Acceptance rate stands at <span class='badge badge-success'>{billing_efficiency:.1f}%</span>, reflecting strong efficiency, but audit shows <span class='badge badge-danger'>{rejection_pct:.1f}%</span> in rejected amounts requiring settlement adjustment.</li>
                <li><b>Operational Capacity:</b> Flown load factor averaged <b>{weighted_load_factor:.2f}%</b>, signaling strong occupancy rates across primary active flight legs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Display monthly revenue comparison dataframe
        monthly_table = monthly_sales[['Period', 'Gross_Fare_AED', 'Net_Fare_AED']].copy()
        monthly_table['Gross_Fare_AED'] = monthly_table['Gross_Fare_AED'].map(lambda x: f"AED {x:,.2f}")
        monthly_table['Net_Fare_AED'] = monthly_table['Net_Fare_AED'].map(lambda x: f"AED {x:,.2f}")
        st.write("Monthly Breakdown Table:")
        st.dataframe(monthly_table, hide_index=True, use_container_width=True)

# ----------------- PAGE 2: REVENUE & ROUTES -----------------
elif page == "✈️ Revenue & Routes":
    st.title("Revenue & Route Analysis")
    st.markdown("Detailed breakdown of route-specific revenues, average fares, rankings, and side-by-side route performance comparison.")
    
    tab1, tab2 = st.tabs(["Route Performance Explorer", "Route Profitability Comparison"])
    
    with tab1:
        st.subheader("Route Financial Ledger & Profitability Rankings")
        
        # Visualizing rankings over time
        route_monthly = route_df.groupby(['Route', 'year', 'month_name'])['Revenue_AED'].sum().reset_index()
        route_monthly['month_num'] = route_monthly['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
        route_monthly = route_monthly.sort_values(by=['year', 'month_num', 'Revenue_AED'], ascending=[True, True, False])
        route_monthly['Rank'] = route_monthly.groupby(['year', 'month_num'])['Revenue_AED'].rank(ascending=False, method='first')
        
        # Display ranking movement for top 5 routes
        top_routes = route_df.groupby('Route')['Revenue_AED'].sum().nlargest(5).index.tolist()
        rank_trend_df = route_monthly[route_monthly['Route'].isin(top_routes)].copy()
        rank_trend_df['Period'] = rank_trend_df['month_name'] + " " + rank_trend_df['year'].astype(str)
        
        fig = px.line(
            rank_trend_df,
            x='Period',
            y='Rank',
            color='Route',
            markers=True,
            line_shape='linear',
            title='Monthly Revenue Ranking Trend (Top 5 Routes)',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(autorange='reverse', tickmode='linear', dtick=1, title="Revenue Rank"),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Ledger table
        st.subheader("Detailed Route Profitability Ledger")
        display_route_df = route_df.groupby('Route').agg({
            'Total_Tickets_Sold': 'sum',
            'Revenue_AED': 'sum',
            'Net_Revenue_AED': 'sum',
            'Total_Commission_AED': 'sum',
            'Total_Discount_AED': 'sum',
            'Total_Tax_AED': 'sum',
            'Passenger_Count': 'sum',
            'Total_Flights': 'sum',
            'Total_Seats_Available': 'sum'
        }).reset_index()
        
        # Derived calculations
        display_route_df['Avg_Fare_AED'] = (display_route_df['Revenue_AED'] / display_route_df['Total_Tickets_Sold']).round(2)
        display_route_df['Load_Factor_Pct'] = ((display_route_df['Passenger_Count'] * 100.0) / display_route_df['Total_Seats_Available']).round(2)
        display_route_df = display_route_df.sort_values(by='Revenue_AED', ascending=False)
        
        # Styling dataframe
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
            # Gather statistics
            stats_a = display_route_df[display_route_df['Route'] == route_a].iloc[0]
            stats_b = display_route_df[display_route_df['Route'] == route_b].iloc[0]
            
            comp_data = []
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
                    st.markdown(f"<div style='text-align: center; padding: 10px; font-weight: 500; border-bottom: 1px solid rgba(255,255,255,0.05);'>{label}</div>", unsafe_allow_html=True)
            
            with col_a:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #00b0ff; margin-bottom:10px;'>{route_a}</div>", unsafe_allow_html=True)
                for _, val_a, val_b, m_type in metrics_list:
                    is_better = val_a > val_b if "Load Factor" in label or val_a != 0 else val_a > val_b
                    color = "#00e676" if is_better else "rgba(255,255,255,0.8)"
                    
                    if m_type == 'currency':
                        disp = f"AED {val_a:,.2f}"
                    elif m_type == 'percentage':
                        disp = f"{val_a:.2f}%"
                    else:
                        disp = f"{val_a:,.0f}"
                        
                    st.markdown(f"<div style='text-align: center; padding: 10px; color: {color}; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600;'>{disp}</div>", unsafe_allow_html=True)
                    
            with col_b:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #2a9d8f; margin-bottom:10px;'>{route_b}</div>", unsafe_allow_html=True)
                for _, val_a, val_b, m_type in metrics_list:
                    is_better = val_b > val_a
                    color = "#00e676" if is_better else "rgba(255,255,255,0.8)"
                    
                    if m_type == 'currency':
                        disp = f"AED {val_b:,.2f}"
                    elif m_type == 'percentage':
                        disp = f"{val_b:.2f}%"
                    else:
                        disp = f"{val_b:,.0f}"
                        
                    st.markdown(f"<div style='text-align: center; padding: 10px; color: {color}; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600;'>{disp}</div>", unsafe_allow_html=True)

# ----------------- PAGE 3: OCCUPANCY & OPERATIONS -----------------
elif page == "📈 Occupancy & Operations":
    st.title("Occupancy & Operational Trends")
    st.markdown("Tracking flight load factors, flown capacity, weekend vs weekday traffic profiles, and scheduling efficiencies.")
    
    # Visual 1: Average Load Factor Trend
    st.subheader("Monthly Load Factor % Trend")
    monthly_occ = uplift_df.groupby(['year', 'month_name']).agg({
        'Passenger_Count': 'sum',
        'Total_Seats': 'sum'
    }).reset_index()
    monthly_occ['month_num'] = monthly_occ['month_name'].map(lambda m: month_order.index(m) if m in month_order else 0)
    monthly_occ = monthly_occ.sort_values(by=['year', 'month_num'])
    monthly_occ['Period'] = monthly_occ['month_name'] + " " + monthly_occ['year'].astype(str)
    monthly_occ['Avg_Load_Factor'] = (monthly_occ['Passenger_Count'] * 100.0) / monthly_occ['Total_Seats']
    
    fig = px.line(
        monthly_occ,
        x='Period',
        y='Avg_Load_Factor',
        markers=True,
        line_shape='spline',
        labels={'Avg_Load_Factor': 'Average Load Factor (%)'},
        color_discrete_sequence=['#2a9d8f']
    )
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[30, 100]),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Visual 2: Weekend vs Weekday analysis
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.subheader("Traffic Segment: Weekend vs Weekday")
        # Group by weekend/weekday and compute metrics
        weekend_df = uplift_df.groupby('is_weekend').agg({
            'Passenger_Count': 'sum',
            'Total_Seats': 'sum',
            'Flight_no': 'count'
        }).reset_index()
        weekend_df['Load_Factor_Pct'] = (weekend_df['Passenger_Count'] * 100.0) / weekend_df['Total_Seats']
        weekend_df['Day_Type'] = weekend_df['is_weekend'].map({True: 'Weekend Flights', False: 'Weekday Flights'})
        
        fig = px.bar(
            weekend_df,
            x='Day_Type',
            y='Load_Factor_Pct',
            color='Day_Type',
            text=weekend_df['Load_Factor_Pct'].map(lambda x: f"{x:.2f}%"),
            color_discrete_map={'Weekend Flights': '#ffeb3b', 'Weekday Flights': '#00b0ff'}
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title='Load Factor (%)', range=[0, 100], gridcolor='rgba(255,255,255,0.05)'),
            xaxis=dict(showgrid=False, title=''),
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_right:
        st.subheader("Capacity Utilization Matrix")
        # Scatter plot of Available Seats vs Passengers Flown by Route
        route_cap = uplift_df.groupby('Route').agg({
            'Total_Seats': 'sum',
            'Passenger_Count': 'sum',
            'Flight_no': 'count'
        }).reset_index()
        route_cap['Load_Factor'] = (route_cap['Passenger_Count'] * 100.0) / route_cap['Total_Seats']
        
        fig = px.scatter(
            route_cap,
            x='Total_Seats',
            y='Passenger_Count',
            size='Flight_no',
            color='Load_Factor',
            hover_name='Route',
            color_continuous_scale='Viridis',
            labels={'Total_Seats': 'Total Seats Offered', 'Passenger_Count': 'Total Flown Passengers', 'Load_Factor': 'Avg Load Factor (%)'}
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------- PAGE 4: AGENT PERFORMANCE -----------------
elif page == "👥 Agent Performance":
    st.title("Agent Sales Performance")
    st.markdown("Attribution of revenue and ticket sales to booking channels, agents, and commissions structure.")
    
    c_top_1, c_top_2 = st.columns([2, 1])
    
    with c_top_1:
        st.subheader("Agent Revenue Leaderboard")
        agent_rev = sales_df.groupby('Agent_Name').agg({
            'Gross_Fare_AED': 'sum',
            'Net_Fare_AED': 'sum',
            'Total_Tickets_Sold': 'sum',
            'Commission_Amount_AED': 'sum'
        }).reset_index().sort_values(by='Gross_Fare_AED', ascending=False)
        
        fig = px.bar(
            agent_rev.head(10),
            x='Gross_Fare_AED',
            y='Agent_Name',
            orientation='h',
            title='Top 10 Agents by Gross Sales (AED)',
            color='Gross_Fare_AED',
            color_continuous_scale='Tealgrn'
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_top_2:
        st.subheader("Channel Sales Split")
        channel_rev = sales_df.groupby('Agent_Location_Type')['Gross_Fare_AED'].sum().reset_index()
        channel_rev['Channel'] = channel_rev['Agent_Location_Type'].map({'GSA': 'General Sales Agent (GSA)', 'BSP': 'Billing & Settlement Plan (BSP)'})
        
        fig = px.pie(
            channel_rev,
            values='Gross_Fare_AED',
            names='Channel',
            hole=0.4,
            color_discrete_sequence=['#2a9d8f', '#e9c46a']
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader("Commission & Discount Distribution")
    # Comm / Discount rates
    agent_rev['Commission_Rate_Pct'] = (agent_rev['Commission_Amount_AED'] * 100.0) / agent_rev['Gross_Fare_AED']
    
    fig = px.scatter(
        agent_rev,
        x='Gross_Fare_AED',
        y='Commission_Amount_AED',
        size='Total_Tickets_Sold',
        color='Commission_Rate_Pct',
        hover_name='Agent_Name',
        color_continuous_scale='Plasma',
        labels={'Gross_Fare_AED': 'Gross Sales (AED)', 'Commission_Amount_AED': 'Commission Paid (AED)', 'Commission_Rate_Pct': 'Avg Comm Rate (%)'}
    )
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------- PAGE 5: GEOGRAPHIC SEGMENTATION -----------------
elif page == "🌍 Geographic Segmentation":
    st.title("Geographic Network Segmentation")
    st.markdown("Drill down into Region, Country, City, and Airport hierarchies to see where revenue is generated and passengers fly.")
    
    # Create the hierarchical data grouping
    geo_df = sales_df.copy()
    
    st.subheader("Interactive Revenue Tree Map (Region > Country > City)")
    # Group by hierarchy
    tree_df = geo_df.groupby(['Foreign_Region', 'Foreign_Country', 'Foreign_City', 'Foreign_Airport_Code']).agg({
        'Gross_Fare_AED': 'sum',
        'Total_Tickets_Sold': 'sum'
    }).reset_index()
    
    fig = px.treemap(
        tree_df,
        path=['Foreign_Region', 'Foreign_Country', 'Foreign_City', 'Foreign_Airport_Code'],
        values='Gross_Fare_AED',
        color='Gross_Fare_AED',
        color_continuous_scale='Blues',
        labels={'Gross_Fare_AED': 'Revenue (AED)'}
    )
    fig.update_layout(
        template='plotly_dark',
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Route Network Map visualization using coordinates
    st.subheader("Star Air Global Hub-and-Spoke Network Map")
    
    # Aggregate traffic for map lines
    network_traffic = uplift_df.groupby(['Origin_Airport_Code', 'Destination_Airport_Code', 'Foreign_Airport_Code', 'Foreign_City', 'Foreign_Country']).agg({
        'Passenger_Count': 'sum',
        'Flight_no': 'count'
    }).reset_index()
    
    # Plotting using Mapbox or Scattergeo
    fig = go.Figure()
    
    # 1. Add Airport Nodes
    airport_nodes = set(network_traffic['Origin_Airport_Code']).union(set(network_traffic['Destination_Airport_Code']))
    node_lats = []
    node_lons = []
    node_names = []
    node_sizes = []
    
    for apt in airport_nodes:
        if apt in AIRPORT_COORDS:
            lat, lon = AIRPORT_COORDS[apt]
            node_lats.append(lat)
            node_lons.append(lon)
            node_names.append(f"{apt} ({AIRPORT_GEOGRAPHY.get(apt, {}).get('City', 'Unknown')})")
            
            # Size node by its route activity
            activity = network_traffic[(network_traffic['Origin_Airport_Code'] == apt) | (network_traffic['Destination_Airport_Code'] == apt)]['Passenger_Count'].sum()
            node_sizes.append(max(6, min(20, int(activity / 1000))))
            
    fig.add_trace(go.Scattergeo(
        locationmode='ISO-3',
        lon=node_lons,
        lat=node_lats,
        text=node_names,
        mode='markers+text',
        textposition='top center',
        marker=dict(
            size=node_sizes,
            color='#00b0ff',
            line=dict(width=1, color='rgba(255,255,255,0.6)'),
            opacity=0.9
        ),
        name='Airports'
    ))
    
    # 2. Add Flight Path Lines
    for idx, row in network_traffic.iterrows():
        orig = row['Origin_Airport_Code']
        dest = row['Destination_Airport_Code']
        passengers = row['Passenger_Count']
        
        if orig in AIRPORT_COORDS and dest in AIRPORT_COORDS:
            lat_o, lon_o = AIRPORT_COORDS[orig]
            lat_d, lon_d = AIRPORT_COORDS[dest]
            
            fig.add_trace(go.Scattergeo(
                locationmode='ISO-3',
                lon=[lon_o, lon_d],
                lat=[lat_o, lat_d],
                mode='lines',
                line=dict(width=max(1, min(6, int(passengers / 2000))), color='rgba(0, 176, 255, 0.4)'),
                hoverinfo='none',
                showlegend=False
            ))
            
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            showland=True,
            landcolor='rgba(25, 35, 50, 1)',
            subunitcolor='rgba(255,255,255,0.1)',
            countrycolor='rgba(255,255,255,0.15)',
            showocean=True,
            oceancolor='rgba(10, 15, 25, 1)',
            projection_type='orthographic', # Cool globe view! Or change to 'equirectangular'
            showcountries=True,
            showlakes=True,
            lakecolor='rgba(10, 15, 25, 1)'
        ),
        margin=dict(l=0, r=0, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ----------------- PAGE 6: SETTLEMENT & BILLING AUDIT -----------------
elif page == "🔍 Settlement & Billing Audit":
    st.title("Interline Billing & Settlement Audit")
    st.markdown("Reconciling outward passenger billing, rejected claims, billing efficiencies, and settlement currency differences.")
    
    # Let's compute settlement metrics from billing_df
    # In billing_df, we have columns:
    # 'Billed_Amount', 'Commission_Amount', 'Billed_Discount', 'Accepted_Amount', 'Accepted_Commission', 'Accepted_Discount', 'Rejected_Amount', 'Rejected_Commission', 'Rejected_Discount', 'Rejection_Percentage', 'Billing_Efficiency_Pct'
    
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
            f"<div class='metric-header'>Settlement Gap</div>"
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
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=billing_monthly['Period'],
            y=billing_monthly['Efficiency_Rate'],
            mode='lines+markers',
            name='Billing Efficiency Pct',
            line=dict(color='#2a9d8f', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=billing_monthly['Period'],
            y=billing_monthly['Rejection_Rate'],
            mode='lines+markers',
            name='Rejection Rate Pct',
            line=dict(color='#ff1744', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Percentage (%)', range=[0, 100]),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_right:
        st.subheader("Billed Amount vs Accepted vs Rejected (AED)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=billing_monthly['Period'],
            y=billing_monthly['Billed_Amount'],
            name='Billed Amount',
            marker_color='#00b0ff'
        ))
        fig.add_trace(go.Bar(
            x=billing_monthly['Period'],
            y=billing_monthly['Accepted_Amount'],
            name='Accepted Amount',
            marker_color='#2a9d8f'
        ))
        fig.add_trace(go.Bar(
            x=billing_monthly['Period'],
            y=billing_monthly['Rejected_Amount'],
            name='Rejected Amount',
            marker_color='#ff1744'
        ))
        fig.update_layout(
            template='plotly_dark',
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='AED'),
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

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
    
    # Formatting
    styled_audit = audit_table.copy()
    styled_audit['Billed_Amount'] = styled_audit['Billed_Amount'].map(lambda x: f"AED {x:,.2f}")
    styled_audit['Accepted_Amount'] = styled_audit['Accepted_Amount'].map(lambda x: f"AED {x:,.2f}")
    styled_audit['Rejected_Amount'] = styled_audit['Rejected_Amount'].map(lambda x: f"AED {x:,.2f}")
    styled_audit['Settlement_Gap'] = styled_audit['Settlement_Gap'].map(lambda x: f"AED {x:,.2f}")
    styled_audit['Efficiency_Rate'] = styled_audit['Efficiency_Rate'].map(lambda x: f"{x:.2f}%")
    styled_audit['Ticket_Count'] = styled_audit['Ticket_Count'].map('{:,.0f}'.format)
    
    st.dataframe(styled_audit, hide_index=True, use_container_width=True)
