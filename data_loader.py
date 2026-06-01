import pandas as pd
import numpy as np
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Coordinates of airports for the map
AIRPORT_COORDS = {
    'ADD': (9.03, 38.74), 'AKL': (-37.00, 174.79), 'BHX': (52.45, -1.74), 'BKK': (13.68, 100.75),
    'BNE': (-27.38, 153.11), 'BOM': (19.09, 72.87), 'CCU': (22.65, 88.45), 'CDG': (49.01, 2.55),
    'CHC': (-43.49, 172.53), 'CMB': (7.18, 79.88), 'COK': (10.15, 76.40), 'CPT': (-33.97, 18.60),
    'DEL': (28.56, 77.10), 'DFW': (32.90, -97.04), 'DUB': (53.43, -6.27), 'DXB': (25.25, 55.36),
    'FRA': (50.03, 8.57), 'GVA': (46.24, 6.11), 'HAN': (21.22, 105.81), 'HYD': (17.24, 78.43),
    'IAH': (29.98, -95.34), 'JFK': (40.64, -73.78), 'JNB': (-26.13, 28.24), 'KHI': (24.91, 67.16),
    'KUL': (2.75, 101.71), 'LGW': (51.15, -0.19), 'LHE': (31.52, 74.40), 'LHR': (51.47, -0.45),
    'MAA': (12.99, 80.18), 'MEL': (-37.67, 144.84), 'MIL': (45.63, 8.73), 'MRU': (-20.43, 57.68),
    'MUC': (48.35, 11.79), 'ORD': (41.98, -87.90), 'PEW': (33.99, 71.51), 'SIN': (1.36, 103.99),
    'SVO': (55.97, 37.41), 'SYD': (-33.95, 151.18), 'YUL': (45.47, -73.74), 'YYZ': (43.68, -79.62),
    'ZRH': (47.46, 8.55)
}

# Geographic metadata for airports
AIRPORT_GEOGRAPHY = {
    'ADD': {'City': 'Addis Ababa', 'Country': 'Ethiopia', 'Region': 'Africa'},
    'AKL': {'City': 'Auckland', 'Country': 'New Zealand', 'Region': 'Oceania'},
    'BHX': {'City': 'Birmingham', 'Country': 'United Kingdom', 'Region': 'Europe'},
    'BKK': {'City': 'Bangkok', 'Country': 'Thailand', 'Region': 'Asia'},
    'BNE': {'City': 'Brisbane', 'Country': 'Australia', 'Region': 'Oceania'},
    'BOM': {'City': 'Mumbai', 'Country': 'India', 'Region': 'Asia'},
    'CCU': {'City': 'Kolkata', 'Country': 'India', 'Region': 'Asia'},
    'CDG': {'City': 'Paris', 'Country': 'France', 'Region': 'Europe'},
    'CHC': {'City': 'Christchurch', 'Country': 'New Zealand', 'Region': 'Oceania'},
    'CMB': {'City': 'Colombo', 'Country': 'Sri Lanka', 'Region': 'Asia'},
    'COK': {'City': 'Kochi', 'Country': 'India', 'Region': 'Asia'},
    'CPT': {'City': 'Cape Town', 'Country': 'South Africa', 'Region': 'Africa'},
    'DEL': {'City': 'Delhi', 'Country': 'India', 'Region': 'Asia'},
    'DFW': {'City': 'Dallas', 'Country': 'United States', 'Region': 'North America'},
    'DUB': {'City': 'Dublin', 'Country': 'Ireland', 'Region': 'Europe'},
    'DXB': {'City': 'Dubai', 'Country': 'United Arab Emirates', 'Region': 'Middle East'},
    'FRA': {'City': 'Frankfurt', 'Country': 'Germany', 'Region': 'Europe'},
    'GVA': {'City': 'Geneva', 'Country': 'Switzerland', 'Region': 'Europe'},
    'HAN': {'City': 'Hanoi', 'Country': 'Vietnam', 'Region': 'Asia'},
    'HYD': {'City': 'Hyderabad', 'Country': 'India', 'Region': 'Asia'},
    'IAH': {'City': 'Houston', 'Country': 'United States', 'Region': 'North America'},
    'JFK': {'City': 'New York', 'Country': 'United States', 'Region': 'North America'},
    'JNB': {'City': 'Johannesburg', 'Country': 'South Africa', 'Region': 'Africa'},
    'KHI': {'City': 'Karachi', 'Country': 'Pakistan', 'Region': 'Asia'},
    'KUL': {'City': 'Kuala Lumpur', 'Country': 'Malaysia', 'Region': 'Asia'},
    'LGW': {'City': 'London', 'Country': 'United Kingdom', 'Region': 'Europe'},
    'LHE': {'City': 'Lahore', 'Country': 'Pakistan', 'Region': 'Asia'},
    'LHR': {'City': 'London', 'Country': 'United Kingdom', 'Region': 'Europe'},
    'MAA': {'City': 'Chennai', 'Country': 'India', 'Region': 'Asia'},
    'MEL': {'City': 'Melbourne', 'Country': 'Australia', 'Region': 'Oceania'},
    'MIL': {'City': 'Milan', 'Country': 'Italy', 'Region': 'Europe'},
    'MRU': {'City': 'Mauritius', 'Country': 'Mauritius', 'Region': 'Africa'},
    'MUC': {'City': 'Munich', 'Country': 'Germany', 'Region': 'Europe'},
    'ORD': {'City': 'Chicago', 'Country': 'United States', 'Region': 'North America'},
    'PEW': {'City': 'Peshawar', 'Country': 'Pakistan', 'Region': 'Asia'},
    'SIN': {'City': 'Singapore', 'Country': 'Singapore', 'Region': 'Asia'},
    'SVO': {'City': 'Moscow', 'Country': 'Russia', 'Region': 'Europe'},
    'SYD': {'City': 'Sydney', 'Country': 'Australia', 'Region': 'Oceania'},
    'YUL': {'City': 'Montreal', 'Country': 'Canada', 'Region': 'North America'},
    'YYZ': {'City': 'Toronto', 'Country': 'Canada', 'Region': 'North America'},
    'ZRH': {'City': 'Zurich', 'Country': 'Switzerland', 'Region': 'Europe'}
}

