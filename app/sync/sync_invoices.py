from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

def sync_invoices():
    logger.info("Starting invoice sync...")

    data = fetch_data("invoice")
    if not data or "items" not in data:
        logger.warning("No invoice data found.")
        return

    conn = connect_db()
    cur = conn.cursor()
    inserted, skipped, failed = 0, 0, 0

    for inv in data["items"]:
        try:
            ns_internalId = inv.get("id")
            amountPaid = inv.get("amountPaid")
            amountRemaining = inv.get("amountRemaining")

            # Extract client from the 'entity' RecordRef (if provided)
            entity = inv.get("entity", {})
            customer_id = entity.get("id")
            customer_name = entity.get("refName")

            tranid = inv.get("tranId")
            tranDate = inv.get("tranDate")
            dueDate = inv.get("dueDate")
            terms = inv.get("terms", {}).get("refName")
            total = inv.get("total")
            status = inv.get("status", {}).get("refName")

            subsidiary = inv.get("subsidiary", {})
            subsidiary_id = subsidiary.get("id")
            subsidiary_name = subsidiary.get("refName")

            # Validate required fields: ns_internalId, tranDate, total, and subsidiary_id.
            if not ns_internalId or not tranDate or total is None or not subsidiary_id:
                logger.warning(
                    f"Skipping invoice with missing fields: ns_internalId={ns_internalId}, tranDate={tranDate}, total={total}, subsidiary_id={subsidiary_id}"
                )
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO invoices (
                    ns_internalId, amountPaid, amountRemaining, customer_id, customer_name, tranid, tranDate, dueDate, terms, total, status, subsidiary_id, subsidiary_name, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    amountPaid = EXCLUDED.amountPaid,
                    amountRemaining = EXCLUDED.amountRemaining,
                    customer_id = EXCLUDED.customer_id,
                    customer_name = EXCLUDED.customer_name,
                    tranid = EXCLUDED.tranid,
                    tranDate = EXCLUDED.tranDate,
                    dueDate = EXCLUDED.dueDate,
                    terms = EXCLUDED.terms,
                    total = EXCLUDED.total,
                    status = EXCLUDED.status,
                    subsidiary_id = EXCLUDED.subsidiary_id,
                    subsidiary_name = EXCLUDED.subsidiary_name;
            """, (ns_internalId, amountPaid, amountRemaining, customer_id, customer_name, tranid, tranDate, dueDate, terms, total, status, subsidiary_id, subsidiary_name))
            inserted += 1

        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting invoice with ns_internalId {ns_internalId}: {e}")
            failed += 1

    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Invoice sync completed. Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")