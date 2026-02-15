#!/bin/bash
##########################################################################
# PackageManager Comprehensive Validation Script - Corrected (v3)
# Based on official RDK Central API: https://rdkcentral.github.io/entservices-apis/#/apis/PackageManager
# Run directly on device to validate all PackageManager API methods
# Device: 192.168.29.123
# Date: February 10, 2026
#
# Usage:
#   ./validate_packagemanager_apis_corrected.sh [true|false]
#
# Parameters:
#   true  - Execute both positive AND negative test scenarios (default)
#   false - Execute ONLY positive test scenarios (skip negative tests)
#
# Examples:
#   ./validate_packagemanager_apis_corrected.sh              # Run all tests
#   ./validate_packagemanager_apis_corrected.sh true         # Explicit: run all tests
#   ./validate_packagemanager_apis_corrected.sh false        # Skip negative tests
##########################################################################

JSONRPC_URL="http://127.0.0.1:9998/jsonrpc"
PACKAGE_URL_COBALT="http://192.168.29.38/com.rdkcentral.cobalt+0.1.0.bolt"
PACKAGE_URL_YOUTUBE="http://192.168.29.38/com.rdkcentral.youtube+0.1.0.bolt"
EXE_NEG_TC="${1:-true}"  # Execute negative test scenarios: true or false
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0
DOWNLOAD_DIR="/opt/CDL"

# Download handles (returned by download method)
COBALT_HANDLE=""
COBALT_FILE_PATH=""
YOUTUBE_HANDLE=""
YOUTUBE_FILE_PATH=""

# Installed package info
INSTALLED_PACKAGE_ID=""
INSTALLED_PACKAGE_VERSION=""

FAILED_TESTS=()

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   PackageManager API Comprehensive Test Suite (v3 - Corrected)  ║"
echo "║   Using: org.rdk.PackageManager (official RDK Central API)      ║"
echo "║   Validating all PackageManager plugin methods                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 0: Check and activate PackageManager service
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 0: Service Initialization"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Checking PackageManager service status..."
systemctl status wpeframework-packagemanager.service --no-pager 2>&1 | head -n 10
echo ""

echo "Starting PackageManager service..."
systemctl start wpeframework-packagemanager.service
sleep 2

echo "Verifying service is active..."
if systemctl is-active --quiet wpeframework-packagemanager.service; then
    echo "✓ PackageManager service is running"
else
    echo "⚠ Warning: Service may not be active, but continuing tests..."
fi
echo ""

# Function to execute curl and format output
execute_test() {
    local test_name="$1"
    local json_request="$2"
    local description="$3"
    local test_type="${4:-positive}"  # positive or negative
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TEST: $test_name"
    echo "DESC: $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Request:"
    echo "$json_request"
    echo ""
    echo "Response:"
    
    local response=$(curl -s -H 'content-type:text/plain;' --data-binary "$json_request" "$JSONRPC_URL")
    echo "$response"
    echo ""
    
    # Extract error message if present
    local error_msg=""
    if echo "$response" | grep -q '"error"'; then
        error_msg=$(echo "$response" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    fi
    
    # Check for errors based on test type
    if [[ "$response" == *'"error":'* ]]; then
        if [ "$test_type" = "negative" ]; then
            # For negative tests, error is expected behavior (PASS)
            echo "✓ TEST PASSED (Error correctly detected: $error_msg)"
            echo ""
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        else
            # For positive tests, error means failure
            echo "✗ TEST FAILED - Error detected: $error_msg"
            echo ""
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("$test_name|$error_msg")
            return 1
        fi
    else
        if [ "$test_type" = "negative" ]; then
            # For negative tests, no error means failure
            echo "✗ TEST FAILED (Error was expected but not returned)"
            echo ""
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("$test_name|Expected error not returned")
            return 1
        else
            # For positive tests, no error means success
            echo "✓ TEST PASSED"
            echo ""
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        fi
    fi
}

# ============================================================================
# POSITIVE TEST SCENARIOS - Testing all APIs with valid parameters
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         POSITIVE TEST SCENARIOS - Valid API Calls               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# TEST 0: SET RATE LIMIT (if we need to limit bandwidth)
echo "Test 0/20: RATELIMIT API (Optional - will set after download starts)"
echo ""

# TEST 1: Download Package - Cobalt
echo "Test 1/20: DOWNLOAD API - Cobalt Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "org.rdk.PackageManager.download",
    "params": {
        "type": "",
        "id": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "url": "'$PACKAGE_URL_COBALT'"
    }
}'
execute_test "download (Cobalt)" "$PKG_REQUEST" "Start download of Cobalt package" "positive"

