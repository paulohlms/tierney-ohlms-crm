#!/bin/bash
# Test /dashboard endpoint using curl with session handling

BASE_URL="http://localhost:8000"
LOGIN_URL="${BASE_URL}/login"
DASHBOARD_URL="${BASE_URL}/dashboard"

# Admin credentials
EMAIL="admin@tierneyohlms.com"
PASSWORD="ChangeMe123!"

echo "============================================================"
echo "Testing /dashboard Endpoint with curl"
echo "============================================================"
echo ""

# Step 1: Login and capture session cookie
echo "[1] Logging in..."
LOGIN_RESPONSE=$(curl -s -c cookies.txt -b cookies.txt \
    -X POST \
    -d "email=${EMAIL}" \
    -d "password=${PASSWORD}" \
    -L \
    -w "\nHTTP_CODE:%{http_code}" \
    "${LOGIN_URL}")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
echo "    Login HTTP Code: ${HTTP_CODE}"

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "303" ]; then
    echo "    [OK] Login successful"
else
    echo "    [ERROR] Login failed"
    exit 1
fi

# Step 2: Access Dashboard with session cookie
echo ""
echo "[2] Accessing /dashboard..."
DASHBOARD_RESPONSE=$(curl -s -b cookies.txt \
    -w "\nHTTP_CODE:%{http_code}" \
    "${DASHBOARD_URL}")

HTTP_CODE=$(echo "$DASHBOARD_RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
CONTENT=$(echo "$DASHBOARD_RESPONSE" | sed 's/HTTP_CODE:[0-9]*$//')

echo "    Dashboard HTTP Code: ${HTTP_CODE}"
echo "    Content Length: $(echo "$CONTENT" | wc -c) bytes"

if [ "$HTTP_CODE" = "200" ]; then
    # Check for errors
    if echo "$CONTENT" | grep -q "UnicodeDecodeError"; then
        echo "    [ERROR] UnicodeDecodeError found in response!"
        exit 1
    elif echo "$CONTENT" | grep -q "Internal Server Error"; then
        echo "    [ERROR] Internal Server Error found!"
        exit 1
    elif echo "$CONTENT" | grep -q "Dashboard"; then
        echo "    [OK] Dashboard loaded successfully"
        echo ""
        echo "============================================================"
        echo "[SUCCESS] Dashboard endpoint test passed!"
        echo "============================================================"
    else
        echo "    [WARN] Unexpected content"
        exit 1
    fi
else
    echo "    [ERROR] Dashboard request failed"
    echo "    Response: ${CONTENT:0:500}"
    exit 1
fi

# Cleanup
rm -f cookies.txt

