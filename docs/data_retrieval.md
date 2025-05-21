# API Endpoints Reference

This page provides a comprehensive reference for the GET API endpoints used in the NetSuite Chatbot project. It covers endpoints for Invoice, Customer, Vendor, Employee, Vendor Bill, Subsidiary, and Account records.

## Overview

Each API endpoint is secured using OAuth1, and all API interactions are logged for debugging and troubleshooting. Make sure your credentials are properly set in the configuration files (e.g., `config.py` and `.env`).

## Authentication & Logging

- **Authentication:**  
  All requests are authenticated using OAuth1. Verify that your `CONSUMER_KEY`, `CONSUMER_SECRET`, `TOKEN_ID`, and `TOKEN_SECRET` are set correctly.
  
- **Logging:**  
  All API requests and errors are logged to `logs/netsuite_api.log`. Check this file for any error messages or debugging information.

## API Endpoints

Below is a table that outlines the primary endpoints, their descriptions, and example URLs.

| **Endpoint**    | **Description**                                    | **Example URL**                                     |
|-----------------|----------------------------------------------------|-----------------------------------------------------|
| **Invoice**     | Retrieves invoice records                          | `/services/rest/record/v1/invoice`                  |
| **Customer**    | Retrieves customer records                         | `/services/rest/record/v1/customer`                 |
| **Vendor**      | Retrieves vendor records                           | `/services/rest/record/v1/vendor`                   |
| **Employee**    | Retrieves employee records                         | `/services/rest/record/v1/employee`                 |
| **Vendor Bill** | Retrieves vendor bill records                      | `/services/rest/record/v1/vendorBill`               |
| **Subsidiary**  | Retrieves subsidiary records                       | `/services/rest/record/v1/subsidiary`               |
| **Account**     | Retrieves account records (Chart of Accounts)      | `/services/rest/record/v1/account`                  |

## Usage Example

Below is a sample code snippet demonstrating how to use the `fetch_data` function to retrieve data from one of the endpoints (in this case, the employee endpoint):

```python
from api.app import fetch_data

data = fetch_data("employee")
if data:
  print("Employee data retrieved successfully!")
else:
  print("Error retrieving employee data. Please check logs for details.")
```
## Error Handling & Debugging

- **All requests & errors are logged** in `logs/netsuite_api.log`.
- If an API request **fails**, error details are automatically logged.
- **Debugging steps:**
  - Check the **NetSuite Login Audit Trail**: Setup → Users/Roles → User Management → View Login Audit Trail