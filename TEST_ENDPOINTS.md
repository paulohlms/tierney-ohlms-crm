# Test Examples for Fixed Endpoints

## Prerequisites

1. Start your server:
   ```bash
   uvicorn main:app --reload
   ```

2. Login first to get session cookie:
   - Email: `admin@tierneyohlms.com`
   - Password: `ChangeMe123!`

## Test Dashboard Endpoint

### Using Python requests:
```python
import requests

# Create session
session = requests.Session()

# Login
login_response = session.post(
    "http://localhost:8000/login",
    data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"}
)

# Access dashboard
dashboard_response = session.get("http://localhost:8000/dashboard")
print(f"Status: {dashboard_response.status_code}")
print(f"Content length: {len(dashboard_response.text)}")
print("Dashboard loaded successfully!" if dashboard_response.status_code == 200 else "Failed!")
```

### Using cURL:
```bash
# Login and save cookie
curl -c cookies.txt -b cookies.txt -X POST \
  -d "email=admin@tierneyohlms.com" \
  -d "password=ChangeMe123!" \
  http://localhost:8000/login

# Access dashboard
curl -b cookies.txt http://localhost:8000/dashboard
```

### Expected Result:
- Status: 200
- Should show dashboard with:
  - Prospects count
  - Won deals count
  - Lost deals count
  - Total revenue
  - Total hours

## Test Clients Endpoint

### Using Python requests:
```python
import requests

session = requests.Session()

# Login
session.post(
    "http://localhost:8000/login",
    data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"}
)

# Get clients list
clients_response = session.get("http://localhost:8000/clients")
print(f"Status: {clients_response.status_code}")
print(f"Has clients data: {'clients_with_revenue' in clients_response.text}")
```

### Using cURL:
```bash
curl -b cookies.txt "http://localhost:8000/clients"
```

### With Filters:
```bash
# Search
curl -b cookies.txt "http://localhost:8000/clients?search=Acme"

# Filter by status
curl -b cookies.txt "http://localhost:8000/clients?status=Active"

# Sort
curl -b cookies.txt "http://localhost:8000/clients?sort_by=name&sort_order=desc"
```

### Expected Result:
- Status: 200
- Should show clients list with:
  - Client names
  - Revenue for each client
  - Timesheet hours
  - Filter options

## Test Prospects Endpoint

### Using Python requests:
```python
import requests

session = requests.Session()

# Login
session.post(
    "http://localhost:8000/login",
    data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"}
)

# Get prospects list
prospects_response = session.get("http://localhost:8000/prospects")
print(f"Status: {prospects_response.status_code}")
print(f"Has prospects data: {'prospects' in prospects_response.text}")
```

### Using cURL:
```bash
curl -b cookies.txt "http://localhost:8000/prospects"
```

### With Filters:
```bash
# Filter by stage
curl -b cookies.txt "http://localhost:8000/prospects?stage=New"

# Filter by owner
curl -b cookies.txt "http://localhost:8000/prospects?owner=Paul"

# Search
curl -b cookies.txt "http://localhost:8000/prospects?search=Corp"
```

### Expected Result:
- Status: 200
- Should show prospects list with:
  - Prospect names
  - Estimated revenue
  - Stage (New, Contacted, Proposal, Negotiation)
  - Expected close date
  - Pipeline totals

## Test Timesheets Endpoint

### Using Python requests:
```python
import requests

session = requests.Session()

# Login
session.post(
    "http://localhost:8000/login",
    data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"}
)

# Get timesheets list
timesheets_response = session.get("http://localhost:8000/timesheets")
print(f"Status: {timesheets_response.status_code}")
print(f"Has timesheets data: {'timesheets' in timesheets_response.text}")
```

### Using cURL:
```bash
curl -b cookies.txt "http://localhost:8000/timesheets"
```

### With Filters:
```bash
# Filter by client
curl -b cookies.txt "http://localhost:8000/timesheets?client_id=1"

# Filter by date range
curl -b cookies.txt "http://localhost:8000/timesheets?date_from=2025-01-01&date_to=2025-01-31"

# Search
curl -b cookies.txt "http://localhost:8000/timesheets?search=tax"
```

### Expected Result:
- Status: 200
- Should show timesheets list with:
  - Time entries
  - Client names
  - Hours worked
  - Billable status
  - Summary statistics (week, month, total)

## Quick Test Script

Save as `test_all_endpoints.py`:

```python
#!/usr/bin/env python3
"""Quick test script for all fixed endpoints."""
import requests

BASE_URL = "http://localhost:8000"
session = requests.Session()

# Login
print("Logging in...")
login = session.post(
    f"{BASE_URL}/login",
    data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"}
)
print(f"Login: {login.status_code}")

# Test endpoints
endpoints = [
    "/dashboard",
    "/clients",
    "/prospects",
    "/timesheets"
]

for endpoint in endpoints:
    response = session.get(f"{BASE_URL}{endpoint}")
    status = "✓" if response.status_code == 200 else "✗"
    print(f"{status} {endpoint}: {response.status_code} ({len(response.text)} bytes)")

print("\nAll tests complete!")
```

Run with:
```bash
python test_all_endpoints.py
```

## Troubleshooting

### If dashboard shows empty data:
1. Check database has clients: `db.query(Client).count()`
2. Check logs for errors
3. Verify client status values are correct

### If clients tab gives error:
1. Check logs for specific error message
2. Verify `get_clients()` function works
3. Check database connection

### If prospects tab doesn't work:
1. Verify clients have status="Prospect"
2. Check `calculate_client_revenue()` function
3. Review logs for errors

### If timesheets tab gives error:
1. Check `current_user.name` is accessible (not `current_user.get("name")`)
2. Verify timesheets table exists
3. Check logs for database errors

