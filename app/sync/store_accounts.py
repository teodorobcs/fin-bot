# store_accounts.py

# Import modules
from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

# Fetch and store accounts from NetSuite into PostgreSQL
def store_accounts():
    logger.info("Starting accounts sync...")

    data = fetch_data("account")
    if not data or "items" not in data:
        logger.warning("No account data retrieved.")
        return

    conn = connect_db()
    cur = conn.cursor()

    for acc in data["items"]:
        try:
            cur.execute("""
                INSERT INTO accounts (
                    netsuite_id, name, account_number, account_type, subsidiary_id
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (netsuite_id) DO NOTHING;
            """, (
                acc.get("id"),
                acc.get("name"),
                acc.get("acctNumber"),
                acc.get("acctType"),
                acc.get("subsidiary", {}).get("id")
            ))
        except Exception as e:
            logger.error(f"Error inserting account ID {acc.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Account sync complete.")