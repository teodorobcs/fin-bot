# sync_account.py
from app.fetch_data import fetch_data               # Function to fetch data from NetSuite
from app.database.connection import connect_db      # Function that establishes connection with the database
from app.logger import logger                       # Function to log the process, warnings, and errors

def sync_account():
    logger.info("Starting account sync...")

    data = fetch_data("account")
    if not data or "items" not in data:
        logger.warning("No account data found.")
        return

    conn = connect_db()                     # Creates connection
    cur = conn.cursor()                     # Creates a cursor object to execute SQL commands
    inserted, skipped, failed = 0, 0, 0     # Initialize the counters

    # forloop to iterate through each account record in 'data'
    for acc in data["items"]:
        try:

            # Field extractions and mapping
            ns_internalId = acc.get("id")
            acctName = acc.get("acctName")
            acctNumber = acc.get("acctNumber")
            acctType = acc.get("acctType", {}).get("refName")

            # Check for required fields; note: acctType == 0 is valid, so we check specifically for None.
            if not ns_internalId or not acctName or acctType is None:
                logger.warning(
                    f"Skipping account with missing fields: ns_internalId={ns_internalId}, acctName={acctName}, acctType={acctType}"
                )
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO accounts (
                    ns_internalId, acctName, acctNumber, acctType, created_at
                ) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    acctName = EXCLUDED.acctName,
                    acctNumber = EXCLUDED.acctNumber,
                    acctType = EXCLUDED.acctType;
            """, (ns_internalId, acctName, acctNumber, acctType))
            inserted += 1

        # Error handling
        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting account with ns_internalId {ns_internalId}: {e}")
            failed += 1

    conn.commit()       # Commit successful transactions to the database
    cur.close()         # Close cursor
    conn.close()        # Close connection

    # Log summary
    logger.info(f"Account sync completed. Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")