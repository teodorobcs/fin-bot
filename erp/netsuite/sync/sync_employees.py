# sync_employees.py
from app.fetch_data import fetch_data          # Fetches data from NetSuite API
from app.database.connection import connect_db # Establishes database connection
from app.logger import logger                  # Handles logging

def sync_employees():
    logger.info("Starting employee sync...")

    data = fetch_data("employee")
    if not data or "items" not in data:
        logger.warning("No employee data found.")
        return

    conn = connect_db()
    cur = conn.cursor()
    inserted, skipped, failed = 0, 0, 0

    # Iterate over each employee record
    for emp in data["items"]:
        try:
            # Field extraction
            ns_internalId = emp.get("id")
            accountNumber = emp.get("accountNumber")
            firstName = emp.get("firstName")
            lastName = emp.get("lastName")
            title = emp.get("title")
            subsidiary = emp.get("subsidiary", {})
            subsidiary_id = subsidiary.get("id")            # References subsidiary table
            subsidiary_name = subsidiary.get("refName")      # Human-readable subsidiary name

            # Validation: Ensure essential fields are present
            if not ns_internalId or not firstName or not lastName:
                logger.warning(
                    f"Skipping employee with missing required fields: ns_internalId={ns_internalId}, firstName={firstName}, lastName={lastName}"
                )
                skipped += 1
                continue

            # Insert or update employee record
            cur.execute("""
                INSERT INTO employees (
                    ns_internalId, accountNumber, firstName, lastName, title, subsidiary_id, subsidiary_name, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    accountNumber = EXCLUDED.accountNumber,
                    firstName = EXCLUDED.firstName,
                    lastName = EXCLUDED.lastName,
                    title = EXCLUDED.title,
                    subsidiary_id = EXCLUDED.subsidiary_id,
                    subsidiary_name = EXCLUDED.subsidiary_name;
            """, (ns_internalId, accountNumber, firstName, lastName, title, subsidiary_id, subsidiary_name))
            inserted += 1

        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting employee with ns_internalId {ns_internalId}: {e}")
            failed += 1

    # Commit and close connection
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Employee sync completed. Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")