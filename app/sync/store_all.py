from store_employees import store_employees
from store_customers import store_customers
from store_vendors import store_vendors
from store_transactions import store_transactions
from store_accounts import store_accounts
from store_subsidiaries import store_subsidiaries

def store_all():
    store_subsidiaries()
    store_employees()
    store_customers()
    store_vendors()
    store_accounts()
    store_transactions()

if __name__ == "__main__":
    store_all()