def get_secret(name):
    """Retrieve secret from Streamlit Secrets, Session State, or Environment Variables"""
    # 1. Check Session State (entered dynamically in UI)
    if "db_credentials" in st.session_state and name in st.session_state["db_credentials"]:
        return st.session_state["db_credentials"][name]
    
    # 2. Check Streamlit Secrets (configured in hosting cloud settings)
    try:
        if hasattr(st, "secrets") and name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
        
    # 3. Check Environment Variables (configured in local env)
    return os.getenv(name)

def get_active_connection_details():
    """Detect configured credentials and return dict containing type and keys"""
    # Try Databricks
    db_host = get_secret("DATABRICKS_SERVER_HOSTNAME")
    db_path = get_secret("DATABRICKS_HTTP_PATH")
    db_token = get_secret("DATABRICKS_ACCESS_TOKEN")
    
    if db_host and db_path and db_token:
        return {
            "type": "databricks",
            "host": db_host,
            "path": db_path,
            "token": db_token
        }
        
    # Try Snowflake
    sf_user = get_secret("SNOWFLAKE_USER")
    sf_pwd = get_secret("SNOWFLAKE_PASSWORD")
    sf_acct = get_secret("SNOWFLAKE_ACCOUNT")
    sf_wh = get_secret("SNOWFLAKE_WAREHOUSE")
    sf_db = get_secret("SNOWFLAKE_DATABASE")
    sf_sch = get_secret("SNOWFLAKE_SCHEMA") or "GOLD"
    
    if sf_user and sf_pwd and sf_acct and sf_wh and sf_db:
        return {
            "type": "snowflake",
            "user": sf_user,
            "password": sf_pwd,
            "account": sf_acct,
            "warehouse": sf_wh,
            "database": sf_db,
            "schema": sf_sch
        }
        
    return None

