import pandas as pd
from data_loader import (
    load_route_profitability_data,
    load_uplift_data,
    load_billing_data,
    load_overall_revenue,
    load_settlement_reconciliation_data
)

def run_tests():
    print("Running Data Loader Health Checks...")
    
    try:
        routes = load_route_profitability_data()
        print(f"✅ Route Profitability Data Loaded successfully: {routes.shape} rows.")
    except Exception as e:
        print(f"❌ Route Profitability Data Load failed: {e}")
        return False

    try:
        uplift = load_uplift_data()
        print(f"✅ Uplift Data Loaded successfully: {uplift.shape} rows.")
        assert 'Foreign_Region' in uplift.columns, "Geographical mapping failed on uplift"
    except Exception as e:
        print(f"❌ Uplift Data Load failed: {e}")
        return False

    try:
        billing = load_billing_data()
        print(f"✅ Billing Data Loaded successfully: {billing.shape} rows.")
    except Exception as e:
        print(f"❌ Billing Data Load failed: {e}")
        return False

    try:
        overall = load_overall_revenue()
        print(f"✅ Overall Revenue (Aggregated) Loaded successfully: {overall.shape} rows.")
        assert 'Revenue_Per_Ticket_AED' in overall.columns, "Revenue_Per_Ticket_AED column missing"
        assert 'Ticket_Count' in overall.columns, "Ticket_Count column missing"
    except Exception as e:
        print(f"❌ Overall Revenue Load failed: {e}")
        return False

    try:
        settlement = load_settlement_reconciliation_data()
        print(f"✅ Settlement Reconciliation Loaded successfully: {settlement.shape} rows.")
        assert 'Settlement_Value' in settlement.columns, "Settlement_Value column missing"
        assert 'Billing_Value' in settlement.columns, "Billing_Value column missing"
    except Exception as e:
        print(f"❌ Settlement Reconciliation Load failed: {e}")
        return False

    print("\n🎉 All health checks passed successfully!")
    return True

if __name__ == "__main__":
    run_tests()