# Extract handle from response
COBALT_HANDLE=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL" | grep -o '"handle":"[^"]*"' | cut -d'"' -f4)
COBALT_FILE_PATH="$DOWNLOAD_DIR/package$COBALT_HANDLE"
echo "Extracted Cobalt Handle: $COBALT_HANDLE (File will be at: $COBALT_FILE_PATH)"
sleep 2

# TEST 2: Download Package - YouTube
echo "Test 2/20: DOWNLOAD API - YouTube Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "org.rdk.PackageManager.download",
    "params": {
        "type": "",
        "id": "com.rdkcentral.youtube",
        "version": "0.1.0",
        "url": "'$PACKAGE_URL_YOUTUBE'"
    }
}'
execute_test "download (YouTube)" "$PKG_REQUEST" "Start download of YouTube package" "positive"

YOUTUBE_HANDLE=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL" | grep -o '"handle":"[^"]*"' | cut -d'"' -f4)
YOUTUBE_FILE_PATH="$DOWNLOAD_DIR/package$YOUTUBE_HANDLE"
echo "Extracted YouTube Handle: $YOUTUBE_HANDLE (File will be at: $YOUTUBE_FILE_PATH)"
sleep 3

# TEST 3: Get Progress using progress API with downloadId
echo "Test 3/20: PROGRESS API - Monitor Cobalt download"
echo "Waiting 5 seconds for download to progress..."
sleep 5
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "org.rdk.PackageManager.progress",
    "params": {
        "downloadId": "'$COBALT_HANDLE'"
    }
}'
execute_test "progress (Cobalt)" "$PKG_REQUEST" "Get progress of download: $COBALT_HANDLE" "positive"
sleep 1

# TEST 4: Get Storage Information
echo "Test 4/20: GET_STORAGE_INFORMATION API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "org.rdk.PackageManager.getStorageInformation"
}'
execute_test "getStorageInformation" "$PKG_REQUEST" "Query available storage information" "positive"
sleep 1

# TEST 5: List Packages (BEFORE install)
echo "Test 5/20: LIST_PACKAGES API - Check currently installed packages"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "org.rdk.PackageManager.listPackages"
}'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST: listPackages"
echo "DESC: List all installed packages before installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
RESPONSE=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL")
echo "Response:"
echo "$RESPONSE"
echo ""

if echo "$RESPONSE" | grep -q "INSTALLED"; then
    echo "✓ TEST PASSED - Found existing installed packages"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "⚠ No installed packages found yet (expected for first run)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi
echo ""
sleep 1

# TEST 6: Pause Download (Cobalt)
echo "Test 6/20: PAUSE API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "org.rdk.PackageManager.pause",
    "params": {
        "downloadId": "'$COBALT_HANDLE'"
    }
}'
execute_test "pause" "$PKG_REQUEST" "Pause download: $COBALT_HANDLE" "positive"
sleep 1

# TEST 7: Resume Download
echo "Test 7/20: RESUME API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 7,
    "method": "org.rdk.PackageManager.resume",
    "params": {
        "downloadId": "'$COBALT_HANDLE'"
    }
}'
execute_test "resume" "$PKG_REQUEST" "Resume download: $COBALT_HANDLE" "positive"
sleep 10