def query_database(query):
    """Execute a query against Databricks or Snowflake dynamically based on configured credentials"""
    creds = get_active_connection_details()
    if not creds:
        raise ValueError("Missing database credentials.")
        
    if creds["type"] == "databricks":
        from databricks import sql
        with sql.connect(
            server_hostname=creds["host"],
            http_path=creds["path"],
            access_token=creds["token"]
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(result, columns=columns)
                
    elif creds["type"] == "snowflake":
        import snowflake.connector
        ctx = snowflake.connector.connect(
            user=creds["user"],
            password=creds["password"],
            account=creds["account"],
            warehouse=creds["warehouse"],
            database=creds["database"],
            schema=creds["schema"]
        )
        cs = ctx.cursor()
        try:
            cs.execute(query)
            result = cs.fetchall()
            columns = [desc[0] for desc in cs.description]
            return pd.DataFrame(result, columns=columns)
        finally:
            cs.close()
            ctx.close()

# Helper to locate local CSV files
def check_local_csv(filename):
    # Check project root directory first
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        return path
    # Check extracted_data directory next
    path_ext = os.path.join(BASE_DIR, "extracted_data", filename)
    if os.path.exists(path_ext):
        return path_ext
    # Fallback to case-insensitive checks in both directories
    search_dirs = [BASE_DIR, os.path.join(BASE_DIR, "extracted_data")]
    for d in search_dirs:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower() == filename.lower():
                    return os.path.join(d, f)
    return None

# Loader Functions querying the database directly with caching, falling back to local CSVs
@st.cache_data(ttl=600)
def load_route_profitability_data():
    try:
        df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_route_profitability_IN1725")
        print("Loaded route profitability from Databricks/Snowflake SQL Warehouse.")
        return df
    except Exception as e:
        path = check_local_csv("gold_flight_class_occupancy_IN1725.csv")
        if path:
            print("Offline Mode: Aggregating route profitability from local occupancy CSV.")
            df_occ = pd.read_csv(path)
            groupby_cols = ['Route', 'Carrier_Name', 'Carrier_Code', 'month_name', 'quarter_label', 'year']
            agg_df = df_occ.groupby(groupby_cols).agg({
                'Starair_Tickets_Sold': 'sum',
                'Starair_Revenue_AED': 'sum',
                'Starair_Net_Revenue_AED': 'sum',
                'Starair_Commission_AED': 'sum',
                'Starair_Discount_AED': 'sum',
                'Starair_Tax_AED': 'sum',
                'Passenger_Count': 'sum',
                'Total_Seats': 'sum'
            }).reset_index()
            
            flight_counts = df_occ.groupby(groupby_cols)['Flight_no'].count().reset_index()
            agg_df = agg_df.merge(flight_counts, on=groupby_cols)
            
            agg_df.rename(columns={
                'Starair_Tickets_Sold': 'Total_Tickets_Sold',
                'Starair_Revenue_AED': 'Revenue_AED',
                'Starair_Net_Revenue_AED': 'Net_Revenue_AED',
                'Starair_Commission_AED': 'Total_Commission_AED',
                'Starair_Discount_AED': 'Total_Discount_AED',
                'Starair_Tax_AED': 'Total_Tax_AED',
                'Total_Seats': 'Total_Seats_Available',
                'Flight_no': 'Total_Flights'
            }, inplace=True)
            
            agg_df['month_num'] = agg_df['month_name'].map(lambda m: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(m) + 1 if m in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] else 1)
            agg_df['Avg_Fare_AED'] = (agg_df['Revenue_AED'] / agg_df['Total_Tickets_Sold']).round(2)
            agg_df['Revenue_Per_Passenger_AED'] = (agg_df['Revenue_AED'] / agg_df['Passenger_Count']).round(2)
            agg_df['Load_Factor_Pct'] = ((agg_df['Passenger_Count'] * 100.0) / agg_df['Total_Seats_Available']).round(2)
            return agg_df
        else:
            raise RuntimeError(f"Database query failed and local CSV not found. Error: {e}")

