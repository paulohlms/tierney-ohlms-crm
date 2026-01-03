#!/usr/bin/env python3
"""Quick test script for all fixed endpoints."""
import requests
import sys

BASE_URL = "http://localhost:8000"
session = requests.Session()

print("=" * 70)
print("Testing All Fixed Endpoints")
print("=" * 70)

# Login
print("\n[1] Logging in...")
try:
    login = session.post(
        f"{BASE_URL}/login",
        data={"email": "admin@tierneyohlms.com", "password": "ChangeMe123!"},
        allow_redirects=False
    )
    if login.status_code in [200, 303]:
        print(f"    ✓ Login successful: {login.status_code}")
    else:
        print(f"    ✗ Login failed: {login.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"    ✗ Login error: {e}")
    sys.exit(1)

# Test endpoints
endpoints = [
    ("/dashboard", "Dashboard"),
    ("/clients", "Clients"),
    ("/prospects", "Prospects"),
    ("/timesheets", "Timesheets")
]

print("\n[2] Testing endpoints...")
all_passed = True

for endpoint, name in endpoints:
    try:
        response = session.get(f"{BASE_URL}{endpoint}", allow_redirects=False)
        if response.status_code == 200:
            # Check for error indicators
            if "Internal Server Error" in response.text:
                print(f"    ✗ {name}: 200 but contains 'Internal Server Error'")
                all_passed = False
            elif "UnicodeDecodeError" in response.text:
                print(f"    ✗ {name}: 200 but contains 'UnicodeDecodeError'")
                all_passed = False
            else:
                print(f"    ✓ {name}: {response.status_code} ({len(response.text)} bytes)")
        elif response.status_code == 303:
            redirect = response.headers.get('Location', '')
            if '/login' in redirect:
                print(f"    ✗ {name}: Redirected to login (session issue)")
                all_passed = False
            else:
                print(f"    ⚠ {name}: Redirected to {redirect}")
        else:
            print(f"    ✗ {name}: {response.status_code}")
            all_passed = False
    except Exception as e:
        print(f"    ✗ {name}: Error - {e}")
        all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("[SUCCESS] All endpoints working correctly!")
    sys.exit(0)
else:
    print("[FAILURE] Some endpoints have issues. Check logs above.")
    sys.exit(1)

