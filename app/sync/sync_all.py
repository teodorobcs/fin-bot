from sync_account import sync_account
from sync_employees import sync_employees
from sync_customers import sync_customer
from sync_vendor import sync_vendor
from sync_invoices import sync_invoices
from sync_subsidiaries import sync_subsidiaries

def sync_all():
    sync_subsidiaries()
    sync_account()
    sync_employees()
    sync_customer()
    sync_vendor()
    sync_invoices()

if __name__ == "__main__":
    sync_all()
