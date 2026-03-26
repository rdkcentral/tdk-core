    #!/bin/bash
    ##########################################################################
    # DownloadManager Comprehensive Validation Script
    # Run directly on device to validate all DownloadManager API methods
    # Device: 192.168.29.123
    # Date: February 9, 2026
    ##########################################################################

    JSONRPC_URL="http://127.0.0.1:9998/jsonrpc"
    DOWNLOAD_URL="http://192.168.29.38/rpi-app-mw11nov-lib32-application-test-image-RPI4-20251112035928-ota.wic.tar.gz"
    TESTS_PASSED=0
    TESTS_FAILED=0
    TESTS_SKIPPED=0
    DOWNLOAD_ID=""
    FAILED_TESTS=()

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     DownloadManager API Comprehensive Test Suite              ║"
    echo "║      Validating all DownloadManager plugin methods             ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Step 0: Check and activate DownloadManager service
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "STEP 0: Service Initialization"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    echo "Checking DownloadManager service status..."
    systemctl status wpeframework-downloadmanager.service --no-pager 2>&1 | head -n 10
    echo ""

    echo "Starting DownloadManager service..."
    systemctl start wpeframework-downloadmanager.service
    sleep 2

    echo "Verifying service is active..."
    if systemctl is-active --quiet wpeframework-downloadmanager.service; then
        echo "✓ DownloadManager service is running"
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

    echo "══════════════════════════════════════════════════════════════════"
    echo "POSITIVE TEST SCENARIOS"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""

    # Test 1: Method 1 - getStorageDetails
    execute_test "Method 1: getStorageDetails" \
    '{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.getStorageDetails"}' \
    "Get information about storage space availability" \
    "positive"

    sleep 1

    # Test 2: Method 2 - download (positive)
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TEST: Method 2: download (positive)"
    echo "DESC: Start downloading file with default options"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Request:"
    DOWNLOAD_REQUEST="{\"jsonrpc\": \"2.0\", \"id\": 2, \"method\": \"org.rdk.DownloadManager.download\", \"params\": {\"url\": \"$DOWNLOAD_URL\", \"options\": {\"priority\": true, \"retries\": 2, \"rateLimit\": 0}}}"
    echo "$DOWNLOAD_REQUEST"
    echo ""
    echo "Response:"
    DOWNLOAD_RESPONSE=$(curl -s -H 'content-type:text/plain;' --data-binary "$DOWNLOAD_REQUEST" "$JSONRPC_URL")
    echo "$DOWNLOAD_RESPONSE"
    echo ""
    
    # Extract download ID from response
    DOWNLOAD_ID=$(echo "$DOWNLOAD_RESPONSE" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
    
    if echo "$DOWNLOAD_RESPONSE" | grep -q '"error":'; then
        echo "✗ TEST FAILED - Error detected"
        echo ""
        TESTS_FAILED=$((TESTS_FAILED + 1))
        FAILED_TESTS+=("Method 2: download (positive)")
    else
        echo "✓ TEST PASSED"
        echo ""
        TESTS_PASSED=$((TESTS_PASSED + 1))
        if [ -z "$DOWNLOAD_ID" ]; then
            DOWNLOAD_ID="0"
            echo "⚠ Warning: Failed to extract download ID - Using 0 as fallback"
        else
            echo "✓ Download started with ID: $DOWNLOAD_ID"
        fi
    fi
    echo ""
    sleep 2

    # Test 4: Method 4 - rateLimit (positive)
    execute_test "Method 4: rateLimit (positive)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 4, \"method\": \"org.rdk.DownloadManager.rateLimit\", \"params\": {\"downloadId\": \"$DOWNLOAD_ID\", \"limit\": 1048576}}" \
    "Set rate limit to 1MB/s for download" \
    "positive"

    sleep 1

    # Test 5: Method 5 - pause (positive)
    execute_test "Method 5: pause (positive)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 5, \"method\": \"org.rdk.DownloadManager.pause\", \"params\": {\"downloadId\": \"$DOWNLOAD_ID\"}}" \
    "Pause the active download" \
    "positive"

    sleep 2

    # Test 6: Method 6 - resume (positive)
    execute_test "Method 6: resume (positive)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 6, \"method\": \"org.rdk.DownloadManager.resume\", \"params\": {\"downloadId\": \"$DOWNLOAD_ID\"}}" \
    "Resume the paused download" \
    "positive"

    sleep 2

    # Test 7: progress after resume
    execute_test "Method 3: progress (after resume)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 7, \"method\": \"org.rdk.DownloadManager.progress\", \"params\": {\"downloadId\": \"$DOWNLOAD_ID\"}}" \
    "Query progress after resuming download" \
    "positive"

    sleep 1

    # Test 8: Method 7 - cancel (positive)
    execute_test "Method 7: cancel (positive)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 8, \"method\": \"org.rdk.DownloadManager.cancel\", \"params\": {\"downloadId\": \"$DOWNLOAD_ID\"}}" \
    "Cancel the active download" \
    "positive"

    sleep 2

    echo "══════════════════════════════════════════════════════════════════"
    echo "NEGATIVE TEST SCENARIOS (Error Handling - Errors Are Expected)"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""

    # Test 8: download with invalid URL (negative)
    execute_test "Method 2: download (negative - invalid URL)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 8, \"method\": \"org.rdk.DownloadManager.download\", \"params\": {\"url\": \"http://invalid.nonexistent.url.host/file.tar.gz\", \"options\": {\"priority\": false, \"retries\": 0, \"rateLimit\": 0}}}" \
    "Download from invalid URL (should return error)" \
    "negative"

    sleep 1

    # Test 9: progress with invalid download ID (negative)
    execute_test "Method 3: progress (negative - invalid ID)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 9, \"method\": \"org.rdk.DownloadManager.progress\", \"params\": {\"downloadId\": \"invalid.nonexistent.id.12345\"}}" \
    "Query progress with non-existent download ID (should return ERROR_UNKNOWN_KEY)" \
    "negative"

    sleep 1

    # Test 10: pause with invalid download ID (negative)
    execute_test "Method 5: pause (negative - invalid ID)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 10, \"method\": \"org.rdk.DownloadManager.pause\", \"params\": {\"downloadId\": \"fake.download.id.xyz\"}}" \
    "Pause non-existent download (should return error)" \
    "negative"

    sleep 1

    # Test 11: resume with invalid download ID (negative)
    execute_test "Method 6: resume (negative - invalid ID)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 11, \"method\": \"org.rdk.DownloadManager.resume\", \"params\": {\"downloadId\": \"unknown.download.12345\"}}" \
    "Resume non-existent download (should return error)" \
    "negative"

    sleep 1

    # Test 12: cancel with invalid download ID (negative)
    execute_test "Method 7: cancel (negative - invalid ID)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 12, \"method\": \"org.rdk.DownloadManager.cancel\", \"params\": {\"downloadId\": \"phantom.id.notfound\"}}" \
    "Cancel non-existent download (should return error)" \
    "negative"

    sleep 1

    # Test 13: rateLimit with invalid download ID (negative)
    execute_test "Method 4: rateLimit (negative - invalid ID)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 13, \"method\": \"org.rdk.DownloadManager.rateLimit\", \"params\": {\"downloadId\": \"missing.download.id\", \"limit\": 512000}}" \
    "Set rate limit on non-existent download (should return error)" \
    "negative"

    sleep 1

    # Test 14: delete with invalid file path (negative)
    execute_test "Method 8: delete (negative - invalid path)" \
    "{\"jsonrpc\": \"2.0\", \"id\": 14, \"method\": \"org.rdk.DownloadManager.delete\", \"params\": {\"fileLocator\": \"/nonexistent/invalid/path/file.tar.gz\"}}" \
    "Delete non-existent file (should return ERROR_GENERAL)" \
    "negative"

    sleep 1

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 Test Execution Complete                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Calculate totals
    TESTS_TOTAL=$((TESTS_PASSED + TESTS_FAILED))

    # Print summary
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    TEST SUMMARY                                ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║  Device IP:           192.168.29.123                           ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    printf "║  Total Tests Run:     %-44s ║\n" "$TESTS_TOTAL"
    printf "║  Tests Passed:        %-44s ║\n" "$TESTS_PASSED (✓)"
    printf "║  Tests Failed:        %-44s ║\n" "$TESTS_FAILED (✗)"
    printf "║  Tests Skipped:       %-44s ║\n" "$TESTS_SKIPPED (⊘)"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║  METHODS TESTED:                                               ║"
    echo "║    1. getStorageDetails        - Query storage info             ║"
    echo "║  POSITIVE TESTS:                                               ║"
    echo "║    2. download (positive)      - Start file download            ║"
    echo "║    3. rateLimit (positive)     - Set bandwidth limit            ║"
    echo "║    4. pause (positive)         - Pause active download          ║"
    echo "║    5. resume (positive)        - Resume paused download         ║"
    echo "║    6. progress (after resume)  - Query download progress        ║"
    echo "║    7. cancel (positive)        - Cancel active download         ║"
    echo "║  NEGATIVE TESTS (Error Handling):                              ║"
    echo "║    8. download (negative)      - Invalid URL handling           ║"
    echo "║    9. progress (negative)      - Invalid download ID            ║"
    echo "║   10. pause (negative)         - Invalid download ID            ║"
    echo "║   11. resume (negative)        - Invalid download ID            ║"
    echo "║   12. cancel (negative)        - Invalid download ID            ║"
    echo "║   13. rateLimit (negative)     - Invalid download ID            ║"
    echo "║   14. delete (negative)        - Invalid file path              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Print failed tests if any
    if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║                  FAILED TEST CASES                             ║"
        echo "╠════════════════════════════════════════════════════════════════╣"
        for failed_test in "${FAILED_TESTS[@]}"; do
            echo "║  ✗ $failed_test"
        done
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
    fi

    if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_PASSED -gt 0 ]; then
        echo "🎉 All executed tests passed successfully!"
    else
        if [ $TESTS_FAILED -gt 0 ]; then
            echo "⚠️  $TESTS_FAILED test(s) failed. Review the output above for details."
        fi
    fi
    echo ""

    echo "📝 Notes:"
    echo "   - Download URL: $DOWNLOAD_URL"
    if [ -n "$DOWNLOAD_ID" ]; then
        echo "   - Download ID used for testing: $DOWNLOAD_ID"
    fi
    echo "   - Negative tests expect errors (proper error handling)"
    echo "   - See CURL_COMMANDS_REFERENCE.md for direct curl command examples"
    echo ""

    echo "Test script completed - $(date)"
