import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os

# Get path to the database file
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_dir, 'data', 'quickbooks_data.db')

def create_database():
    """Create database tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS invoices ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "invoice_id TEXT,"
        "customer_id TEXT,"
        "date TEXT,"
        "item_id TEXT,"
        "quantity REAL,"
        "unit_price REAL,"
        "amount REAL,"
        "status TEXT,"
        "year INTEGER,"
        "month INTEGER,"
        "day INTEGER,"
        "day_of_week INTEGER,"
        "is_paid INTEGER"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS customers ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "customer_id TEXT,"
        "name TEXT,"
        "email TEXT,"
        "phone TEXT"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS items ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "item_id TEXT,"
        "name TEXT,"
        "description TEXT,"
        "type TEXT,"
        "price REAL"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS accounts ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "account_id TEXT,"
        "name TEXT,"
        "type TEXT,"
        "balance REAL"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS daily_sales ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "date TEXT,"
        "daily_sales REAL"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS customer_insights ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "customer_id TEXT,"
        "name TEXT,"
        "total_sales REAL,"
        "transaction_count INTEGER,"
        "avg_order_value REAL"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS product_insights ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "item_id TEXT,"
        "name TEXT,"
        "total_sales REAL,"
        "total_quantity REAL,"
        "order_count INTEGER"
        ");"
    )
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS aging_summary ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "aging_bucket TEXT,"
        "amount REAL"
        ");"
    )
    
    conn.commit()
    conn.close()

def store_dataframe(df, table_name):
    """Store DataFrame to database table"""
    engine = create_engine(f'sqlite:///{DB_PATH}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result