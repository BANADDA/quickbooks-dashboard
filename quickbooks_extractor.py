import pandas as pd
import os
from config import (
    QUICKBOOKS_CLIENT_ID, 
    QUICKBOOKS_CLIENT_SECRET,
    QUICKBOOKS_REDIRECT_URI,
    QUICKBOOKS_ENVIRONMENT
)

# Note: Uncomment the following imports when you have the QuickBooks API credentials
# from intuitlib.client import AuthClient
# from quickbooks import QuickBooks
# from quickbooks.objects.invoice import Invoice
# from quickbooks.objects.customer import Customer
# from quickbooks.objects.item import Item
# from quickbooks.objects.account import Account

def get_auth_client():
    """Get QuickBooks authentication client"""
    # Uncomment when ready to use the QuickBooks API
    # auth_client = AuthClient(
    #     client_id=QUICKBOOKS_CLIENT_ID,
    #     client_secret=QUICKBOOKS_CLIENT_SECRET,
    #     redirect_uri=QUICKBOOKS_REDIRECT_URI,
    #     environment=QUICKBOOKS_ENVIRONMENT
    # )
    # return auth_client
    pass

def get_quickbooks_client(auth_client, refresh_token, company_id):
    """Get QuickBooks client"""
    # Uncomment when ready to use the QuickBooks API
    # client = QuickBooks(
    #     auth_client=auth_client,
    #     refresh_token=refresh_token,
    #     company_id=company_id
    # )
    # return client
    pass

def extract_invoices(start_date, end_date, client=None):
    """Extract invoices within date range"""
    if client:
        # Use QuickBooks API
        # Uncomment and implement when ready to use the QuickBooks API
        # invoices = Invoice.query(
        #     f"TxnDate >= '{start_date}' AND TxnDate <= '{end_date}'", 
        #     qb=client
        # )
        # 
        # invoice_data = []
        # for invoice in invoices:
        #     for line in invoice.Line:
        #         if hasattr(line, 'SalesItemLineDetail'):
        #             invoice_data.append({
        #                 'invoice_id': invoice.Id,
        #                 'customer_id': invoice.CustomerRef.value if invoice.CustomerRef else None,
        #                 'date': invoice.TxnDate,
        #                 'item_id': line.SalesItemLineDetail.ItemRef.value,
        #                 'quantity': line.SalesItemLineDetail.Qty,
        #                 'unit_price': line.SalesItemLineDetail.UnitPrice,
        #                 'amount': line.Amount,
        #                 'status': invoice.status,
        #             })
        # 
        # return pd.DataFrame(invoice_data)
        pass
    else:
        # Use CSV file
        return import_from_csv('exports/invoices.csv')

def extract_customers(client=None):
    """Extract customer information"""
    if client:
        # Use QuickBooks API
        # Uncomment and implement when ready to use the QuickBooks API
        # customers = Customer.query("SELECT * FROM Customer", qb=client)
        # 
        # customer_data = []
        # for customer in customers:
        #     customer_data.append({
        #         'customer_id': customer.Id,
        #         'name': customer.DisplayName,
        #         'email': customer.PrimaryEmailAddr.Address if hasattr(customer, 'PrimaryEmailAddr') else None,
        #         'phone': customer.PrimaryPhone.FreeFormNumber if hasattr(customer, 'PrimaryPhone') else None,
        #     })
        # 
        # return pd.DataFrame(customer_data)
        pass
    else:
        # Use CSV file
        return import_from_csv('exports/customers.csv')

def extract_items(client=None):
    """Extract item/product information"""
    if client:
        # Use QuickBooks API
        # Uncomment and implement when ready to use the QuickBooks API
        # items = Item.query("SELECT * FROM Item", qb=client)
        # 
        # item_data = []
        # for item in items:
        #     item_data.append({
        #         'item_id': item.Id,
        #         'name': item.Name,
        #         'description': item.Description,
        #         'type': item.Type,
        #         'price': item.UnitPrice if hasattr(item, 'UnitPrice') else None,
        #     })
        # 
        # return pd.DataFrame(item_data)
        pass
    else:
        # Use CSV file
        return import_from_csv('exports/items.csv')

def extract_accounts(client=None):
    """Extract account information"""
    if client:
        # Use QuickBooks API
        # Uncomment and implement when ready to use the QuickBooks API
        # accounts = Account.query("SELECT * FROM Account", qb=client)
        # 
        # account_data = []
        # for account in accounts:
        #     account_data.append({
        #         'account_id': account.Id,
        #         'name': account.Name,
        #         'type': account.AccountType,
        #         'balance': account.CurrentBalance if hasattr(account, 'CurrentBalance') else None,
        #     })
        # 
        # return pd.DataFrame(account_data)
        pass
    else:
        # Use CSV file
        return import_from_csv('exports/accounts.csv')

def import_from_csv(filepath):
    """Import data from CSV export"""
    # Get the absolute path to the CSV file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_dir, filepath)
    
    # Read the CSV file
    return pd.read_csv(absolute_path)