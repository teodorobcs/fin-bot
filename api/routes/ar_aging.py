# api/routes/ar_aging.py

# Import
from fastapi import APIRouter, Query, HTTPException
from app.database.connection import connect_db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

router = APIRouter()

@router.get("/ar-aging")
def get_ar_aging(
    as_of_date: str = Query(default=datetime.today().strftime("%Y-%m-%d"), description="Date to calculate aging buckets (YYYY-MM-DD)"),
    subsidiary: Optional[str] = Query(None, description="Filter by subsidiary name"),
    customer: Optional[str] = Query("customer", description="Filter by customer name")
):
    try:
        report_date = datetime.strptime(as_of_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    conn = connect_db()
    cur = conn.cursor()

    query = f"""
        SELECT
            customer_name,
            subsidiary_name,
            tranid AS invoice_id,
            total,
            amountRemaining,
            dueDate,
            CASE
                WHEN dueDate >= %s THEN 'current'
                WHEN dueDate < %s AND dueDate >= %s THEN '30_days'
                WHEN dueDate < %s AND dueDate >= %s THEN '60_days'
                WHEN dueDate < %s AND dueDate >= %s THEN '90_days'
                ELSE 'over_90_days'
            END AS aging_bucket
        FROM invoices
        WHERE amountRemaining > 0
    """

    params = [
        report_date,  # for Current
        report_date, report_date - relativedelta(months=1),  # for 30 Days
                     report_date - relativedelta(months=1), report_date - relativedelta(months=2),  # for 60 Days
                     report_date - relativedelta(months=2), report_date - relativedelta(months=3)  # for 90 Days
    ]

    if subsidiary:
        query += " AND subsidiary_name = %s"
        params.append(subsidiary)

    if customer:
        query += " AND customer_name = %s"
        params.append(customer)

    query += " ORDER BY customer_name, subsidiary_name, dueDate"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Build customer-level AR aging report
    report = {}
    for row in rows:
        customer_name, sub_name, invoice_id, total, remaining, due_date, bucket = row
        if customer_name not in report:
            report[customer_name] = {
                "current": 0.0,
                "30_days": 0.0,
                "60_days": 0.0,
                "90_days": 0.0,
                "over_90_days": 0.0,
                "total": 0.0
            }

        report[customer_name][bucket] += float(remaining)
        report[customer_name]["total"] += float(remaining)

    # Format output
    output = {
        "as_of_date": str(report_date),
        "filters": {
            "subsidiary": subsidiary or "All",
            "customer": customer or "All"
        },
        "data": []
    }

    for customer, values in sorted(report.items(), key=lambda i: i[1]["total"], reverse=True):
        output["data"].append({
            "customer": customer,
            "current": round(values["current"], 2),
            "30_days": round(values["30_days"], 2),
            "60_days": round(values["60_days"], 2),
            "90_days": round(values["90_days"], 2),
            "over_90_days": round(values["over_90_days"], 2),
            "total": round(values["total"], 2),
        })

    return output