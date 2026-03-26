    #!/bin/bash
    ##########################################################################
    # AppManager Comprehensive Validation Script
    # Run directly on device to validate all AppManager API methods
    # Device: 192.168.29.123
    # Date: February 9, 2026
    ##########################################################################

    JSONRPC_URL="http://127.0.0.1:9998/jsonrpc"
    TESTS_PASSED=0
    TESTS_FAILED=0
    TESTS_SKIPPED=0
    FAILED_TESTS=()
SKIPPED_TESTS=()
    echo ""

    # Step 0: Check and activate AppManager service
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "STEP 0: Service Initialization"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    echo "Checking AppManager service status..."
    systemctl status wpeframework-appmanager.service --no-pager 2>&1 | head -n 10
    echo ""

    echo "Starting AppManager service..."
    systemctl start wpeframework-appmanager.service
    sleep 2

    echo "Verifying service is active..."
    if systemctl is-active --quiet wpeframework-appmanager.service; then
        echo "✓ AppManager service is running"
    else
        echo "⚠ Warning: Service may not be active, but continuing tests..."
    fi
    echo ""

    # Function to check if app is currently loaded
    is_app_loaded() {
        local app_id="$1"
        local loaded_apps=$(curl -s -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 0, "method": "org.rdk.AppManager.1.getLoadedApps"}' "$JSONRPC_URL")
        
        if [[ "$loaded_apps" == *"\"$app_id\""* ]]; then
            return 0  # App is loaded
        else
            return 1  # App is not loaded
        fi
    }

    # Function to check system logs for app-related errors
    check_app_logs() {
        local app_id="$1"
        local app_name=$(echo "$app_id" | cut -d'+' -f1)
        
        # Check for dependency issues
        if journalctl -n 100 2>/dev/null | grep -q "Failed to identify dependency"; then
            echo "⚠️  DEPENDENCY ISSUE DETECTED:"
            journalctl -n 100 2>/dev/null | grep -A2 "Failed to identify dependency" | head -n 5
            return 1
        fi
        
        # Check for package lock failures
        if journalctl -n 100 2>/dev/null | grep -q "Lock Failed"; then
            echo "⚠️  PACKAGE LOCK FAILURE DETECTED:"
            journalctl -n 100 2>/dev/null | grep -A2 "Lock Failed" | head -n 5
            return 1
        fi
        
        return 0
    }

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
        
        # Check for errors
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

    # Test 1: Get Installed Apps (to find test app)
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TEST: Preparation: Get installed apps for testing"
    echo "DESC: Find an app to use for lifecycle tests"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    response=$(curl -s -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 0, "method": "org.rdk.AppManager.1.getInstalledApps"}' "$JSONRPC_URL")
    echo "$response"
    echo ""

    # Extract first app ID if available
    if [[ "$response" == *'"appId"'* ]]; then
        TEST_APP_ID=$(echo "$response" | grep -o '"appId":"[^"]*"' | head -n 1 | cut -d'"' -f4)
        if [ -n "$TEST_APP_ID" ]; then
            echo "✓ Found test app: $TEST_APP_ID"
            APP_FOUND=true
        else
            echo "⚠ No apps installed - Some tests will be skipped"
            APP_FOUND=false
        TESTS_SKIPPED=$((TESTS_SKIPPED + 14))
        fi
    else
        echo "⚠ No apps installed - Some tests will be skipped"
        APP_FOUND=false
        TESTS_SKIPPED=$((TESTS_SKIPPED + 14))
    fi
    echo ""

    sleep 1

    # Test 2: Method 1 - getInstalledApps
    execute_test "Method 1: getInstalledApps" \
    '{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.1.getInstalledApps"}' \
    "Get list of all installed applications"

    sleep 1

    # Test 3: Method 2 - getLoadedApps
    execute_test "Method 2: getLoadedApps" \
    '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.1.getLoadedApps"}' \
    "Get list of currently loaded/running applications"

    sleep 1

    # Test 4: Method 3 - getMaxRunningApps
    execute_test "Method 3: getMaxRunningApps" \
    '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getMaxRunningApps"}' \
    "Get maximum number of apps that can run simultaneously"

    sleep 1

    # Test 5: Method 4 - getMaxHibernatedApps
    execute_test "Method 4: getMaxHibernatedApps" \
    '{"jsonrpc": "2.0", "id": 4, "method": "org.rdk.AppManager.1.getMaxHibernatedApps"}' \
    "Get maximum number of hibernated apps allowed"

    sleep 1

    # Test 6: Method 5 - getMaxInactiveRamUsage
    execute_test "Method 5: getMaxInactiveRamUsage" \
    '{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.AppManager.1.getMaxInactiveRamUsage"}' \
    "Get maximum RAM usage allowed for inactive apps"

    sleep 1

    # Test 7: Method 6 - getMaxHibernatedFlashUsage
    execute_test "Method 6: getMaxHibernatedFlashUsage" \
    '{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.AppManager.1.getMaxHibernatedFlashUsage"}' \
    "Get maximum flash storage usage for hibernated apps"

    sleep 1

    echo "══════════════════════════════════════════════════════════════════"
    echo "POSITIVE TEST SCENARIOS"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""

    # App-specific positive tests (only if app found)
    if [ "$APP_FOUND" = true ]; then
        
        # Cleanup: Attempt to kill any existing instances from previous runs
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "CLEANUP: Attempting to terminate any existing instances"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Try to kill any existing instance (ignore errors)
        curl -s -H 'content-type:text/plain;' --data-binary "{\"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"org.rdk.AppManager.1.killApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" "$JSONRPC_URL" > /dev/null 2>&1
        echo "✓ Cleanup completed (any existing instances terminated)"
        sleep 2
        echo ""
        
        # Test 8: Method 7 - isInstalled (positive)
        execute_test "Method 7: isInstalled (positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 7, \"method\": \"org.rdk.AppManager.1.isInstalled\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Check if app '$TEST_APP_ID' is installed" \
        "positive"
        
        sleep 1
        
        # Test 10: Method 10 - getAppMetadata (test before lifecycle operations)
        execute_test "Method 10: getAppMetadata (positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 10, \"method\": \"org.rdk.AppManager.1.getAppMetadata\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Get metadata for app '$TEST_APP_ID'" \
        "positive"
        
        sleep 1
        
        # Test 9a: Method 9 - launchApp (first time)
        execute_test "Method 9: launchApp (for closeApp test)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 9, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application '$TEST_APP_ID' (will close it in next test)" \
        "positive"
        
        sleep 2
        
        # Check system logs for underlying issues
        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        # CRITICAL: Verify app actually loaded despite API success
        if ! is_app_loaded "$TEST_APP_ID"; then
            # App failed to load - launchApp test should FAIL (not skip)
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("Method 9: launchApp (for closeApp test) - App load failure")
            
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
            
            # Skip close test due to launch failure
            if [ $LOG_ERROR -eq 1 ]; then
                SKIPPED_TESTS+=("Method 12: closeApp - Prerequisite launchApp failed (dependency/package lock issue)")
            else
                SKIPPED_TESTS+=("Method 12: closeApp - Prerequisite launchApp failed to load app")
            fi
            TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
        else
            echo "✓ App is confirmed loaded, proceeding with closeApp test"
            echo ""
            
            # Test 12: Method 12 - closeApp (on a running instance)
            execute_test "Method 12: closeApp (positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 12, \"method\": \"org.rdk.AppManager.1.closeApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Close running app '$TEST_APP_ID'" \
            "positive"
        fi
        
        sleep 2
        
        # Test 9b: Method 9 - launchApp (second time for terminate test)
        execute_test "Method 9: launchApp (for terminateApp test)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 9, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application '$TEST_APP_ID' (will terminate it in next test)" \
        "positive"
        
        sleep 2
        
        # Check system logs for underlying issues
        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        # CRITICAL: Verify app actually loaded despite API success
        if ! is_app_loaded "$TEST_APP_ID"; then
            # App failed to load - launchApp test should FAIL (not skip)
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("Method 9: launchApp (for terminateApp test) - App load failure")
            
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
            
            # Skip terminate test due to launch failure
            if [ $LOG_ERROR -eq 1 ]; then
                SKIPPED_TESTS+=("Method 13: terminateApp - Prerequisite launchApp failed (dependency/package lock issue)")
            else
                SKIPPED_TESTS+=("Method 13: terminateApp - Prerequisite launchApp failed to load app")
            fi
            TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
        else
            echo "✓ App is confirmed loaded, proceeding with terminateApp test"
            echo ""
            
            # Test 13: Method 13 - terminateApp (on a running instance)
            execute_test "Method 13: terminateApp (positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 13, \"method\": \"org.rdk.AppManager.1.terminateApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Terminate running app '$TEST_APP_ID'" \
            "positive"
        fi
        
        sleep 2
        
        # Test 9c: Method 9 - launchApp (third time for kill test)
        execute_test "Method 9: launchApp (for killApp test)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 9, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application '$TEST_APP_ID' (will kill it in next test)" \
        "positive"
        
        sleep 2
        
        # Check system logs for underlying issues
        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        # CRITICAL: Verify app actually loaded despite API success
        if ! is_app_loaded "$TEST_APP_ID"; then
            # App failed to load - launchApp test should FAIL (not skip)
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("Method 9: launchApp (for killApp test) - App load failure")
            
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
            
            # Skip kill test due to launch failure
            if [ $LOG_ERROR -eq 1 ]; then
                SKIPPED_TESTS+=("Method 14: killApp - Prerequisite launchApp failed (dependency/package lock issue)")
            else
                SKIPPED_TESTS+=("Method 14: killApp - Prerequisite launchApp failed to load app")
            fi
            TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
        else
            echo "✓ App is confirmed loaded, proceeding with killApp test"
            echo ""
            
            # Test 14: Method 14 - killApp (on a running instance)
            execute_test "Method 14: killApp (positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 14, \"method\": \"org.rdk.AppManager.1.killApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Kill running app '$TEST_APP_ID'" \
            "positive"
        fi
        
        sleep 2
        
        # Test 11: Method 11 - preloadApp (test separately, should not be followed by close/kill)
        execute_test "Method 11: preloadApp (positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 11, \"method\": \"org.rdk.AppManager.1.preloadApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Preload app '$TEST_APP_ID' into memory (NOTE: preloaded apps cannot be closed)" \
        "positive"
        
        sleep 1

    echo "══════════════════════════════════════════════════════════════════"
    echo "NEGATIVE TEST SCENARIOS (Error Handling)"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""
        
        # Test 15: Method 8 - isInstalled (negative) - Special handling for this test
        # This test can PASS in two ways: 1) Return error, or 2) Return false for non-existent app
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "TEST: Method 8: isInstalled (negative)"
        echo "DESC: Check non-existent app (should return false or error)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Request:"
        ISINSTALLED_REQUEST="{\"jsonrpc\": \"2.0\", \"id\": 15, \"method\": \"org.rdk.AppManager.1.isInstalled\", \"params\": {\"appId\": \"nonexistent.invalid.app\"}}"
        echo "$ISINSTALLED_REQUEST"
        echo ""
        echo "Response:"
        ISINSTALLED_RESPONSE=$(curl -s -H 'content-type:text/plain;' --data-binary "$ISINSTALLED_REQUEST" "$JSONRPC_URL")
        echo "$ISINSTALLED_RESPONSE"
        echo ""
        
        # For isInstalled with non-existent app: either error OR false result is valid
        if [[ "$ISINSTALLED_RESPONSE" == *'"error":'* ]]; then
            # Error response is valid (app doesn't exist)
            echo "✓ TEST PASSED (Error correctly detected for non-existent app)"
            echo ""
            TESTS_PASSED=$((TESTS_PASSED + 1))
        elif [[ "$ISINSTALLED_RESPONSE" == *'"result":false'* ]]; then
            # False result is also valid (app is not installed)
            echo "✓ TEST PASSED (Correctly returned false for non-existent app)"
            echo ""
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            # Any other response (like true) is incorrect
            echo "✗ TEST FAILED (Should return error or false for non-existent app)"
            echo ""
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("Method 8: isInstalled (negative)")
        fi
        
        sleep 1
        
    else
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "SKIPPED: Tests 7-15 (No installed apps available)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "ℹ️  To test app-specific methods, install an app using:"
        echo "   PackageManager or manually install a DAC application."
        echo ""
        echo "   These methods were skipped:"
        echo "   - isInstalled, launchApp, getAppMetadata, preloadApp"
        echo "   - closeApp, terminateApp, killApp"
        echo ""
    fi

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 Test Execution Complete                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Calculate totals (including skipped tests)
    TESTS_TOTAL=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))

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
    echo "║  Methods Tested:                                               ║"
    echo "║    1. getInstalledApps         - List installed apps            ║"
    echo "║    2. getLoadedApps            - List loaded/running apps       ║"
    echo "║    3. getMaxRunningApps        - Max concurrent apps            ║"
    echo "║    4. getMaxHibernatedApps     - Max hibernated apps            ║"
    echo "║    5. getMaxInactiveRamUsage   - Max RAM for inactive apps      ║"
    echo "║    6. getMaxHibernatedFlashUsage - Max flash for hibernated     ║"
    if [ "$APP_FOUND" = true ]; then
    echo "║    7. isInstalled               - Check app installed (positive) ║"
    echo "║    8. isInstalled               - Check non-existent (negative)  ║"
    echo "║    9. launchApp                 - Launch application            ║"
    echo "║   10. getAppMetadata            - Get app metadata              ║"
    echo "║   11. preloadApp                - Preload app into memory       ║"
    echo "║   12. closeApp                  - Close application             ║"
    echo "║   13. terminateApp              - Terminate application         ║"
    echo "║   14. killApp                   - Kill application              ║"
    echo "║   15. isInstalled (negative)    - Check non-existent (negative) ║"
    fi
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

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                   FINAL TEST REPORT                            ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    if [ $TESTS_FAILED -gt 0 ]; then
        echo "║  STATUS: ✗ FAILED                                             ║"
        echo "║  Failed Tests: $TESTS_FAILED                                         ║"
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║  FAILED TESTS:                                                 ║"
        for failed_test in "${FAILED_TESTS[@]}"; do
            printf "║    ✗ %-58s ║\n" "$failed_test"
        done
        echo "╠════════════════════════════════════════════════════════════════╣"
    elif [ $TESTS_SKIPPED -gt 0 ]; then
        echo "║  STATUS: ⊘ PARTIALLY SKIPPED                                  ║"
        echo "║  Skipped Tests: $TESTS_SKIPPED (due to dependency issues)        ║"
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║  SKIPPED TESTS:                                                ║"
        for skipped_test in "${SKIPPED_TESTS[@]}"; do
            printf "║    ⊘ %-58s ║\n" "$skipped_test"
        done
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║  PASSED TESTS: $TESTS_PASSED                                          ║"
    elif [ $TESTS_PASSED -gt 0 ]; then
        echo "║  STATUS: ✓ PASSED                                              ║"
        echo "║  All tests executed successfully!                             ║"
    else
        echo "║  STATUS: ⊘ SKIPPED                                             ║"
        echo "║  No tests were executed.                                       ║"
    fi
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    echo "Test script completed - $(date)"