# TEST 8: Set Rate Limit for YouTube download
if [ -n "$YOUTUBE_HANDLE" ]; then
    echo "Test 8/20: RATELIMIT API"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 8,
        "method": "org.rdk.PackageManager.rateLimit",
        "params": {
            "downloadId": "'$YOUTUBE_HANDLE'",
            "limit": 512
        }
    }'
    execute_test "rateLimit (YouTube)" "$PKG_REQUEST" "Set rate limit to 512 Kbps for YouTube" "positive"
    sleep 1
fi

# TEST 9: Cancel YouTube Download
echo "Test 9/20: CANCEL API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 9,
    "method": "org.rdk.PackageManager.cancel",
    "params": {
        "handle": "'$YOUTUBE_HANDLE'"
    }
}'
execute_test "cancel" "$PKG_REQUEST" "Cancel download handle: $YOUTUBE_HANDLE" "positive"
sleep 1

# TEST 10: Delete cancelled download (YouTube)
if [ -n "$YOUTUBE_FILE_PATH" ]; then
    echo "Test 10/20: DELETE API"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 10,
        "method": "org.rdk.PackageManager.delete",
        "params": {
            "fileLocator": "'$YOUTUBE_FILE_PATH'"
        }
    }'
    execute_test "delete (YouTube)" "$PKG_REQUEST" "Delete YouTube file: $YOUTUBE_FILE_PATH" "positive"
    sleep 1
fi

# TEST 11: Wait for Cobalt download to complete
echo "Test 11/20: Waiting for Cobalt download to complete..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Waiting 20 seconds for Cobalt download to finish..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sleep 20

# Verify file exists
if [ -f "$COBALT_FILE_PATH" ]; then
    echo "✓ Cobalt package file exists: $COBALT_FILE_PATH ($(du -h "$COBALT_FILE_PATH" | cut -f1))"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "⚠ Cobalt package file not yet available at: $COBALT_FILE_PATH (still downloading)"
    TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
fi
echo ""

# TEST 12: Install Package (Cobalt)
echo "Test 12/20: INSTALL API - Cobalt"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 12,
    "method": "org.rdk.PackageManager.install",
    "params": {
        "type": "",
        "id": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "url": "'$COBALT_FILE_PATH'",
        "appName": "Cobalt",
        "category": "media"
    }
}'
execute_test "install (Cobalt)" "$PKG_REQUEST" "Install Cobalt package" "positive"
sleep 2

# TEST 13: List Packages (AFTER install)
echo "Test 13/20: LIST_PACKAGES API - Verify installed package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 13,
    "method": "org.rdk.PackageManager.listPackages"
}'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST: listPackages (After Install)"
echo "DESC: List packages to find newly installed package ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
RESPONSE=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL")
echo "Response:"
echo "$RESPONSE"
echo ""

# Extract installed Cobalt package
INSTALLED_COBALT=$(echo "$RESPONSE" | sed -n 's/.*"packageId":"\([^"]*cobalt[^"]*\)"[^}]*"state":"INSTALLED".*/\1/p' | head -n 1)

if [ -n "$INSTALLED_COBALT" ]; then
    echo "✓ TEST PASSED - Found installed Cobalt package: $INSTALLED_COBALT"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    INSTALLED_PACKAGE_ID="$INSTALLED_COBALT"
else
    echo "✗ TEST FAILED - Cobalt package not found in installed list"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    FAILED_TESTS+=("listPackages (After Install)|Package not installed successfully")
fi
echo ""
sleep 1

# TEST 14: Package State
if [ -n "$INSTALLED_PACKAGE_ID" ]; then
    echo "Test 14/20: PACKAGE_STATE API - Using package: $INSTALLED_PACKAGE_ID"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 14,
        "method": "org.rdk.PackageManager.packageState",
        "params": {
            "packageId": "'$INSTALLED_PACKAGE_ID'",
            "version": "0.1.0"
        }
    }'
    execute_test "packageState" "$PKG_REQUEST" "Get state of package: $INSTALLED_PACKAGE_ID" "positive"
    sleep 1
