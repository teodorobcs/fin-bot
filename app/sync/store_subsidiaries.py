# store_subsidiaries.py

# Import modules
from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

# Fetch and store subsidiaries from NetSuite into PostgreSQL
def store_subsidiaries():
    logger.info("Starting subsidiary sync...")

    data = fetch_data("subsidiary")
    if not data or "items" not in data:
        logger.warning("No subsidiary data retrieved.")
        return

    conn = connect_db()
    cur = conn.cursor()

    for sub in data["items"]:
        try:
            cur.execute("""
                INSERT INTO subsidiaries (
                    netsuite_id, name, country, currency
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (netsuite_id) DO NOTHING;
            """, (
                sub.get("id"),
                sub.get("name"),
                sub.get("country"),
                sub.get("currency", {}).get("name")
            ))
        except Exception as e:
            logger.error(f"Error inserting subsidiary ID {sub.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Subsidiary sync complete.")