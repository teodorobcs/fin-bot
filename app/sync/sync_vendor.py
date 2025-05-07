from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

def sync_vendor():
    logger.info("Starting vendor sync...")

    data = fetch_data("vendor")
    if not data or "items" not in data:
        logger.warning("No vendor data found.")
        return

    conn = connect_db()
    cur = conn.cursor()
    inserted, skipped, failed = 0, 0, 0

    for vendor in data["items"]:
        try:
            ns_internalId = vendor.get("id")
            vendorName = vendor.get("entityId")
            isperson = vendor.get("isPerson", False)  # capture early
            email = vendor.get("email")
            phone = vendor.get("phone")

            subsidiary = vendor.get("subsidiary", {})
            subsidiary_id = subsidiary.get("id")
            subsidiary_name = subsidiary.get("refName")

            if not ns_internalId or not vendorName or not subsidiary_id:
                logger.warning(
                    f"Skipping vendor with missing fields: ns_internalId={ns_internalId}, vendorName={vendorName}, subsidiary_id={subsidiary_id}"
                )
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO vendors (
                    ns_internalId, vendorName, email, phone, subsidiary_id, subsidiary_name, isperson, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (ns_internalId) DO UPDATE SET
                    vendorName = EXCLUDED.vendorName,
                    email = EXCLUDED.email,
                    phone = EXCLUDED.phone,
                    subsidiary_id = EXCLUDED.subsidiary_id,
                    subsidiary_name = EXCLUDED.subsidiary_name,
                    isperson = EXCLUDED.isperson;
            """, (ns_internalId, vendorName, email, phone, subsidiary_id, subsidiary_name, isperson))
            inserted += 1

        except Exception as e:
            conn.rollback()
            logger.error(f"Error inserting vendor with ns_internalId {ns_internalId}: {e}")
            failed += 1

    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Vendor sync completed. Inserted: {inserted}, Skipped: {skipped}, Failed: {failed}")