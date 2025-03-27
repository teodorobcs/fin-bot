# store_transactions.py

# Import modules
from app.fetch_data import fetch_data
from app.database.connection import connect_db
from app.logger import logger

# Fetch and store transaction records from NetSuite into PostgreSQL
def store_transactions():
    logger.info("Starting transaction sync...")

    data = fetch_data("transaction")
    if not data or "items" not in data:
        logger.warning("No transaction data retrieved.")
        return

    conn = connect_db()
    cur = conn.cursor()

    for txn in data["items"]:
        try:
            cur.execute("""
                INSERT INTO transactions (
                    netsuite_id,
                    transaction_type,
                    transaction_number,
                    reference_number,
                    amount,
                    currency,
                    date,
                    customer_id,
                    vendor_id,
                    account_id,
                    status,
                    memo,
                    last_modified
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (netsuite_id) DO NOTHING;
            """, (
                txn.get("id"),
                txn.get("type"),
                txn.get("tranId"),
                txn.get("refNumber"),
                txn.get("total"),
                txn.get("currency", {}).get("name"),
                txn.get("tranDate"),
                txn.get("entity", {}).get("id") if txn.get("type") in ("Invoice", "SalesOrd") else None,
                txn.get("entity", {}).get("id") if txn.get("type") in ("VendorBill", "Check") else None,
                txn.get("account", {}).get("id"),
                txn.get("status"),
                txn.get("memo")
            ))
        except Exception as e:
            logger.error(f"Error inserting transaction ID {txn.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.info("Transaction sync complete.")