"""
Verification script for dashboard error handling fix.

This script helps verify that the dashboard fix works correctly.
Run this after deployment to ensure the fix is working.

Usage:
    python verify_dashboard_fix.py
"""

import sys
import requests
from typing import Dict, List

# Configuration
BASE_URL = "https://tierney-ohlms-crm.onrender.com"  # Update for your deployment
LOGIN_EMAIL = "admin@tierneyohlms.com"
LOGIN_PASSWORD = "ChangeMe123!"


class DashboardVerification:
    """Verification tests for dashboard error handling."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.results: List[Dict] = []
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "message": message
        }
        self.results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_login(self) -> bool:
        """Test 1: Verify login works."""
        try:
            # Get login page first to establish session
            login_page = self.session.get(f"{self.base_url}/login")
            if login_page.status_code != 200:
                self.log_result("Login Page Access", False, f"Status: {login_page.status_code}")
                return False
            
            # Attempt login
            login_response = self.session.post(
                f"{self.base_url}/login",
                data={
                    "email": LOGIN_EMAIL,
                    "password": LOGIN_PASSWORD
                },
                allow_redirects=False
            )
            
            if login_response.status_code == 303:
                self.log_result("Login", True, "Login successful, redirected to dashboard")
                return True
            else:
                self.log_result("Login", False, f"Status: {login_response.status_code}")
                return False
        except Exception as e:
            self.log_result("Login", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_loads(self) -> bool:
        """Test 2: Verify dashboard loads successfully."""
        try:
            dashboard_response = self.session.get(f"{self.base_url}/dashboard")
            
            if dashboard_response.status_code == 200:
                # Check for error message
                if "An error occurred loading the dashboard" in dashboard_response.text:
                    self.log_result("Dashboard Loads", False, "Error message found in response")
                    return False
                
                # Check for dashboard content
                if "dashboard" in dashboard_response.text.lower() or "prospects" in dashboard_response.text.lower():
                    self.log_result("Dashboard Loads", True, "Dashboard rendered successfully")
                    return True
                else:
                    self.log_result("Dashboard Loads", False, "Dashboard content not found")
                    return False
            else:
                self.log_result("Dashboard Loads", False, f"Status: {dashboard_response.status_code}")
                return False
        except Exception as e:
            self.log_result("Dashboard Loads", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_no_error_message(self) -> bool:
        """Test 3: Verify dashboard doesn't show error message."""
        try:
            dashboard_response = self.session.get(f"{self.base_url}/dashboard")
            
            error_indicators = [
                "An error occurred loading the dashboard",
                "Please try logging in again",
                "Internal Server Error",
                "500",
            ]
            
            found_errors = []
            for indicator in error_indicators:
                if indicator in dashboard_response.text:
                    found_errors.append(indicator)
            
            if found_errors:
                self.log_result("No Error Message", False, f"Found: {', '.join(found_errors)}")
                return False
            else:
                self.log_result("No Error Message", True, "No error messages found")
                return True
        except Exception as e:
            self.log_result("No Error Message", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_has_content(self) -> bool:
        """Test 4: Verify dashboard has expected content sections."""
        try:
            dashboard_response = self.session.get(f"{self.base_url}/dashboard")
            
            expected_sections = [
                "clients",
                "revenue",
                "prospects",
            ]
            
            found_sections = []
            for section in expected_sections:
                if section.lower() in dashboard_response.text.lower():
                    found_sections.append(section)
            
            if len(found_sections) >= 2:  # At least 2 sections should be present
                self.log_result("Dashboard Content", True, f"Found sections: {', '.join(found_sections)}")
                return True
            else:
                self.log_result("Dashboard Content", False, f"Only found: {', '.join(found_sections)}")
                return False
        except Exception as e:
            self.log_result("Dashboard Content", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all verification tests."""
        print("=" * 60)
        print("Dashboard Fix Verification")
        print("=" * 60)
        print()
        
        # Test 1: Login
        if not self.test_login():
            print("\n❌ Login failed. Cannot continue with dashboard tests.")
            return False
        
        print()
        
        # Test 2-4: Dashboard tests
        self.test_dashboard_loads()
        self.test_dashboard_no_error_message()
        self.test_dashboard_has_content()
        
        print()
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        for result in self.results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['test']}")
            if result["message"]:
                print(f"   {result['message']}")
        
        print()
        print(f"Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n✅ All tests passed! Dashboard fix is working correctly.")
            return True
        else:
            print(f"\n❌ {total - passed} test(s) failed. Please review the results.")
            return False


def main():
    """Main entry point."""
    # Allow override of base URL via command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    
    print(f"Testing dashboard at: {base_url}")
    print(f"Login email: {LOGIN_EMAIL}")
    print()
    
    verifier = DashboardVerification(base_url)
    success = verifier.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

