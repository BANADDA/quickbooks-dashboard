import pandas as pd
from datetime import datetime, timedelta
import os

from quickbooks_extractor import (
    extract_invoices, 
    extract_customers, 
    extract_items, 
    extract_accounts,
    get_auth_client,
    get_quickbooks_client
)

from data_processor import (
    clean_invoice_data,
    create_time_aggregations,
    create_customer_insights,
    create_product_insights,
    calculate_aging_summary
)

from database import (
    create_database,
    store_dataframe
)

def run_pipeline(use_api=False, start_date=None, end_date=None):
    """Run the complete QuickBooks data pipeline"""
    print("Starting QuickBooks data pipeline...")
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        # Default to 6 months of data
        start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    
    print(f"Processing data from {start_date} to {end_date}")
    
    # 1. Extract data
    if use_api:
        print("Extracting data from QuickBooks API...")
        # Setup QuickBooks client (uncomment when ready to use API)
        # auth_client = get_auth_client()
        # client = get_quickbooks_client(
        #     auth_client=auth_client,
        #     refresh_token="YOUR_REFRESH_TOKEN",
        #     company_id="YOUR_COMPANY_ID"
        # )
        client = None  # Remove this line when using the API
        
        invoices_df = extract_invoices(start_date, end_date, client)
        customers_df = extract_customers(client)
        items_df = extract_items(client)
        accounts_df = extract_accounts(client)
    else:
        print("Importing data from CSV exports...")
        invoices_df = extract_invoices(start_date, end_date)
        customers_df = extract_customers()
        items_df = extract_items()
        accounts_df = extract_accounts()
    
    print(f"Extracted {len(invoices_df)} invoice line items")
    print(f"Extracted {len(customers_df)} customers")
    print(f"Extracted {len(items_df)} items/products")
    print(f"Extracted {len(accounts_df)} accounts")
    
    # 2. Process data
    print("Processing data...")
    clean_invoices = clean_invoice_data(invoices_df)
    daily_sales, monthly_sales, dow_sales = create_time_aggregations(clean_invoices)
    customer_sales = create_customer_insights(clean_invoices, customers_df)
    product_sales = create_product_insights(clean_invoices, items_df)
    aging_summary = calculate_aging_summary(clean_invoices)
    
    # 3. Store processed data
    print("Storing data in database...")
    create_database()
    store_dataframe(clean_invoices, 'invoices')
    store_dataframe(customers_df, 'customers')
    store_dataframe(items_df, 'items')
    store_dataframe(accounts_df, 'accounts')
    store_dataframe(daily_sales, 'daily_sales')
    store_dataframe(customer_sales, 'customer_insights')
    store_dataframe(product_sales, 'product_insights')
    store_dataframe(aging_summary, 'aging_summary')
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    # Run with API extraction (set to False by default)
    # run_pipeline(use_api=True)
    
    # Run with CSV imports (if API access is not available)
    run_pipeline(use_api=False)