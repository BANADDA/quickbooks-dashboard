import pandas as pd
import numpy as np

def clean_invoice_data(df):
    """Clean and transform invoice data"""
    # Handle missing values
    df = df.fillna({
        'customer_id': 'unknown',
        'item_id': 'unknown',
        'quantity': 0,
        'unit_price': 0,
        'amount': 0
    })
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create derived fields
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    
    # Flag for paid status (example logic)
    df['is_paid'] = np.where(df['status'] == 'Paid', 1, 0)
    
    return df

def create_time_aggregations(invoice_df):
    """Create time-based aggregations"""
    # Daily aggregation
    daily_sales = invoice_df.groupby('date')['amount'].sum().reset_index()
    daily_sales.columns = ['date', 'daily_sales']
    
    # Monthly aggregation
    monthly_sales = invoice_df.groupby(['year', 'month'])['amount'].sum().reset_index()
    monthly_sales.columns = ['year', 'month', 'monthly_sales']
    
    # Day of week aggregation
    dow_sales = invoice_df.groupby('day_of_week')['amount'].sum().reset_index()
    dow_sales.columns = ['day_of_week', 'dow_sales']
    
    return daily_sales, monthly_sales, dow_sales

def create_customer_insights(invoice_df, customer_df):
    """Create customer insights"""
    # Merge customer information
    df = pd.merge(invoice_df, customer_df, on='customer_id', how='left')
    
    # Customer total sales
    customer_sales = df.groupby('customer_id')['amount'].agg(['sum', 'count']).reset_index()
    customer_sales.columns = ['customer_id', 'total_sales', 'transaction_count']
    
    # Add customer name
    customer_sales = pd.merge(customer_sales, customer_df[['customer_id', 'name']], 
                             on='customer_id', how='left')
    
    # Calculate average order value
    customer_sales['avg_order_value'] = customer_sales['total_sales'] / customer_sales['transaction_count']
    
    return customer_sales

def create_product_insights(invoice_df, item_df):
    """Create product insights"""
    # Merge product information
    df = pd.merge(invoice_df, item_df, on='item_id', how='left')
    
    # Product sales analytics
    product_sales = df.groupby('item_id').agg({
        'amount': 'sum',
        'quantity': 'sum',
        'invoice_id': 'count'
    }).reset_index()
    
    product_sales.columns = ['item_id', 'total_sales', 'total_quantity', 'order_count']
    
    # Add product name
    product_sales = pd.merge(product_sales, item_df[['item_id', 'name']], 
                            on='item_id', how='left')
    
    return product_sales

def calculate_aging_summary(invoice_df, as_of_date=None):
    """Calculate accounts receivable aging"""
    if as_of_date is None:
        as_of_date = pd.Timestamp.now().date()
    else:
        as_of_date = pd.to_datetime(as_of_date).date()
    
    # Filter unpaid invoices
    unpaid = invoice_df[invoice_df['is_paid'] == 0].copy()
    
    # Calculate days outstanding
    unpaid['date'] = pd.to_datetime(unpaid['date']).dt.date
    unpaid['days_outstanding'] = [(as_of_date - date).days for date in unpaid['date']]
    
    # Categorize into aging buckets
    conditions = [
        (unpaid['days_outstanding'] <= 30),
        (unpaid['days_outstanding'] > 30) & (unpaid['days_outstanding'] <= 60),
        (unpaid['days_outstanding'] > 60) & (unpaid['days_outstanding'] <= 90),
        (unpaid['days_outstanding'] > 90)
    ]
    
    buckets = ['Current', '31-60 Days', '61-90 Days', '90+ Days']
    unpaid['aging_bucket'] = np.select(conditions, buckets, default='Current')
    
    # Aggregate by bucket
    aging_summary = unpaid.groupby('aging_bucket')['amount'].sum().reset_index()
    
    return aging_summary