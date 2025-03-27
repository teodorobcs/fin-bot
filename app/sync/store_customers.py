# store_customers.py

# Import modules from code base
from app.fetch_data import fetch_data               # Imports the fetch function to get data from NetSuite
from app.database.connection import connect_db      # Connects to Postgres database
from app.logger import logger                       # Logs info and errors to a log file

# Function to fetch and store customer records from NetSuite into PostgreSQL
def store_customers():
    logger.info("Starting customer sync...")

    # Fetch data from NetSuite customer endpoint
    data = fetch_data("customer") # This is the ending part of the endpoint URL
    if not data or "items" not in data:
        logger.warning("No customer data found.")
        return

    # Initialize connection and cursor
    conn = connect_db()
    cur = conn.cursor()

    for cust in data["items"]:
        try:
            cur.execute("""
                INSERT INTO customers (
                    netsuite_id, name, company, email, phone, subsidiary_id, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (netsuite_id) DO NOTHING;
            """,(
                cust.get("id"),
                cust.get("entityid"),
                cust.get("companyName"),
                cust.get("email"),
                cust.get("phone"),
                cust.get("subsidiary", {}).get("id"),
                cust.get("entityStatus", {}).get("name")
            ))
        except Exception as e:
            logger.error(f"Error inserting customer ID {cust.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Customer sync complete.")

