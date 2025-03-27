# store_vendors.py

# Import modules
from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

# Fetch and store vendor records from NetSuite into PostgreSQL
def store_vendors():
    logger.info("Starting vendor sync...")

    data = fetch_data("vendor")
    if not data or "items" not in data:
        logger.warning("No vendor data retrieved.")
        return

    conn = connect_db()
    cur = conn.cursor()

    for vendor in data["items"]:
        try:
            cur.execute("""
                INSERT INTO vendors (
                    netsuite_id, name, email, phone, subsidiary_id
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (netsuite_id) DO NOTHING;
            """, (
                vendor.get("id"),
                vendor.get("entityid"),
                vendor.get("email"),
                vendor.get("phone"),
                vendor.get("subsidiary", {}).get("id")
            ))
        except Exception as e:
            logger.error(f"Error inserting vendor ID {vendor.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Vendor sync complete.")