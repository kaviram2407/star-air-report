# ✈️ Star Air BI Portal

A premium Business Intelligence Portal designed for Star Air, built with Python, Streamlit, and Plotly. The dashboard integrates with Databricks SQL Warehouse and Snowflake Data Warehouse to display key metrics, route capacity analysis, and inward billing reconciliations.

---

## 🚀 Key Features

*   **📊 KPI Dashboard:** Live financial ledger summaries tracking Gross Ticket Sales, Realized Net Revenue, Flown Passengers, and Overall Billing Efficiency. Includes a monthly revenue trend line and a waterfall funnel analysis of margin leakages (commissions, taxes, and agent discounts).
*   **✈️ Route Performance & Capacity:** Interactive route ranking, seat availability tracking, load factor trends, and a geospatial route map displaying network flows.
*   **🔍 Inward Billing Audit:** Dedicated dashboard module to audit interline invoices, identify billed mismatches, trace dispute reasons, and reconcile settlements.
*   **🔄 Cloud Data Sync:** Integrates directly with Snowflake and Databricks. Data can be refreshed on-demand from database views to local CSV cache.
*   **🌓 Adaptive UI:** Features a dynamic theme mode switcher in the sidebar (System Default, Dark, Light) with a custom CSS design system.

---

## 🛠️ Getting Started (Local Development)

### 1. Setup Environment & Install Dependencies

Ensure you have Python 3.8+ installed. Navigate to the project root and run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

The application can load credentials in three ways (in order of priority):
1.  **Direct UI Input:** If no credentials are found, the app prompts you on the startup page to enter credentials.
2.  **Environment Variables / `.env`:** Copy `.env.example` to `.env` and fill in your cloud database credentials.
3.  **Streamlit Secrets:** Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and populate it.

#### 📴 Offline Mode (No DB Connection Required)
If no credentials are provided and local CSV data files are present in the workspace directory (e.g., `gold_overall_revenue_in1725.csv`), the application **automatically enters Offline Mode**. It will load and aggregate data from the cached CSV files seamlessly.

### 3. Run the Dashboard

To launch the Streamlit server locally, execute:

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`.

---

## 🔄 Cloud Data Synchronization

To pull the latest tables from your cloud data warehouses and overwrite the local CSV cache:

### Via command line:
```bash
# Sync from Databricks SQL Warehouse
python data_injector.py --source databricks

# Sync from Snowflake
python data_injector.py --source snowflake
```

### Via the App UI:
Use the **🔄 Data Sync Panel** in the sidebar:
1. Select your target source (**Databricks** or **Snowflake**).
2. Click **Trigger Cloud Fetch**.

---

## ☁️ Hosting on Streamlit Community Cloud

Deploying your app to Streamlit Community Cloud is free and can be set up in a few minutes directly from GitHub.

### Step 1: Push Project to GitHub
1. Create a new repository on [GitHub](https://github.com).
2. Initialize git and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Configure project for Streamlit hosting"
   ```
   > [!NOTE]
   > The large file `gold_sales_performance_in1725.csv` (218MB) is automatically ignored in `.gitignore` so you do not exceed GitHub's 100MB file limit. The dashboard relies on smaller, pre-aggregated CSVs for offline fallback, which will be pushed and hosted successfully.

3. Push the files to your GitHub repository:
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click the **"New app"** button.
3. Select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **"Advanced settings..."** before deploying.
5. In the **Secrets** section, copy and paste the credentials template from `.streamlit/secrets.toml.example` and fill in your production credentials.
6. Click **"Save"** and then **"Deploy!"**.

Streamlit Cloud will provision the container, install the packages listed in `requirements.txt`, configure the environment variables from your secrets, and launch the portal.

---

## 📁 Workspace Structure

```
├── .streamlit/
│   ├── config.toml           # Streamlit UI theme and server settings
│   └── secrets.toml.example  # Configuration template for cloud databases
├── app.py                    # Main Streamlit application file
├── data_loader.py            # Logic to query databases (with fallback to local CSVs)
├── data_injector.py          # Data ingestion script to sync views to local CSVs
├── requirements.txt          # Python package dependencies
├── .gitignore                # Git ignore configuration
└── gold_*.csv                # Cached datasets for offline mode execution
```
