#!/bin/bash
    ##########################################################################
    # AppManager Comprehensive Validation Script
    # Includes ALL 34 test cases from framework/fileStore/testscriptsRDKV/component/AppManager
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
    TEST_APP_ID=""
    SYSTEM_APP_ID=""
    
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
        local test_type="${4:-positive}"  # positive, negative, query, property
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "TEST: $test_name"
        echo "DESC: $description"
        echo "TYPE: $test_type"
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
                # For positive/query/property tests, error means failure
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
                # For positive/query/property tests, no error means success
                echo "✓ TEST PASSED"
                echo ""
                TESTS_PASSED=$((TESTS_PASSED + 1))
                return 0
            fi
        fi
    }

    # Get installed and loaded apps for use in tests
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "STEP 1: Initial Discovery"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    response=$(curl -s -H 'content-type:text/plain;' --data-binary '{"jsonrpc": "2.0", "id": 0, "method": "org.rdk.AppManager.1.getInstalledApps"}' "$JSONRPC_URL")
    echo "getInstalledApps response:"
    echo "$response"
    echo ""

    # Extract first app ID if available
    if [[ "$response" == *'"appId"'* ]]; then
        TEST_APP_ID=$(echo "$response" | grep -o '"appId":"[^"]*"' | head -n 1 | cut -d'"' -f4)
        if [ -n "$TEST_APP_ID" ]; then
            echo "✓ Found test app: $TEST_APP_ID"
            APP_FOUND=true
        else
            echo "⚠ No apps installed - Lifecycle tests will be marked as FAILED"
            APP_FOUND=false
        fi
    else
        echo "⚠ No apps installed - Lifecycle tests will be marked as FAILED"
        APP_FOUND=false
    fi
    echo ""
    sleep 1

    echo "══════════════════════════════════════════════════════════════════"
    echo "TEST GROUP 1: Plugin Activation"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""

    # Test 1: activate via systemctl
    test_name="TC_01: activate (systemctl)"
    echo "Testing: $test_name"
    echo "Description: Activate AppManager plugin via systemctl service"
    echo ""
    
    # Start the service via systemctl
    systemctl start wpeframework-appmanager.service
    sleep 2
    
    # Verify service is active
    if systemctl is-active --quiet wpeframework-appmanager.service; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "✓ TEST PASSED - AppManager service activated successfully"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        FAILED_TESTS+=("$test_name - Service activation failed")
        echo "✗ TEST FAILED - AppManager service activation failed"
    fi
    echo ""

    sleep 1

    echo "══════════════════════════════════════════════════════════════════"
    echo "TEST GROUP 2: Query APIs"
    echo "══════════════════════════════════════════════════════════════════"
    echo ""

    # Test 2: getInstalledApps (Query)
    execute_test "TC_14: getInstalledApps" \
    '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.1.getInstalledApps"}' \
    "Get list of all installed applications" \
    "query"

    sleep 1

    # Test 3: getLoadedApps (Query)
    execute_test "TC_15: getLoadedApps" \
    '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' \
    "Get list of currently loaded/running applications" \
    "query"

    sleep 1

    # Test 4: clearAllAppData (Query)
    execute_test "TC_24: clearAllAppData" \
    '{"jsonrpc": "2.0", "id": 4, "method": "org.rdk.AppManager.1.clearAllAppData"}' \
    "Clear all app data from system" \
    "query"

    sleep 1

    # Test 5-8: Resource Property APIs
    execute_test "TC_31: getMaxRunningApps" \
    '{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.AppManager.1.getMaxRunningApps"}' \
    "Get maximum number of apps that can run simultaneously" \
    "property"

    sleep 1

    execute_test "TC_32: getMaxHibernatedApps" \
    '{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.AppManager.1.getMaxHibernatedApps"}' \
    "Get maximum number of hibernated apps allowed" \
    "property"

    sleep 1

    execute_test "TC_33: getMaxHibernatedFlashUsage" \
    '{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.AppManager.1.getMaxHibernatedFlashUsage"}' \
    "Get maximum flash storage usage for hibernated apps" \
    "property"

    sleep 1

    execute_test "TC_34: getMaxInactiveRamUsage" \
    '{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.AppManager.1.getMaxInactiveRamUsage"}' \
    "Get maximum RAM usage allowed for inactive apps" \
    "property"

    sleep 1

    if [ "$APP_FOUND" = true ]; then
        
        echo "══════════════════════════════════════════════════════════════════"
        echo "TEST GROUP 3: App Lifecycle - Positive Tests"
        echo "══════════════════════════════════════════════════════════════════"
        echo ""

        # Cleanup: Kill any existing instances
        curl -s -H 'content-type:text/plain;' --data-binary "{\"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"org.rdk.AppManager.1.killApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" "$JSONRPC_URL" > /dev/null 2>&1
        sleep 1

        # Test 9: isInstalled (Positive - installed app)
        execute_test "TC_12: isInstalled (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 9, \"method\": \"org.rdk.AppManager.1.isInstalled\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Check if installed app is detected" \
        "positive"

        sleep 1

        # Test 10: getAppMetadata (Positive)
        execute_test "TC_25: getAppMetadata (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 10, \"method\": \"org.rdk.AppManager.1.getAppMetadata\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Get metadata for installed app" \
        "positive"

        sleep 1

        # Test 11: getAppProperty (Positive)
        execute_test "TC_27: getAppProperty (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 11, \"method\": \"org.rdk.AppManager.1.getAppProperty\", \"params\": {\"appId\": \"$TEST_APP_ID\", \"property\": \"state\"}}" \
        "Get property of installed app" \
        "positive"

        sleep 1

        # Test 12: launchApp (Positive - First Launch for closeApp)
        execute_test "TC_02: launchApp (Positive - for closeApp)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 12, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application for closeApp test" \
        "positive"

        sleep 2

        # Verify launch success
        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        if ! is_app_loaded "$TEST_APP_ID"; then
            # Launch failed - this is a real failure
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("TC_02: launchApp (Positive) - App failed to load (system error)")
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
        else
            # Test 13: closeApp (Positive)
            execute_test "TC_06: closeApp (Positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 13, \"method\": \"org.rdk.AppManager.1.closeApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Close running app gracefully" \
            "positive"
        fi

        sleep 2

        # Test 14: preloadApp (Positive - Second Launch)
        execute_test "TC_04: preloadApp (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 14, \"method\": \"org.rdk.AppManager.1.preloadApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Preload app into memory" \
        "positive"

        sleep 2

        # Test 15: launchApp (Positive - Second Launch for terminateApp)
        execute_test "TC_02: launchApp (Positive - for terminateApp)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 15, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application for terminateApp test" \
        "positive"

        sleep 2

        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        if ! is_app_loaded "$TEST_APP_ID"; then
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("TC_02: launchApp (Positive) - App failed to load (system error)")
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
        else
            # Test 16: terminateApp (Positive)
            execute_test "TC_08: terminateApp (Positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 16, \"method\": \"org.rdk.AppManager.1.terminateApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Forcefully terminate running app" \
            "positive"
        fi

        sleep 2

        # Test 17: launchApp (Positive - Third Launch for killApp)
        execute_test "TC_02: launchApp (Positive - for killApp)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 17, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Launch application for killApp test" \
        "positive"

        sleep 2

        check_app_logs "$TEST_APP_ID"
        LOG_ERROR=$?
        
        if ! is_app_loaded "$TEST_APP_ID"; then
            TESTS_PASSED=$((TESTS_PASSED - 1))
            TESTS_FAILED=$((TESTS_FAILED + 1))
            FAILED_TESTS+=("TC_02: launchApp (Positive) - App failed to load (system error)")
            echo "✗ TEST FAILED - API returned success but app failed to load"
            echo ""
        else
            # Test 18: killApp (Positive)
            execute_test "TC_10: killApp (Positive)" \
            "{\"jsonrpc\": \"2.0\", \"id\": 18, \"method\": \"org.rdk.AppManager.1.killApp\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
            "Immediately kill running app" \
            "positive"
        fi

        sleep 1

        # Test 19: setAppProperty (Positive)
        execute_test "TC_29: setAppProperty (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 19, \"method\": \"org.rdk.AppManager.1.setAppProperty\", \"params\": {\"appId\": \"$TEST_APP_ID\", \"property\": \"priority\", \"value\": \"high\"}}" \
        "Set property on app" \
        "positive"

        sleep 1

        echo "══════════════════════════════════════════════════════════════════"
        echo "TEST GROUP 4: App Lifecycle - Negative Tests"
        echo "══════════════════════════════════════════════════════════════════"
        echo ""

        # Test 20: isInstalled (Negative - non-existent app)
        execute_test "TC_13: isInstalled (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 20, \"method\": \"org.rdk.AppManager.1.isInstalled\", \"params\": {\"appId\": \"nonexistent.invalid.app\"}}" \
        "Check non-existent app (should return false or error)" \
        "negative"

        sleep 1

        # Test 21: getAppMetadata (Negative)
        execute_test "TC_26: getAppMetadata (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 21, \"method\": \"org.rdk.AppManager.1.getAppMetadata\", \"params\": {\"appId\": \"nonexistent.app.xyz\"}}" \
        "Get metadata of non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 22: getAppProperty (Negative)
        execute_test "TC_28: getAppProperty (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 22, \"method\": \"org.rdk.AppManager.1.getAppProperty\", \"params\": {\"appId\": \"nonexistent.app\", \"property\": \"state\"}}" \
        "Get property of non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 23: launchApp (Negative - invalid app)
        execute_test "TC_03: launchApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 23, \"method\": \"org.rdk.AppManager.1.launchApp\", \"params\": {\"appId\": \"invalid.nonexistent.app\"}}" \
        "Launch non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 24: preloadApp (Negative)
        execute_test "TC_05: preloadApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 24, \"method\": \"org.rdk.AppManager.1.preloadApp\", \"params\": {\"appId\": \"fake.app.xyz\"}}" \
        "Preload non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 25: closeApp (Negative)
        execute_test "TC_07: closeApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 25, \"method\": \"org.rdk.AppManager.1.closeApp\", \"params\": {\"appId\": \"not.running.app\"}}" \
        "Close non-running app (should return error)" \
        "negative"

        sleep 1

        # Test 26: terminateApp (Negative)
        execute_test "TC_09: terminateApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 26, \"method\": \"org.rdk.AppManager.1.terminateApp\", \"params\": {\"appId\": \"nonexistent.app.123\"}}" \
        "Terminate non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 27: killApp (Negative)
        execute_test "TC_11: killApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 27, \"method\": \"org.rdk.AppManager.1.killApp\", \"params\": {\"appId\": \"fake.killed.app\"}}" \
        "Kill non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 28: setAppProperty (Negative)
        execute_test "TC_30: setAppProperty (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 28, \"method\": \"org.rdk.AppManager.1.setAppProperty\", \"params\": {\"appId\": \"nonexistent.app\", \"property\": \"invalid\", \"value\": \"bad\"}}" \
        "Set property on non-existent app (should return error)" \
        "negative"

        sleep 1

        # Test 29: clearAppData (Positive)
        execute_test "TC_22: clearAppData (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 29, \"method\": \"org.rdk.AppManager.1.clearAppData\", \"params\": {\"appId\": \"$TEST_APP_ID\"}}" \
        "Clear data for installed app" \
        "positive"

        sleep 1

        # Test 30: clearAppData (Negative)
        execute_test "TC_23: clearAppData (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 30, \"method\": \"org.rdk.AppManager.1.clearAppData\", \"params\": {\"appId\": \"nonexistent.app\"}}" \
        "Clear data for non-existent app (should return error)" \
        "negative"

        sleep 1

        echo "══════════════════════════════════════════════════════════════════"
        echo "TEST GROUP 5: System Apps"
        echo "══════════════════════════════════════════════════════════════════"
        echo ""

        # Test 31: startSystemApp (Positive)
        execute_test "TC_18: startSystemApp (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 31, \"method\": \"org.rdk.AppManager.1.startSystemApp\", \"params\": {\"appId\": \"org.rdk.firebolt-ui\"}}" \
        "Start system app (if available)" \
        "positive"

        sleep 2

        # Test 32: stopSystemApp (Positive)
        execute_test "TC_20: stopSystemApp (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 32, \"method\": \"org.rdk.AppManager.1.stopSystemApp\", \"params\": {\"appId\": \"org.rdk.firebolt-ui\"}}" \
        "Stop system app" \
        "positive"

        sleep 1

        # Test 33: startSystemApp (Negative)
        execute_test "TC_19: startSystemApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 33, \"method\": \"org.rdk.AppManager.1.startSystemApp\", \"params\": {\"appId\": \"fake.system.app\"}}" \
        "Start non-existent system app (should return error)" \
        "negative"

        sleep 1

        # Test 34: stopSystemApp (Negative)
        execute_test "TC_21: stopSystemApp (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 34, \"method\": \"org.rdk.AppManager.1.stopSystemApp\", \"params\": {\"appId\": \"nonexistent.system.app\"}}" \
        "Stop non-existent system app (should return error)" \
        "negative"

        sleep 1

        echo "══════════════════════════════════════════════════════════════════"
        echo "TEST GROUP 6: Intent Communication"
        echo "══════════════════════════════════════════════════════════════════"
        echo ""

        # Test 35: sendIntent (Positive)
        execute_test "TC_16: sendIntent (Positive)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 35, \"method\": \"org.rdk.AppManager.1.sendIntent\", \"params\": {\"appId\": \"$TEST_APP_ID\", \"action\": \"test.action\"}}" \
        "Send intent to app" \
        "positive"

        sleep 1

        # Test 36: sendIntent (Negative)
        execute_test "TC_17: sendIntent (Negative)" \
        "{\"jsonrpc\": \"2.0\", \"id\": 36, \"method\": \"org.rdk.AppManager.1.sendIntent\", \"params\": {\"appId\": \"nonexistent.app\", \"action\": \"test.action\"}}" \
        "Send intent to non-existent app (should return error)" \
        "negative"

        sleep 1

    else
        echo "⚠⚠⚠ No apps found - Skipping app lifecycle and system app tests ⚠⚠⚠"
        echo ""
        # These would fail because no app to test with
        TESTS_SKIPPED=$((TESTS_SKIPPED + 26))  # Tests 9-34 in the with-app section
    fi

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 Test Execution Complete                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Calculate totals
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
    echo "║  API METHODS TESTED (21 total):                                ║"
    echo "║    • activate, launchApp, preloadApp                           ║"
    echo "║    • closeApp, terminateApp, killApp                           ║"
    echo "║    • isInstalled, getInstalledApps, getLoadedApps              ║"
    echo "║    • sendIntent, startSystemApp, stopSystemApp                 ║"
    echo "║    • clearAppData, clearAllAppData                             ║"
    echo "║    • getAppMetadata, getAppProperty, setAppProperty            ║"
    echo "║    • getMaxRunningApps, getMaxHibernatedApps                   ║"
    echo "║    • getMaxHibernatedFlashUsage, getMaxInactiveRamUsage        ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║  TEST CATEGORIES:                                              ║"
    echo "║    Group 1: Plugin Activation (1 test)                         ║"
    echo "║    Group 2: Query APIs (8 tests)                               ║"
    echo "║    Group 3: App Lifecycle - Positive (11 tests)                ║"
    echo "║    Group 4: App Lifecycle - Negative (8 tests)                 ║"
    echo "║    Group 5: System Apps (4 tests)                              ║"
    echo "║    Group 6: Intent Communication (2 tests)                     ║"
    echo "║    TOTAL: 34 tests covering all AppManager APIs                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Print failed tests if any
    if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║                  FAILED TEST CASES                             ║"
        echo "╠════════════════════════════════════════════════════════════════╣"
        for failed_test in "${FAILED_TESTS[@]}"; do
            printf "║  ✗ %-60s ║\n" "$failed_test"
        done
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
    fi

    # Print skipped tests if any
    if [ ${#SKIPPED_TESTS[@]} -gt 0 ]; then
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║                  SKIPPED TEST CASES                            ║"
        echo "╠════════════════════════════════════════════════════════════════╣"
        for skipped_test in "${SKIPPED_TESTS[@]}"; do
            printf "║  ⊘ %-60s ║\n" "$skipped_test"
        done
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""
    fi

    if [ $TESTS_FAILED -eq 0 ] && [ $TESTS_PASSED -gt 0 ]; then
        echo "🎉 All executed tests passed successfully!"
    else
        if [ $TESTS_FAILED -gt 0 ]; then
            echo "⚠️  $TESTS_FAILED test(s) FAILED. Review the output above for details."
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
        echo "║  Skipped Tests: $TESTS_SKIPPED                                        ║"
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
