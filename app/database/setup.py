from connection import connect_db

def create_tables():
    """Creates tables for NetSuite data: employees, customers, vendors, transactions, accounts, subsidiaries, etc."""
    conn = connect_db()
    cur = conn.cursor()

    # Subsidiaries Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subsidiaries (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        country TEXT,
        currency TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_subsidiaries_netsuite_id ON subsidiaries(netsuite_id);
    """)

    # Employees Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE,
        name TEXT NOT NULL,
        title TEXT,
        department TEXT,
        email TEXT UNIQUE,
        subsidiary_id INT REFERENCES subsidiaries(netsuite_id),
        active BOOLEAN DEFAULT TRUE,
        last_modified TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_employees_netsuite_id ON employees(netsuite_id);
    CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
    """)

    # Customers Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE,
        name TEXT NOT NULL,
        company TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        subsidiary_id INT REFERENCES subsidiaries(netsuite_id),
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_customers_netsuite_id ON customers(netsuite_id);
    CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
    """)

    # Vendors Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        subsidiary_id INT REFERENCES subsidiaries(netsuite_id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_vendors_netsuite_id ON vendors(netsuite_id);
    """)

    # Accounts Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        account_number TEXT,
        account_type TEXT CHECK (account_type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense')),
        subsidiary_id INT REFERENCES subsidiaries(netsuite_id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_accounts_netsuite_id ON accounts(netsuite_id);
    CREATE INDEX IF NOT EXISTS idx_accounts_type ON accounts(account_type);
    """)

    # Transactions Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        netsuite_id INT UNIQUE NOT NULL,
        transaction_type TEXT NOT NULL,
        transaction_number TEXT,
        reference_number TEXT,
        amount DECIMAL(12,2) NOT NULL,
        currency TEXT,
        date TIMESTAMP NOT NULL,
        customer_id INT REFERENCES customers(netsuite_id) ON DELETE SET NULL,
        vendor_id INT REFERENCES vendors(netsuite_id) ON DELETE SET NULL,
        account_id INT REFERENCES accounts(netsuite_id),
        status TEXT,
        memo TEXT,
        last_modified TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_transactions_netsuite_id ON transactions(netsuite_id);
    CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
    CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);
    CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);
    """)

    # API Sync Status Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_sync_status (
        id SERIAL PRIMARY KEY,
        entity TEXT,
        last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT CHECK (status IN ('Success', 'Failed')),
        error_message TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_sync_status_entity ON api_sync_status(entity);
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database setup complete!")

if __name__ == "__main__":
    create_tables()