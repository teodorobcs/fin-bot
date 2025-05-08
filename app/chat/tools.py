import requests

API_BASE_URL = "http://localhost:8000"  # Update this if running elsewhere

# --------------------
# Tool: Get Invoices
# --------------------
def get_invoices(subsidiary=None, customer=None, status=None):
    """Fetches filtered invoice list from the FastAPI backend."""
    params = {}
    if subsidiary:
        params["subsidiary"] = subsidiary
    if customer:
        params["customer"] = customer
    if status:
        params["status"] = status

    try:
        response = requests.get(f"{API_BASE_URL}/invoices", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": f"Failed to fetch invoices: {str(e)}",
            "status_code": response.status_code if 'response' in locals() else None,
            "details": response.text if 'response' in locals() else None
        }


# --------------------
# Tool: Get AR Balance
# --------------------
def get_ar_balance(group_by="subsidiary", status=None):
    """Returns AR balances grouped by subsidiary or customer."""
    params = {}
    if group_by:
        params["group_by"] = group_by
    if status:
        params["status"] = status

    try:
        response = requests.get(f"{API_BASE_URL}/ar-balance", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": f"Failed to fetch AR balance: {str(e)}",
            "status_code": response.status_code if 'response' in locals() else None,
            "details": response.text if 'response' in locals() else None
        }