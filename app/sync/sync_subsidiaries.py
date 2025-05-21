# imports
from app.fetch_data import fetch_data               # Function to fetch data from NetSuite
from app.database.connection import connect_db      # Function that establishes connection with the database
from app.logger import logger                       # Function to log the process, warnings, and errors

# Function definition to fetch and store data
def sync_subsidiaries():
    logger.info("Starting subsidiary sync...")

    """
    Calls the fetch_data function to fetch data from NetSuite.
    Calls fetch_data with the parameter "subsidiary".
    The expected response should have an "items" key containing a list of subsidiary records.
    If no data is returned or the expected structure is missing, it logs a warning and stops the process.
    """
    data = fetch_data("subsidiary")
    if not data or "items" not in data:
        logger.warning("No subsidiary data found.")
        return

    conn = connect_db()                     # Creates connection
    cur = conn.cursor()                     # Creates a cursor object to execute SQL commands
    inserted, skipped, failed = 0, 0, 0     # Initialize the counters

    # forloop to iterate through each subsidiary record in 'data'
    for sub in data["items"]:
        try:
            # Field extraction and mapping
            ns_internalId = sub.get("id")                           # Retrieved from sub.get("internalId") and maps it
            name = sub.get("name")                                  # Maps the name field
            state = sub.get("state")                                # Maps the state field
            currency = sub.get("currency", {}).get("refName")       # [dict] Maps the currency field

            # Data validation - checks if essential fields are present
            if not ns_internalId or not name:
                logger.warning(f"Skipping subsidiary with missing fields: ns_internalId={ns_internalId}, name={name}")
                skipped += 1
                continue

           # Record insertion
            cur.execute("""
                INSERT INTO subsidiaries (
                    ns_internalId, name, state, currency, created_at
                ) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    name = EXCLUDED.name,
                    state = EXCLUDED.state,
                    currency = EXCLUDED.currency;
            """, (ns_internalId, name, state, currency))
            inserted += 1

        # Error handling
        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting subsidiary with internalId {ns_internalId}: {e}")
            failed += 1

    conn.commit()       # Commit successful transactions to the database
    cur.close()         # Close cursor
    conn.close()        # Close connection

    # Log summary
    logger.info(f"Subsidiary sync completed. Inserted/Updated: {inserted}, Skipped: {skipped}, Failed: {failed}")
