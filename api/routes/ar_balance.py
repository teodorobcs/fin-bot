# ar_balance.py
from fastapi import APIRouter, Query, HTTPException
from app.database.connection import connect_db

router = APIRouter()

@router.get("/ar-balance")
def get_ar_balance(
    group_by: str = Query("subsidiary", description="Group by 'subsidiary' or 'customer'"),
    subsidiary: str = Query(None, description="Filter by subsidiary name"),
    customer: str = Query(None, description="Filter by customer name"),
    status: str = Query(None, description="Filter by invoice status")
):
    if group_by not in ["subsidiary", "customer"]:
        raise HTTPException(status_code=400, detail="Invalid group_by value. Must be 'subsidiary' or 'customer'.")

    group_field = "subsidiary_name" if group_by == "subsidiary" else "customer_name"

    conn = connect_db()
    cur = conn.cursor()

    # Build base query
    query = f"""
        SELECT {group_field}, SUM(amountRemaining)
        FROM invoices
        WHERE amountRemaining > 0
    """
    params = []

    if subsidiary:
        query += " AND subsidiary_name = %s"
        params.append(subsidiary)

    if customer:
        query += " AND customer_name = %s"
        params.append(customer)

    if status:
        query += " AND status = %s"
        params.append(status)

    query += f" GROUP BY {group_field}"

    cur.execute(query, params)
    rows = cur.fetchall()

    total_ar = sum([row[1] for row in rows])

    result = {
        "total_ar": float(total_ar),
        f"by_{group_by}": [
            {"name": row[0], "amount": float(row[1])} for row in rows
        ]
    }

    cur.close()
    conn.close()
    return result