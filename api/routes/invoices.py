# api/routes/invoices.py
from fastapi import APIRouter, Query
from app.database.connection import connect_db

router = APIRouter()

@router.get("/invoices")
def get_invoices(
    subsidiary: str = Query(None, description="Filter by subsidiary name"),
    customer: str = Query(None, description="Filter by customer name"),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    status: str = Query(None, description="Filter by invoice status (e.g. 'Open')")
):
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Base query
    query = """
        SELECT tranid, customer_name, subsidiary_name, total, amountRemaining, status, tranDate, total, duedate, terms
        FROM invoices
        WHERE 1=1
    """
    params = []

    # Apply filters if provided
    if subsidiary:
        query += " AND subsidiary_name = %s"
        params.append(subsidiary)

    if customer:
        query += " AND customer_name = %s"
        params.append(customer)

    if status:
        if status.lower() == "open":
            query += " AND amountRemaining > 0"
        elif status.lower() in ("paid", "paid in full"):
            query += " AND amountRemaining = 0"
        else:
            query += " AND status = %s"
            params.append(status)

    if start_date:
        query += " AND tranDate >= %s"
        params.append(start_date)

    if end_date:
        query += " AND tranDate <= %s"
        params.append(end_date)

    query += " ORDER BY tranDate DESC"

    # Execute query
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Map results to dictionaries for JSON response
    return [
        {
            "ns_internalId": row[0],
            "customer_name": row[1],
            "subsidiary_name": row[2],
            "total": row[3],
            "amountRemaining": row[4],
            "status": row[5],
            "tranDate": row[6],
        } for row in rows
    ]