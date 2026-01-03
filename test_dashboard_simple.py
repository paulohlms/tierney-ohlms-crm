#!/usr/bin/env python3
"""
Simple test script for /dashboard endpoint using only built-in libraries.

No external dependencies required - uses urllib which is built into Python.
"""

import urllib.request
import urllib.parse
import http.cookiejar
import sys

# Configuration
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"

# Default admin credentials
ADMIN_EMAIL = "admin@tierneyohlms.com"
ADMIN_PASSWORD = "ChangeMe123!"

def test_dashboard_endpoint():
    """Test the dashboard endpoint with proper session handling."""
    print("=" * 70)
    print("Testing /dashboard Endpoint (using built-in libraries)")
    print("=" * 70)
    
    # Create cookie jar to maintain session
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    
    # Step 1: Login
    print(f"\n[1] Logging in as {ADMIN_EMAIL}...")
    try:
        login_data = urllib.parse.urlencode({
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }).encode('utf-8')
        
        login_request = urllib.request.Request(
            LOGIN_URL,
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        login_response = opener.open(login_request, timeout=10)
        status_code = login_response.getcode()
        
        print(f"    Status Code: {status_code}")
        print(f"    Response URL: {login_response.geturl()}")
        
        # Check cookies
        cookies = [cookie.name for cookie in cookie_jar]
        print(f"    Session Cookies: {cookies}")
        
        if status_code in [200, 303]:
            if '/dashboard' in login_response.geturl() or status_code == 303:
                print("    [OK] Login successful")
            else:
                # Read response to check for errors
                response_text = login_response.read().decode('utf-8', errors='ignore')
                if 'error' in response_text.lower():
                    print("    [ERROR] Login failed - error in response")
                    print(f"    Response preview: {response_text[:200]}")
                    return False
                else:
                    print("    [OK] Login successful")
        else:
            print(f"    [ERROR] Unexpected status code: {status_code}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"    [ERROR] Login HTTP error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"    [ERROR] Login request failed: {e}")
        return False
    
    # Step 2: Access Dashboard
    print(f"\n[2] Accessing /dashboard endpoint...")
    try:
        dashboard_request = urllib.request.Request(DASHBOARD_URL)
        dashboard_response = opener.open(dashboard_request, timeout=10)
        status_code = dashboard_response.getcode()
        content = dashboard_response.read()
        
        print(f"    Status Code: {status_code}")
        print(f"    Content Length: {len(content)} bytes")
        
        if status_code == 200:
            # Decode content
            try:
                content_text = content.decode('utf-8')
                print("    [OK] Dashboard loaded successfully")
                
                # Check for common error indicators
                if 'UnicodeDecodeError' in content_text:
                    print("    [ERROR] UnicodeDecodeError found in response!")
                    return False
                elif 'Internal Server Error' in content_text:
                    print("    [ERROR] Internal Server Error in response!")
                    return False
                elif 'Error in dashboard' in content_text:
                    print("    [ERROR] Dashboard error message found!")
                    return False
                elif 'Dashboard' in content_text or 'dashboard' in content_text.lower():
                    print("    [OK] Dashboard content appears valid")
                    
                    # Check if it extends base.html
                    if 'navbar' in content_text or 'nav' in content_text.lower():
                        print("    [OK] Base template structure found")
                    else:
                        print("    [WARN] Base template structure not found")
                    
                    return True
                else:
                    print("    [WARN] Unexpected content")
                    print(f"    Content preview: {content_text[:200]}")
                    return False
                    
            except UnicodeDecodeError as e:
                print(f"    [ERROR] UnicodeDecodeError when reading response: {e}")
                print(f"    Response bytes (first 100): {content[:100]}")
                return False
        else:
            print(f"    [ERROR] Unexpected status code: {status_code}")
            try:
                error_text = content.decode('utf-8', errors='ignore')
                print(f"    Response: {error_text[:500]}")
            except:
                print(f"    Response (raw): {content[:500]}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"    [ERROR] Dashboard HTTP error: {e.code} - {e.reason}")
        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            print(f"    Error response: {error_content[:500]}")
        except:
            pass
        return False
    except Exception as e:
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
        print("3. Use VS Code debugger (see DEBUG_DASHBOARD.md)")
        sys.exit(1)

if __name__ == "__main__":
    main()