@st.cache_data(ttl=600)
def load_uplift_data():
    try:
        df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_uplift_summary_IN1725")
        print("Loaded uplift summary from Databricks/Snowflake SQL Warehouse.")
    except Exception as e:
        path = check_local_csv("gold_flight_class_occupancy_IN1725.csv")
        if path:
            print("Offline Mode: Extracting uplift summary from local occupancy CSV.")
            df = pd.read_csv(path)
            df['Origin_Airport_Code'] = df['Route'].apply(lambda r: str(r).split('-')[0] if '-' in str(r) else '')
            df['Destination_Airport_Code'] = df['Route'].apply(lambda r: str(r).split('-')[1] if '-' in str(r) else '')
            df['day_of_week'] = pd.to_datetime(df['Flight_Date']).dt.day_name()
            df['is_weekend'] = pd.to_datetime(df['Flight_Date']).dt.dayofweek.isin([5, 6])
        else:
            raise RuntimeError(f"Database query failed and local CSV not found. Error: {e}")
            
    df['Flight_Date'] = pd.to_datetime(df['Flight_Date'])
    
    df['Foreign_Airport_Code'] = np.where(df['Origin_Airport_Code'] == 'DXB', df['Destination_Airport_Code'], df['Origin_Airport_Code'])
    df['Foreign_City'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('City', 'Unknown'))
    df['Foreign_Country'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Country', 'Unknown'))
    df['Foreign_Region'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Region', 'Unknown'))
    return df

@st.cache_data(ttl=600)
def load_billing_data():
    try:
        df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_inward_billing_IN1725")
        print("Loaded inward billing from Databricks/Snowflake SQL Warehouse.")
    except Exception as e:
        path = check_local_csv("gold_inward_billing_in1725.csv")
        if path:
            print("Offline Mode: Loaded inward billing from local CSV file.")
            df = pd.read_csv(path)
        else:
            raise RuntimeError(f"Database query failed and local CSV not found. Error: {e}")
            
    df['Billed_Date'] = pd.to_datetime(df['Billed_Date'])
    return df

@st.cache_data(ttl=600)
def load_overall_revenue():
    try:
        df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_overall_revenue_IN1725")
        print("Loaded overall revenue from Databricks/Snowflake SQL Warehouse.")
    except Exception as e:
        path = check_local_csv("gold_overall_revenue_in1725.csv")
        if path:
            print("Offline Mode: Loading and pre-aggregating overall revenue from local CSV file...")
            df = pd.read_csv(path)
        else:
            raise RuntimeError(f"Database query failed and local CSV not found. Error: {e}")
            
    # Perform pre-aggregation to save memory and CPU inside streamlit
    groupby_cols = ['Revenue_Date', 'month_name', 'month_num', 'quarter_label', 'year', 'Carrier_Code', 'Route', 'Inward_Available_Flag']
    
    # Ensure columns exist, fillna where necessary
    numeric_cols = [
        'Ticket_Amount_AED', 'Tax_AED', 'Agent_Commission_AED', 'Discount_AED', 
        'Inward_Billed_Amount', 'Inward_Commission_Received', 'Revenue_Per_Ticket_AED'
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
            
    agg_df = df.groupby(groupby_cols).agg({
        'Ticket_Amount_AED': 'sum',
        'Tax_AED': 'sum',
        'Agent_Commission_AED': 'sum',
        'Discount_AED': 'sum',
        'Inward_Billed_Amount': 'sum',
        'Inward_Commission_Received': 'sum',
        'Revenue_Per_Ticket_AED': 'sum',
        'Ticket_Number': 'count' if 'Ticket_Number' in df.columns else 'size'
    }).reset_index()
    
    agg_df.rename(columns={'Ticket_Number': 'Ticket_Count'}, inplace=True)
    
    # Convert dates
    agg_df['Revenue_Date'] = pd.to_datetime(agg_df['Revenue_Date'])
    
    return agg_df

@st.cache_data(ttl=600)
def load_settlement_reconciliation_data():
    try:
        df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_settlement_reconciliation_IN1725")
        print("Loaded settlement reconciliation from Databricks/Snowflake SQL Warehouse.")
    except Exception as e:
        path = check_local_csv("gold_settlement_reconciliation_in1725.csv")
        if path:
            print("Offline Mode: Loaded settlement reconciliation from local CSV.")
            df = pd.read_csv(path)
        else:
            raise RuntimeError(f"Database query failed and local CSV not found. Error: {e}")
            
    df['Settlement_Date'] = pd.to_datetime(df['Settlement_Date'])
    return df


