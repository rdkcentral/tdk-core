#!/bin/bash
##########################################################################
# PackageManager Comprehensive Validation Script
# Run directly on device to validate all PackageManager API methods
# Device: 192.168.29.123
# Date: February 10, 2026
#
# Usage:
#   ./validate_all_packagemanager_apis.sh [true|false]
#
# Parameters:
#   true  - Execute both positive AND negative test scenarios (default)
#   false - Execute ONLY positive test scenarios (skip negative tests)
#
# Examples:
#   ./validate_all_packagemanager_apis.sh              # Run all tests
#   ./validate_all_packagemanager_apis.sh true         # Explicit: run all tests
#   ./validate_all_packagemanager_apis.sh false        # Skip negative tests
##########################################################################

JSONRPC_URL="http://127.0.0.1:9998/jsonrpc"
PACKAGE_URL_COBALT="http://192.168.29.38/com.rdkcentral.cobalt+0.1.0.bolt"
PACKAGE_URL_YOUTUBE="http://192.168.29.38/com.rdkcentral.youtube+0.1.0.bolt"
EXE_NEG_TC="${1:-true}"  # Execute negative test scenarios: true or false
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0
DOWNLOAD_DIR="/opt/CDL"
COBALT_DOWNLOAD_ID=""
COBALT_FILE_PATH=""
YOUTUBE_DOWNLOAD_ID=""
YOUTUBE_FILE_PATH=""
INSTALLED_PACKAGE_ID=""
FAILED_TESTS=()

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     PackageManager API Comprehensive Test Suite                ║"
echo "║      Validating all 17 PackageManager plugin methods            ║"
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
    
    # Check for errors based on test type
    if [[ "$response" == *'"error":'* ]]; then
        if [ "$test_type" = "negative" ]; then
            # For negative tests, error is expected behavior (PASS)
            echo "✓ TEST PASSED (Error correctly detected)"
            echo ""
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        else
            # For positive tests, error means failure
            echo "✗ TEST FAILED - Error detected"
            echo ""
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("$test_name")
            return 1
        fi
    else
        if [ "$test_type" = "negative" ]; then
            # For negative tests, no error means failure
            echo "✗ TEST FAILED (Error was expected but not returned)"
            echo ""
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("$test_name")
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
# POSITIVE TEST SCENARIOS - Testing all 17 APIs with valid parameters
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         POSITIVE TEST SCENARIOS - Valid API Calls               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# TEST 1: Download Package (API #1)
echo "Test 1/25: DOWNLOAD API - Cobalt Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "org.rdk.PackageManagerRDKEMS.download",
    "params": {
        "url": "'$PACKAGE_URL_COBALT'"
    }
}'
execute_test "download (Cobalt)" "$PKG_REQUEST" "Start download of Cobalt package" "positive"
COBALT_DOWNLOAD_ID=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL" | grep -o '"downloadId":"[^"]*"' | cut -d'"' -f4)
if [ -z "$COBALT_DOWNLOAD_ID" ]; then
    COBALT_DOWNLOAD_ID="1001"
fi

sleep 1

# TEST 2: Download Package - YouTube
echo "Test 2/25: DOWNLOAD API - YouTube Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "org.rdk.PackageManagerRDKEMS.download",
    "params": {
        "url": "'$PACKAGE_URL_YOUTUBE'"
    }
}'
execute_test "download (YouTube)" "$PKG_REQUEST" "Start download of YouTube package" "positive"
YOUTUBE_DOWNLOAD_ID=$(curl -s -H 'content-type:text/plain;' --data-binary "$PKG_REQUEST" "$JSONRPC_URL" | grep -o '"downloadId":"[^"]*"' | cut -d'"' -f4)
if [ -z "$YOUTUBE_DOWNLOAD_ID" ]; then
    YOUTUBE_DOWNLOAD_ID="1002"
fi

sleep 1

# TEST 3: Get Storage Information
echo "Test 3/25: GET_STORAGE_INFORMATION API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "org.rdk.PackageManagerRDKEMS.getStorageInformation",
    "params": {}
}'
execute_test "getStorageInformation" "$PKG_REQUEST" "Query available storage information" "positive"
sleep 1

# TEST 4: Get Progress
echo "Test 4/25: GET_PROGRESS API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "org.rdk.PackageManagerRDKEMS.getProgress",
    "params": {
        "downloadId": "'$COBALT_DOWNLOAD_ID'"
    }
}'
execute_test "getProgress" "$PKG_REQUEST" "Get progress of download ID: $COBALT_DOWNLOAD_ID" "positive"
sleep 1