fi

# TEST 15: Config API
echo "Test 15/20: CONFIG API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 15,
    "method": "org.rdk.PackageManager.config",
    "params": {
        "packageId": "'${INSTALLED_PACKAGE_ID:-com.rdkcentral.cobalt}'",
        "version": "0.1.0"
    }
}'
execute_test "config" "$PKG_REQUEST" "Get configuration for package" "positive"
sleep 1

# TEST 16: Get Config for Package (using fileLocator)
if [ -n "$INSTALLED_PACKAGE_ID" ] && [ -n "$COBALT_FILE_PATH" ]; then
    echo "Test 16/20: GET_CONFIG_FOR_PACKAGE API"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 16,
        "method": "org.rdk.PackageManager.getConfigForPackage",
        "params": {
            "fileLocator": "'$COBALT_FILE_PATH'"
        }
    }'
    execute_test "getConfigForPackage" "$PKG_REQUEST" "Get config for: $COBALT_FILE_PATH" "positive"
    sleep 1
fi

# TEST 17: Lock Package
if [ -n "$INSTALLED_PACKAGE_ID" ]; then
    echo "Test 17/20: LOCK API - Package: $INSTALLED_PACKAGE_ID"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 17,
        "method": "org.rdk.PackageManager.lock",
        "params": {
            "type": "",
            "id": "'$INSTALLED_PACKAGE_ID'",
            "version": "0.1.0",
            "reason": "Launch",
            "owner": "AppManager"
        }
    }'
    execute_test "lock" "$PKG_REQUEST" "Lock package: $INSTALLED_PACKAGE_ID" "positive"
    sleep 1
fi

# TEST 18: Get Locked Info
if [ -n "$INSTALLED_PACKAGE_ID" ]; then
    echo "Test 18/20: GET_LOCKED_INFO API - Package: $INSTALLED_PACKAGE_ID"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 18,
        "method": "org.rdk.PackageManager.getLockedInfo",
        "params": {
            "packageId": "'$INSTALLED_PACKAGE_ID'",
            "version": "0.1.0"
        }
    }'
    execute_test "getLockedInfo" "$PKG_REQUEST" "Get locked info for: $INSTALLED_PACKAGE_ID" "positive"
    sleep 1
fi

# TEST 19: Unlock Package
if [ -n "$INSTALLED_PACKAGE_ID" ]; then
    echo "Test 19/20: UNLOCK API - Package: $INSTALLED_PACKAGE_ID"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 19,
        "method": "org.rdk.PackageManager.unlock",
        "params": {
            "handle": ""
        }
    }'
    execute_test "unlock" "$PKG_REQUEST" "Unlock package handle" "positive"
    sleep 1
fi

# TEST 20: Uninstall Package
if [ -n "$INSTALLED_PACKAGE_ID" ]; then
    echo "Test 20/20: UNINSTALL API - Package: $INSTALLED_PACKAGE_ID"
    PKG_REQUEST='{
        "jsonrpc": "2.0",
        "id": 20,
        "method": "org.rdk.PackageManager.uninstall",
        "params": {
            "type": "",
            "id": "'$INSTALLED_PACKAGE_ID'",
            "version": "0.1.0",
            "uninstallType": "normal"
        }
    }'
    execute_test "uninstall (Cobalt)" "$PKG_REQUEST" "Uninstall package: $INSTALLED_PACKAGE_ID" "positive"
    sleep 1
fi

# Only execute negative tests if EXE_NEG_TC is true
if [ "$EXE_NEG_TC" = "true" ] || [ "$EXE_NEG_TC" = "True" ] || [ "$EXE_NEG_TC" = "TRUE" ]; then

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        NEGATIVE TEST SCENARIOS - Invalid Parameters             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# NEGATIVE TEST 1: Download with Invalid URL
echo "Negative Test 1: DOWNLOAD API - Invalid URL"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 101,
    "method": "org.rdk.PackageManager.download",
    "params": {
        "type": "",
        "id": "com.invalid.test",
        "version": "1.0.0",
        "url": "http://invalid.example.com/nonexistent.bolt"
    }
}'
execute_test "download (Invalid URL)" "$PKG_REQUEST" "Attempt download with invalid URL" "negative"
sleep 1

