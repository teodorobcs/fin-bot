from connection import connect_db

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Subsidiaries - reviewed 2025-04-03
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subsidiaries (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        state TEXT,
        currency TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_subsidiaries_ns_internalId ON subsidiaries(ns_internalId);")

    # Accounts - reviewed and updated 2025-04-27
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        acctName TEXT NOT NULL,
        acctNumber TEXT,
        acctType TEXT,  -- changed from INT to TEXT, no CHECK constraint
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_ns_internalId ON accounts(ns_internalId);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_acctType ON accounts(acctType);")

    # Employees - reviewed 2025-04-27
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        accountNumber TEXT,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        title TEXT,
        subsidiary_id TEXT REFERENCES subsidiaries(ns_internalId), -- Connection
        subsidiary_name TEXT, -- Display name
        last_modified TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_employees_ns_internalId ON employees(ns_internalId);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_employees_subsidiary_id ON employees(subsidiary_id);")

    # Customers - reviewed 2025-04-28
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        clientName TEXT NOT NULL,
        clientEmail TEXT,
        subsidiary_id TEXT NOT NULL REFERENCES subsidiaries(ns_internalId),
        subsidiary_name TEXT,
        startDate TIMESTAMP,
        endDate TIMESTAMP,
        terms TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_customers_ns_internalId ON customers(ns_internalId);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_customers_clientEmail ON customers(clientEmail);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_customers_subsidiary_id ON customers(subsidiary_id);")

    # Vendors - reviewed 2025-04-28
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        vendorName TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        subsidiary_id TEXT REFERENCES subsidiaries(ns_internalId),
        subsidiary_name TEXT,
        isperson BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_ns_internalId ON vendors(ns_internalId);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_subsidiary_id ON vendors(subsidiary_id);")

    # Invoices - reviewed 2025-04-29
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id SERIAL PRIMARY KEY,
        ns_internalId TEXT UNIQUE NOT NULL,
        amountPaid DECIMAL(12,2),
        amountRemaining DECIMAL(12,2),
        customer_id TEXT REFERENCES customers(ns_internalId) ON DELETE SET NULL,
        customer_name TEXT,
        tranid TEXT,
        tranDate DATE NOT NULL,
        dueDate DATE,
        terms TEXT,
        total DECIMAL(12,2) NOT NULL,
        status TEXT,
        subsidiary_id TEXT NOT NULL REFERENCES subsidiaries(ns_internalId),
        subsidiary_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_invoices_ns_internalId ON invoices(ns_internalId);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_invoices_tranDate ON invoices(tranDate);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_invoices_subsidiary_id ON invoices(subsidiary_id);")

    """# API Sync Status - reviewed 2025-04-29
    cur.execute("""
    """CREATE TABLE IF NOT EXISTS api_sync_status (
        id SERIAL PRIMARY KEY,
        entity TEXT,
        last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT CHECK (status IN ('Success', 'Failed')),
        error_message TEXT
    );"""
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sync_status_entity ON api_sync_status(entity);")"""

    conn.commit()
    cur.close()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    create_tables()
