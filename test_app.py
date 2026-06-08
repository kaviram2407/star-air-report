import unittest
import pandas as pd
import numpy as np
import os
import sys

# Ensure project root is in the path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from data_loader import (
    load_route_profitability_data,
    load_uplift_data,
    load_billing_data,
    load_overall_revenue,
    load_settlement_reconciliation_data,
    filter_dataframe
)


class TestDataLoaderHealthChecks(unittest.TestCase):
    """Health checks to verify CSV files are present and load correctly."""

    def test_load_route_profitability(self):
        try:
            df = load_route_profitability_data()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0, "Route profitability data is empty")
            required_cols = ['Route', 'Revenue_AED', 'Total_Flights', 'Passenger_Count']
            for col in required_cols:
                self.assertIn(col, df.columns, f"Missing required column: {col}")
        except Exception as e:
            self.fail(f"Route Profitability load failed: {e}")

    def test_load_uplift_summary(self):
        try:
            df = load_uplift_data()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0, "Uplift summary data is empty")
            self.assertIn('Foreign_Region', df.columns, "Geographical mapping failed on uplift")
        except Exception as e:
            self.fail(f"Uplift load failed: {e}")

    def test_load_inward_billing(self):
        try:
            df = load_billing_data()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0, "Billing data is empty")
            self.assertIn('Billed_Amount', df.columns, "Billed_Amount column missing")
        except Exception as e:
            self.fail(f"Billing data load failed: {e}")

    def test_load_overall_revenue(self):
        try:
            df = load_overall_revenue()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0, "Overall revenue data is empty")
            self.assertIn('Revenue_Per_Ticket_AED', df.columns, "Revenue_Per_Ticket_AED column missing")
            self.assertIn('Ticket_Count', df.columns, "Ticket_Count column missing")
        except Exception as e:
            self.fail(f"Overall revenue load failed: {e}")

    def test_load_settlement_reconciliation(self):
        try:
            df = load_settlement_reconciliation_data()
            self.assertIsNotNone(df)
            self.assertGreater(df.shape[0], 0, "Settlement reconciliation data is empty")
            self.assertIn('Settlement_Value', df.columns, "Settlement_Value column missing")
            self.assertIn('Billing_Value', df.columns, "Billing_Value column missing")
        except Exception as e:
            self.fail(f"Settlement reconciliation load failed: {e}")


class TestFilterDataframe(unittest.TestCase):
    """Unit tests for the filter_dataframe utility function."""

    def setUp(self):
        # Create a sample DataFrame to test filtering
        self.df = pd.DataFrame({
            'year': [2024, 2024, 2025, 2025, 2026],
            'month_name': ['January', 'February', 'January', 'March', 'January'],
            'value': [10, 20, 30, 40, 50]
        })

    def test_no_filters_applied(self):
        # When filters are empty or None, return original dataframe
        res1 = filter_dataframe(self.df, selected_years=[], selected_months=[])
        res2 = filter_dataframe(self.df, selected_years=None, selected_months=None)
        
        self.assertEqual(res1.shape[0], 5)
        self.assertEqual(res2.shape[0], 5)

    def test_filter_by_single_year(self):
        res = filter_dataframe(self.df, selected_years=[2024])
        self.assertEqual(res.shape[0], 2)
        self.assertTrue((res['year'] == 2024).all())

    def test_filter_by_multiple_years(self):
        res = filter_dataframe(self.df, selected_years=[2024, 2025])
        self.assertEqual(res.shape[0], 4)
        self.assertTrue(res['year'].isin([2024, 2025]).all())

    def test_filter_by_single_month(self):
        res = filter_dataframe(self.df, selected_months=['January'])
        self.assertEqual(res.shape[0], 3)
        self.assertTrue((res['month_name'] == 'January').all())

    def test_filter_by_multiple_months(self):
        res = filter_dataframe(self.df, selected_months=['January', 'February'])
        self.assertEqual(res.shape[0], 4)
        self.assertTrue(res['month_name'].isin(['January', 'February']).all())

    def test_filter_by_both_year_and_month(self):
        res = filter_dataframe(self.df, selected_years=[2024], selected_months=['January'])
        self.assertEqual(res.shape[0], 1)
        self.assertEqual(res.iloc[0]['value'], 10)


class TestKPICalculations(unittest.TestCase):
    """Tests verify core business mathematical formulas."""

    def test_load_factor_calculation(self):
        # Load Factor = (Passengers * 100) / Seats
        def calc_load_factor(passengers, seats):
            return (passengers * 100.0) / seats if seats > 0 else 0

        # Normal case
        self.assertEqual(calc_load_factor(75, 100), 75.0)
        self.assertAlmostEqual(calc_load_factor(120, 150), 80.0)
        # Empty/Edge cases
        self.assertEqual(calc_load_factor(0, 100), 0.0)
        self.assertEqual(calc_load_factor(50, 0), 0.0)

    def test_billing_efficiency_calculation(self):
        # Billing Efficiency = (Accepted * 100) / Billed
        def calc_billing_eff(accepted, billed):
            return (accepted * 100.0) / billed if billed > 0 else 0

        # Normal case
        self.assertEqual(calc_billing_eff(90, 100), 90.0)
        # Edge cases
        self.assertEqual(calc_billing_eff(0, 100), 0.0)
        self.assertEqual(calc_billing_eff(10, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
