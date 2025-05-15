import json

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

from database import execute_query

app = Flask(__name__)

# Add JSON encoder class to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

# Configure Flask to use our custom JSON encoder
app.json.encoder = NumpyEncoder

@app.route('/')
def dashboard():
    """Render main dashboard"""
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/invoices')
def invoices():
    """Render invoices page"""
    # Get invoices data
    invoices_data = execute_query(
        """
        SELECT invoice_id, customer_id, date, SUM(amount) as total, status, is_paid
        FROM invoices
        GROUP BY invoice_id
        ORDER BY date DESC
        LIMIT 50
        """
    )
    
    # Get customer names for each invoice
    customers = execute_query("SELECT customer_id, name FROM customers")
    customer_dict = {row['customer_id']: row['name'] for _, row in customers.iterrows()}
    
    # Add customer name to invoices
    invoices_with_names = []
    for _, invoice in invoices_data.iterrows():
        invoice_dict = invoice.to_dict()
        invoice_dict['customer_name'] = customer_dict.get(invoice['customer_id'], 'Unknown Customer')
        invoice_dict['is_paid'] = bool(invoice['is_paid'])
        invoices_with_names.append(invoice_dict)
    
    return render_template('invoices.html', invoices=invoices_with_names, active_page='invoices')

@app.route('/customers')
def customers():
    """Render customers page"""
    # Get customer data with insights
    customers_data = execute_query(
        """
        SELECT c.customer_id, c.name, c.email, c.phone, 
               ci.total_sales, ci.transaction_count, ci.avg_order_value
        FROM customers c
        LEFT JOIN customer_insights ci ON c.customer_id = ci.customer_id
        ORDER BY ci.total_sales DESC
        """
    )
    
    # Convert to list of dicts for template
    customers_list = []
    for _, customer in customers_data.iterrows():
        customer_dict = customer.to_dict()
        # Handle NaN values
        for key, value in customer_dict.items():
            if pd.isna(value):
                customer_dict[key] = 0 if key in ['total_sales', 'transaction_count', 'avg_order_value'] else ''
        customers_list.append(customer_dict)
    
    return render_template('customers.html', customers=customers_list, active_page='customers')

@app.route('/products')
def products():
    """Render products page"""
    # Get product data with insights
    products_data = execute_query(
        """
        SELECT i.item_id, i.name, i.description, i.type, i.price,
               pi.total_sales, pi.total_quantity, pi.order_count
        FROM items i
        LEFT JOIN product_insights pi ON i.item_id = pi.item_id
        ORDER BY pi.total_sales DESC
        """
    )
    
    # Convert to list of dicts for template
    products_list = []
    for _, product in products_data.iterrows():
        product_dict = product.to_dict()
        # Handle NaN values
        for key, value in product_dict.items():
            if pd.isna(value):
                product_dict[key] = 0 if key in ['total_sales', 'total_quantity', 'order_count'] else ''
        products_list.append(product_dict)
    
    return render_template('products.html', products=products_list, active_page='products')

@app.route('/api/summary')
def get_summary():
    """Get summary metrics"""
    total_revenue = execute_query(
        "SELECT SUM(amount) as total FROM invoices"
    ).iloc[0]['total']
    
    total_expenses = execute_query(
        "SELECT SUM(amount) as total FROM invoices WHERE item_id IN (SELECT item_id FROM items WHERE type='Expense')"
    ).iloc[0]['total']
    
    net_profit = total_revenue - total_expenses
    
    invoice_count = execute_query(
        "SELECT COUNT(DISTINCT invoice_id) as count FROM invoices"
    ).iloc[0]['count']
    
    # Compare with previous period (example: previous month)
    prev_month_revenue = execute_query(
        "SELECT SUM(amount) as total FROM invoices WHERE month = (SELECT MAX(month)-1 FROM invoices)"
    ).iloc[0]['total']
    
    revenue_change = ((total_revenue - prev_month_revenue) / prev_month_revenue) * 100 if prev_month_revenue else 0
    
    return jsonify({
        'total_revenue': round(total_revenue, 2),
        'total_expenses': round(total_expenses, 2),
        'net_profit': round(net_profit, 2),
        'invoice_count': int(invoice_count),
        'revenue_change': round(revenue_change, 2)
    })

@app.route('/api/sales_trend')
def get_sales_trend():
    """Get monthly sales trend"""
    sales = execute_query(
        """
        SELECT year, month, SUM(amount) as total 
        FROM invoices 
        GROUP BY year, month
        ORDER BY year, month
        """
    )
    
    # Format for chart.js
    months = [f"{row['year']}-{row['month']}" for _, row in sales.iterrows()]
    values = [row['total'] for _, row in sales.iterrows()]
    
    return jsonify({
        'labels': months,
        'values': values
    })

@app.route('/api/top_customers')
def get_top_customers():
    """Get top customers"""
    customers = execute_query(
        """
        SELECT name, total_sales 
        FROM customer_insights 
        ORDER BY total_sales DESC 
        LIMIT 5
        """
    )
    
    return jsonify({
        'names': customers['name'].tolist(),
        'values': customers['total_sales'].tolist()
    })

@app.route('/api/product_breakdown')
def get_product_breakdown():
    """Get product sales breakdown"""
    products = execute_query(
        """
        SELECT name, total_sales 
        FROM product_insights 
        ORDER BY total_sales DESC 
        LIMIT 5
        """
    )
    
    return jsonify({
        'names': products['name'].tolist(),
        'values': products['total_sales'].tolist()
    })

@app.route('/api/invoice_status')
def get_invoice_status():
    """Get invoice payment status"""
    status = execute_query(
        """
        SELECT is_paid, COUNT(*) as count, SUM(amount) as total
        FROM invoices
        GROUP BY is_paid
        """
    )
    
    # Format for chart.js
    labels = ['Paid', 'Unpaid']
    
    # Convert NumPy types to Python native types
    values = [
        int(status[status['is_paid'] == 1]['count'].iloc[0]) if 1 in status['is_paid'].values else 0,
        int(status[status['is_paid'] == 0]['count'].iloc[0]) if 0 in status['is_paid'].values else 0
    ]
    
    receivables = float(status[status['is_paid'] == 0]['total'].iloc[0]) if 0 in status['is_paid'].values else 0
    
    return jsonify({
        'labels': labels,
        'values': values,
        'receivables': round(receivables, 2)
    })

@app.route('/api/aging')
def get_aging():
    """Get AR aging data"""
    aging = execute_query(
        """
        SELECT aging_bucket, amount
        FROM aging_summary
        ORDER BY CASE 
            WHEN aging_bucket = 'Current' THEN 1
            WHEN aging_bucket = '31-60 Days' THEN 2
            WHEN aging_bucket = '61-90 Days' THEN 3
            WHEN aging_bucket = '90+ Days' THEN 4
        END
        """
    )
    
    return jsonify({
        'buckets': aging['aging_bucket'].tolist(),
        'amounts': aging['amount'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)