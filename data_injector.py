import os
import argparse
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Queries mapping to the predefined Gold views and Date dimension
QUERIES = {
    "gold_9_cell_9.csv": "SELECT * FROM bootcamp_2026_simulation.gold.gold_sales_performance_team3",
    "gold_2_cell_3.csv": "SELECT * FROM bootcamp_2026_simulation.gold.gold_route_profitability_team3",
    "gold_4_cell_4.csv": "SELECT * FROM bootcamp_2026_simulation.gold.gold_uplift_summary_team3",
    "gold_8_cell_8.csv": "SELECT * FROM bootcamp_2026_simulation.gold.gold_inward_billing_team3",
    "silver_3_cell_3.csv": "SELECT * FROM bootcamp_2026_simulation.silver.dim_date_team3"
}

# Use relative paths so it works both locally and when deployed/hosted on Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "extracted_data")

def get_secret(name, default=None):
    """Retrieve secret from Streamlit Secrets or Environment Variables"""
    try:
        # Check Streamlit secrets first (used when hosted on Streamlit Cloud)
        if hasattr(st, "secrets") and name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    # Fallback to standard environment variables
    return os.getenv(name, default)

def connect_databricks():
    """Connect to Databricks SQL Warehouse and return connection object"""
    try:
        from databricks import sql
    except ImportError:
        raise ImportError(
            "databricks-sql-connector is missing. Install it using:\n"
            "pip install databricks-sql-connector"
        )
    
    server_hostname = get_secret("DATABRICKS_SERVER_HOSTNAME")
    http_path = get_secret("DATABRICKS_HTTP_PATH")
    access_token = get_secret("DATABRICKS_ACCESS_TOKEN")
    
    if not (server_hostname and http_path and access_token):
        raise ValueError(
            "Missing Databricks connection credentials. Ensure you configure:\n"
            "DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, and DATABRICKS_ACCESS_TOKEN"
        )
        
    return sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    )

def connect_snowflake():
    """Connect to Snowflake and return connection object"""
    try:
        import snowflake.connector
    except ImportError:
        raise ImportError(
            "snowflake-connector-python is missing. Install it using:\n"
            "pip install snowflake-connector-python"
        )
        
    user = get_secret("SNOWFLAKE_USER")
    password = get_secret("SNOWFLAKE_PASSWORD")
    account = get_secret("SNOWFLAKE_ACCOUNT")
    warehouse = get_secret("SNOWFLAKE_WAREHOUSE")
    database = get_secret("SNOWFLAKE_DATABASE")
    schema = get_secret("SNOWFLAKE_SCHEMA", "GOLD")
    
    if not (user and password and account and warehouse and database):
        raise ValueError(
            "Missing Snowflake credentials. Ensure you configure:\n"
            "SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE"
        )
        
    return snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

def run_sync(source="databricks"):
    """Fetch views from cloud database and save them as local CSV files"""
    print(f"Starting Data Sync from {source.upper()}...")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    conn = None
    try:
        if source == "databricks":
            conn = connect_databricks()
        elif source == "snowflake":
            conn = connect_snowflake()
        else:
            raise ValueError(f"Unknown data source: {source}")
            
        cursor = conn.cursor()
        
        for filename, query in QUERIES.items():
            print(f"Syncing query for {filename}...")
            cursor.execute(query)
            result = cursor.fetchall()
            
            # Extract column headers
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            
            # Save to target CSV directory
            output_path = os.path.join(DATA_DIR, filename)
            df.to_csv(output_path, index=False)
            print(f"   Successfully wrote {len(df):,} rows to {output_path}")
            
        print("🎉 Sync completed successfully!")
        return True, "Data successfully sync'd from source."
        
    except Exception as e:
        err_msg = f"❌ Sync failed: {e}"
        print(err_msg)
        return False, err_msg
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Star Air BI Data Injector")
    parser.add_argument(
        "--source", 
        choices=["databricks", "snowflake"], 
        default="databricks",
        help="Specify the target source database (databricks or snowflake)"
    )
    args = parser.parse_args()
    run_sync(source=args.source)
