import pandas as pd
import numpy as np
import os
import streamlit as st

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

# Loader Functions querying the database directly with caching (TTL = 10 mins)
@st.cache_data(ttl=600)
def load_sales_data():
    df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_sales_performance_team3")
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
    
    # Map geographical features
    df['Origin_City'] = df['Origin_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('City', 'Unknown'))
    df['Origin_Country'] = df['Origin_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Country', 'Unknown'))
    df['Origin_Region'] = df['Origin_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Region', 'Unknown'))
    
    df['Dest_City'] = df['Destination_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('City', 'Unknown'))
    df['Dest_Country'] = df['Destination_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Country', 'Unknown'))
    df['Dest_Region'] = df['Destination_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Region', 'Unknown'))
    
    df['Foreign_Airport_Code'] = np.where(df['Origin_Airport_Code'] == 'DXB', df['Destination_Airport_Code'], df['Origin_Airport_Code'])
    df['Foreign_City'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('City', 'Unknown'))
    df['Foreign_Country'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Country', 'Unknown'))
    df['Foreign_Region'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Region', 'Unknown'))
    return df

@st.cache_data(ttl=600)
def load_route_profitability_data():
    return query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_route_profitability_team3")

@st.cache_data(ttl=600)
def load_uplift_data():
    df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_uplift_summary_team3")
    df['Flight_Date'] = pd.to_datetime(df['Flight_Date'])
    
    df['Foreign_Airport_Code'] = np.where(df['Origin_Airport_Code'] == 'DXB', df['Destination_Airport_Code'], df['Origin_Airport_Code'])
    df['Foreign_City'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('City', 'Unknown'))
    df['Foreign_Country'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Country', 'Unknown'))
    df['Foreign_Region'] = df['Foreign_Airport_Code'].map(lambda x: AIRPORT_GEOGRAPHY.get(x, {}).get('Region', 'Unknown'))
    return df

@st.cache_data(ttl=600)
def load_billing_data():
    df = query_database("SELECT * FROM bootcamp_2026_simulation.gold.gold_inward_billing_team3")
    df['Billed_Date'] = pd.to_datetime(df['Billed_Date'])
    return df

@st.cache_data(ttl=600)
def load_date_dimension():
    df = query_database("SELECT * FROM bootcamp_2026_simulation.silver.dim_date_team3")
    df['full_date'] = pd.to_datetime(df['full_date'])
    return df