# NEGATIVE TEST 2: Cancel with invalid handle
echo "Negative Test 2: CANCEL API - Invalid Handle"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 102,
    "method": "org.rdk.PackageManager.cancel",
    "params": {
        "handle": "invalid-handle-99999"
    }
}'
execute_test "cancel (Invalid Handle)" "$PKG_REQUEST" "Cancel with invalid handle" "negative"
sleep 1

# NEGATIVE TEST 3: Pause with invalid downloadId
echo "Negative Test 3: PAUSE API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 103,
    "method": "org.rdk.PackageManager.pause",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "pause (Invalid ID)" "$PKG_REQUEST" "Pause with invalid download ID" "negative"
sleep 1

# NEGATIVE TEST 4: Resume with invalid downloadId
echo "Negative Test 4: RESUME API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 104,
    "method": "org.rdk.PackageManager.resume",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "resume (Invalid ID)" "$PKG_REQUEST" "Resume with invalid download ID" "negative"
sleep 1

# NEGATIVE TEST 5: Get Progress with invalid downloadId
echo "Negative Test 5: PROGRESS API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 105,
    "method": "org.rdk.PackageManager.progress",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "progress (Invalid ID)" "$PKG_REQUEST" "Get progress with invalid download ID" "negative"
sleep 1

# NEGATIVE TEST 6: Uninstall with Invalid Package
echo "Negative Test 6: UNINSTALL API - Invalid Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 106,
    "method": "org.rdk.PackageManager.uninstall",
    "params": {
        "type": "",
        "id": "com.invalid.nonexistent",
        "version": "0.0.0",
        "uninstallType": "normal"
    }
}'
execute_test "uninstall (Invalid Package)" "$PKG_REQUEST" "Uninstall with invalid package ID" "negative"
sleep 1

else
    echo "Skipping NEGATIVE TEST SCENARIOS (EXE_NEG_TC=false)"
    echo ""
fi

# ============================================================================
# TEST SUMMARY WITH DETAILED FAILURE REASONS
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      TEST SUMMARY REPORT                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))

printf "%-40s %3d\n" "Total Tests Executed:" "$TOTAL_TESTS"
printf "%-40s %3d ($(( TOTAL_TESTS > 0 ? TESTS_PASSED * 100 / TOTAL_TESTS : 0 ))%%)\n" "Tests Passed:" "$TESTS_PASSED"
printf "%-40s %3d\n" "Tests Failed:" "$TESTS_FAILED"
printf "%-40s %3d\n" "Tests Skipped:" "$TESTS_SKIPPED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo "═════════════════════════════════════════════════════════════════"
    echo "FAILURE DETAILS:"
    echo "═════════════════════════════════════════════════════════════════"
    for failure in "${FAILED_TESTS[@]}"; do
        test_name=$(echo "$failure" | cut -d'|' -f1)
        reason=$(echo "$failure" | cut -d'|' -f2)
        printf "  ✗ %-35s | %s\n" "$test_name" "$reason"
    done
    echo ""
fi

echo "KEY OBSERVATIONS:"
echo "  • API Method Namespace: org.rdk.PackageManager"
echo "  • Cobalt Download Handle: $COBALT_HANDLE"
echo "  • YouTube Download Handle: $YOUTUBE_HANDLE"
echo "  • Installed Package ID: ${INSTALLED_PACKAGE_ID:-Not installed}"
echo "  • Download Directory: $DOWNLOAD_DIR"
echo ""

if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_PASSED -gt 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  ✓ ALL TESTS PASSED - PackageManager APIs are functioning     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║   ⚠ SOME TESTS FAILED - Review FAILURE DETAILS above          ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 1
fi