# TEST 5: Pause Download
echo "Test 5/25: PAUSE API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "org.rdk.PackageManagerRDKEMS.pause",
    "params": {
        "downloadId": "'$COBALT_DOWNLOAD_ID'"
    }
}'
execute_test "pause" "$PKG_REQUEST" "Pause download ID: $COBALT_DOWNLOAD_ID" "positive"
sleep 1

# TEST 6: Resume Download
echo "Test 6/25: RESUME API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "org.rdk.PackageManagerRDKEMS.resume",
    "params": {
        "downloadId": "'$COBALT_DOWNLOAD_ID'"
    }
}'
execute_test "resume" "$PKG_REQUEST" "Resume download ID: $COBALT_DOWNLOAD_ID" "positive"
sleep 1

# TEST 7: Cancel Download
echo "Test 7/25: CANCEL API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 7,
    "method": "org.rdk.PackageManagerRDKEMS.cancel",
    "params": {
        "downloadId": "'$COBALT_DOWNLOAD_ID'"
    }
}'
execute_test "cancel" "$PKG_REQUEST" "Cancel download ID: $COBALT_DOWNLOAD_ID" "positive"
sleep 1

# TEST 8: Rate Limit
echo "Test 8/25: RATE_LIMIT API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 8,
    "method": "org.rdk.PackageManagerRDKEMS.rateLimit",
    "params": {
        "rateLimitKbps": 2048
    }
}'
execute_test "rateLimit" "$PKG_REQUEST" "Set rate limit to 2048 Kbps" "positive"
sleep 1

# TEST 9: Delete Download
echo "Test 9/25: DELETE API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 9,
    "method": "org.rdk.PackageManagerRDKEMS.delete",
    "params": {
        "downloadId": "'$YOUTUBE_DOWNLOAD_ID'"
    }
}'
execute_test "delete" "$PKG_REQUEST" "Delete download ID: $YOUTUBE_DOWNLOAD_ID" "positive"
sleep 1

# TEST 10: Install Package
echo "Test 10/25: INSTALL API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 10,
    "method": "org.rdk.PackageManagerRDKEMS.install",
    "params": {
        "packageId": "com.rdkcentral.cobalt",
        "version": "0.1.0",
        "fileLocator": "'$COBALT_DOWNLOAD_ID'"
    }
}'
execute_test "install" "$PKG_REQUEST" "Install Cobalt package" "positive"
sleep 1

# TEST 11: Uninstall Package
echo "Test 11/25: UNINSTALL API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 11,
    "method": "org.rdk.PackageManagerRDKEMS.uninstall",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "uninstall" "$PKG_REQUEST" "Uninstall Cobalt package" "positive"
sleep 1

# TEST 12: List Packages
echo "Test 12/25: LIST_PACKAGES API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 12,
    "method": "org.rdk.PackageManagerRDKEMS.listPackages",
    "params": {}
}'
execute_test "listPackages" "$PKG_REQUEST" "List all installed packages" "positive"
sleep 1

# TEST 13: Set Configuration
echo "Test 13/25: CONFIG API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 13,
    "method": "org.rdk.PackageManagerRDKEMS.config",
    "params": {
        "configKey": "testKey",
        "configValue": "testValue"
    }
}'
execute_test "config" "$PKG_REQUEST" "Set configuration parameter" "positive"
sleep 1

# TEST 14: Get Package State
echo "Test 14/25: PACKAGE_STATE API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 14,
    "method": "org.rdk.PackageManagerRDKEMS.packageState",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "packageState" "$PKG_REQUEST" "Get state of Cobalt package" "positive"
sleep 1

# TEST 15: Get Config for Package
echo "Test 15/25: GET_CONFIG_FOR_PACKAGE API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 15,
    "method": "org.rdk.PackageManagerRDKEMS.getConfigForPackage",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "getConfigForPackage" "$PKG_REQUEST" "Get configuration for Cobalt package" "positive"
sleep 1

# TEST 16: Lock Package
echo "Test 16/25: LOCK API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 16,
    "method": "org.rdk.PackageManagerRDKEMS.lock",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "lock" "$PKG_REQUEST" "Lock Cobalt package" "positive"
sleep 1

# TEST 17: Unlock Package
echo "Test 17/25: UNLOCK API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 17,
    "method": "org.rdk.PackageManagerRDKEMS.unlock",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "unlock" "$PKG_REQUEST" "Unlock Cobalt package" "positive"
