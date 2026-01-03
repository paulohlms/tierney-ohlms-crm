#!/usr/bin/env python3
"""
Test script for /dashboard endpoint after login.

This script:
1. Logs in with admin credentials
2. Captures the session cookie
3. Accesses the /dashboard endpoint
4. Reports success/failure with details

Requires: pip install requests
Alternative: Use test_dashboard_simple.py (no dependencies)
"""

try:
    import requests
except ImportError:
    print("ERROR: 'requests' module not found!")
    print("Install it with: pip install requests")
    print("Or use test_dashboard_simple.py (no dependencies)")
    sys.exit(1)

import sys
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:8000"  # Change if your server runs on different port
LOGIN_URL = urljoin(BASE_URL, "/login")
DASHBOARD_URL = urljoin(BASE_URL, "/dashboard")

# Default admin credentials (from bootstrap_admin_users)
ADMIN_EMAIL = "admin@tierneyohlms.com"
ADMIN_PASSWORD = "ChangeMe123!"

def test_dashboard_endpoint():
    """Test the dashboard endpoint with proper session handling."""
    print("=" * 70)
    print("Testing /dashboard Endpoint")
    print("=" * 70)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Login
    print(f"\n[1] Logging in as {ADMIN_EMAIL}...")
    try:
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        login_response = session.post(
            LOGIN_URL,
            data=login_data,
            allow_redirects=False,  # Don't follow redirects automatically
            timeout=10
        )
        
        print(f"    Status Code: {login_response.status_code}")
        print(f"    Headers: {dict(login_response.headers)}")
        
        # Check if login was successful (should redirect to /dashboard)
        if login_response.status_code == 303:
            redirect_location = login_response.headers.get('Location', '')
            print(f"    Redirect Location: {redirect_location}")
            if '/dashboard' in redirect_location:
                print("    [OK] Login successful - redirected to dashboard")
            else:
                print(f"    [WARN] Unexpected redirect: {redirect_location}")
        elif login_response.status_code == 200:
            # Check if we got an error page
            if 'error' in login_response.text.lower():
                print("    [ERROR] Login failed - error in response")
                print(f"    Response preview: {login_response.text[:200]}")
                return False
            else:
                print("    [OK] Login successful - got 200 response")
        else:
            print(f"    [ERROR] Unexpected status code: {login_response.status_code}")
            print(f"    Response: {login_response.text[:500]}")
            return False
        
        # Check session cookie
        cookies = session.cookies.get_dict()
        print(f"    Session Cookies: {cookies}")
        
        if not cookies:
            print("    [WARN] No session cookies found - authentication may have failed")
        
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] Login request failed: {e}")
        return False
    
    # Step 2: Access Dashboard
    print(f"\n[2] Accessing /dashboard endpoint...")
    try:
        dashboard_response = session.get(
            DASHBOARD_URL,
            timeout=10,
            allow_redirects=False
        )
        
        print(f"    Status Code: {dashboard_response.status_code}")
        print(f"    Content-Type: {dashboard_response.headers.get('Content-Type', 'unknown')}")
        print(f"    Content Length: {len(dashboard_response.content)} bytes")
        
        # Check response
        if dashboard_response.status_code == 200:
            # Check for encoding errors in response
            try:
                content = dashboard_response.text
                print("    [OK] Dashboard loaded successfully")
                
                # Check for common error indicators
                if 'UnicodeDecodeError' in content:
                    print("    [ERROR] UnicodeDecodeError found in response!")
                    return False
                elif 'Internal Server Error' in content:
                    print("    [ERROR] Internal Server Error in response!")
                    return False
                elif 'Error in dashboard' in content:
                    print("    [ERROR] Dashboard error message found!")
                    return False
                elif 'Dashboard' in content or 'dashboard' in content.lower():
                    print("    [OK] Dashboard content appears valid")
                    
                    # Check if it extends base.html (should have nav, etc.)
                    if 'navbar' in content or 'nav' in content.lower():
                        print("    [OK] Base template structure found")
                    else:
                        print("    [WARN] Base template structure not found")
                    
                    return True
                else:
                    print("    [WARN] Unexpected content - may have been redirected")
                    print(f"    Content preview: {content[:200]}")
                    return False
                    
            except UnicodeDecodeError as e:
                print(f"    [ERROR] UnicodeDecodeError when reading response: {e}")
                print(f"    Response bytes (first 100): {dashboard_response.content[:100]}")
                return False
                
        elif dashboard_response.status_code == 303:
            redirect_location = dashboard_response.headers.get('Location', '')
            print(f"    [WARN] Redirected to: {redirect_location}")
            if '/login' in redirect_location:
                print("    [ERROR] Redirected to login - session may have expired or authentication failed")
            return False
        else:
            print(f"    [ERROR] Unexpected status code: {dashboard_response.status_code}")
            print(f"    Response: {dashboard_response.text[:500]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] Dashboard request failed: {e}")
        return False

def main():
    """Main test function."""
    print(f"\nTesting against: {BASE_URL}")
    print(f"Make sure your server is running: uvicorn main:app --reload\n")
    
    success = test_dashboard_endpoint()
    
    print("\n" + "=" * 70)
    if success:
        print("[SUCCESS] Dashboard endpoint test passed!")
        sys.exit(0)
    else:
        print("[FAILURE] Dashboard endpoint test failed!")
        print("\nNext steps:")
        print("1. Check server logs for errors")
        print("2. Verify template encoding (run: python fix_all_templates_encoding.py)")
        print("3. Use VS Code debugger (see .vscode/launch.json)")
        sys.exit(1)

if __name__ == "__main__":
    main()

