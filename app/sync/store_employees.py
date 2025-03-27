# store_employees.py

# Import modules from code base
from app.fetch_data import fetch_data               # Imports the fetch function to get data from NetSutie
from app.database.connection import connect_db      # Connects to Postgres database
from app.logger import logger                       # Logs info and errors to a log file

# Function to fetch and store employee records from NetSuite into PostgreSQL
def store_employees():
    logger.info("Starting employee sync...")

    # Fetch data from NetSuite employee endpoint
    data = fetch_data("employee") # This is the ending part of the endpoint URL
    if not data or "items" not in data:
        logger.warning("No employee data found.")
        return

    # Initialize connection and cursor
    conn = connect_db()
    cur = conn.cursor()

    for emp in data["items"]:
        try:
            cur.execute("""
                INSERT INTO employees (
                    netsuite_id, name, title, department, email, subsidiary_id, active, last_modified, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (netsuite_id) DO NOTHING;
            """,(
                emp.get("id"),
                emp.get("entityid"),
                emp.get("title"),
                emp.get("department"),
                emp.get("email"),
                emp.get("subsidiary", {}).get("id"),
                emp.get("isInactive") is False  # True if not inactive
            ))
        except Exception as e:
            logger.error(f"Error inserting employee ID {emp.get('id')} into database: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Employee sync complete.")