sleep 1

# TEST 18: Get Locked Info
echo "Test 18/25: GET_LOCKED_INFO API"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 18,
    "method": "org.rdk.PackageManagerRDKEMS.getLockedInfo",
    "params": {
        "packageId": "com.rdkcentral.cobalt"
    }
}'
execute_test "getLockedInfo" "$PKG_REQUEST" "Get locked information for Cobalt" "positive"
sleep 1

# Only execute negative tests if EXE_NEG_TC is true
if [ "$EXE_NEG_TC" = "true" ] || [ "$EXE_NEG_TC" = "True" ] || [ "$EXE_NEG_TC" = "TRUE" ]; then

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        NEGATIVE TEST SCENARIOS - Invalid Parameters             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# TEST 19: Download with Invalid URL
echo "Test 19/25: DOWNLOAD API - Invalid URL"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 19,
    "method": "org.rdk.PackageManagerRDKEMS.download",
    "params": {
        "url": "http://invalid.example.com/nonexistent.bolt"
    }
}'
execute_test "download (Invalid URL)" "$PKG_REQUEST" "Attempt download with invalid URL" "negative"
sleep 1

# TEST 20: Get Progress with Invalid ID
echo "Test 20/25: GET_PROGRESS API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 20,
    "method": "org.rdk.PackageManagerRDKEMS.getProgress",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "getProgress (Invalid ID)" "$PKG_REQUEST" "Query progress with invalid download ID" "negative"
sleep 1

# TEST 21: Pause with Invalid ID
echo "Test 21/25: PAUSE API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 21,
    "method": "org.rdk.PackageManagerRDKEMS.pause",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "pause (Invalid ID)" "$PKG_REQUEST" "Pause with invalid download ID" "negative"
sleep 1

# TEST 22: Resume with Invalid ID
echo "Test 22/25: RESUME API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 22,
    "method": "org.rdk.PackageManagerRDKEMS.resume",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "resume (Invalid ID)" "$PKG_REQUEST" "Resume with invalid download ID" "negative"
sleep 1

# TEST 23: Cancel with Invalid ID
echo "Test 23/25: CANCEL API - Invalid Download ID"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 23,
    "method": "org.rdk.PackageManagerRDKEMS.cancel",
    "params": {
        "downloadId": "99999"
    }
}'
execute_test "cancel (Invalid ID)" "$PKG_REQUEST" "Cancel with invalid download ID" "negative"
sleep 1

# TEST 24: Install with Invalid Package ID
echo "Test 24/25: INSTALL API - Invalid Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 24,
    "method": "org.rdk.PackageManagerRDKEMS.install",
    "params": {
        "packageId": "com.invalid.nonexistent",
        "version": "0.0.0",
        "fileLocator": "99999"
    }
}'
execute_test "install (Invalid Package)" "$PKG_REQUEST" "Install with invalid package ID" "negative"
sleep 1

# TEST 25: Uninstall with Invalid Package ID
echo "Test 25/25: UNINSTALL API - Invalid Package"
PKG_REQUEST='{
    "jsonrpc": "2.0",
    "id": 25,
    "method": "org.rdk.PackageManagerRDKEMS.uninstall",
    "params": {
        "packageId": "com.invalid.nonexistent"
    }
}'
execute_test "uninstall (Invalid Package)" "$PKG_REQUEST" "Uninstall with invalid package ID" "negative"
sleep 1

else
    echo "Skipping NEGATIVE TEST SCENARIOS (EXE_NEG_TC=false)"
    echo ""
fi

# ============================================================================
# TEST SUMMARY
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      TEST SUMMARY REPORT                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))

printf "%-40s %3d\n" "Total Tests Executed:" "$TOTAL_TESTS"
printf "%-40s %3d ($(( TESTS_PASSED * 100 / TOTAL_TESTS ))%%)\n" "Tests Passed:" "$TESTS_PASSED"
printf "%-40s %3d\n" "Tests Failed:" "$TESTS_FAILED"
printf "%-40s %3d\n" "Tests Skipped:" "$TESTS_SKIPPED"
echo ""

if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_PASSED -gt 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  ✓ ALL TESTS PASSED - PackageManager APIs are functioning     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    if [ $TESTS_FAILED -gt 0 ]; then
        echo "Failed Tests:"
        for test in "${FAILED_TESTS[@]}"; do
            echo "  ✗ $test"
        done
        echo ""
    fi
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║   ⚠ SOME TESTS FAILED - Review output above for details      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 1
fi
