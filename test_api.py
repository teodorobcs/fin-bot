import fetch_data as fd

endpoint = "invoice"

try:
    data = fd.fetch_data(endpoint)
except Exception as e:
    print(f"An error occurred: {e}")
    data = None

if data is not None:
    print("Data retrieved successfully!")
else:
    print("Error retrieving data. Check logs for details.")