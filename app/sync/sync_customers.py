from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

def sync_customer():
    logger.info("Starting customer sync...")

    data = fetch_data("customer")
    if not data or "items" not in data:
        logger.warning("No customer data found.")
        return

    conn = connect_db()
    cur = conn.cursor()
    inserted, skipped, failed = 0, 0, 0

    for cust in data["items"]:
        try:
            ns_internalId = cust.get("id")
            clientName = cust.get("companyName")
            clientEmail = cust.get("email")
            startDate = cust.get("startDate")
            endDate = cust.get("endDate")
            terms = cust.get("terms", {}).get("refName")
            subsidiary = cust.get("subsidiary", {})
            subsidiary_id = subsidiary.get("id")  # References subsidiary table
            subsidiary_name = subsidiary.get("refName")  # Human-readable subsidiary name

            # Validate required fields: ns_internalId, clientName, and subsidiary_id.
            if not ns_internalId or not clientName or not subsidiary_id:
                logger.warning(
                    f"Skipping customer with missing fields: ns_internalId={ns_internalId}, clientName={clientName}, subsidiary_id={subsidiary_id}"
                )
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO customers (
                    ns_internalId, clientName, clientEmail, subsidiary_id, subsidiary_name, startDate, endDate, terms, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    clientName = EXCLUDED.clientName,
                    clientEmail = EXCLUDED.clientEmail,
                    subsidiary_id = EXCLUDED.subsidiary_id,
                    subsidiary_name = EXCLUDED.subsidiary_name,
                    startDate = EXCLUDED.startDate,
                    endDate = EXCLUDED.endDate,
                    terms = EXCLUDED.terms;
            """, (ns_internalId, clientName, clientEmail, subsidiary_id, subsidiary_name, startDate, endDate, terms))
            inserted += 1

        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting customer with ns_internalId {ns_internalId}: {e}")
            failed += 1

    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Customer sync completed. Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")