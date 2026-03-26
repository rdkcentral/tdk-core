#!/bin/bash

##########################################################################
# Standalone Package Manager Validation and Installation Script
# 
# This script:
# 1. Validates PackageManager plugin is available and active
# 2. Downloads specified packages via PackageManager API
# 3. Installs downloaded packages
# 
# No external dependencies required (uses curl, bash, systemctl)
# Compatible with: RDK2.0 devices with WPEFramework
#
# Usage: ./validate_and_install_packages.sh [device_ip] [jsonrpc_port]
#        ./validate_and_install_packages.sh 192.168.29.123 9998
##########################################################################

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

DEVICE_IP="${1:-127.0.0.1}"
JSONRPC_PORT="${2:-9998}"
JSONRPC_URL="http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc"

# Service names
PACKAGEMANAGER_SERVICE="wpeframework-packagemanager.service"
PLUGIN_NAME="org.rdk.PackageManagerRDKEMS"

# Package URLs to download and install
PACKAGES=(
    "http://192.168.29.38/com.rdkcentral.cobalt+0.1.0.bolt"
    "http://192.168.29.38/com.rdkcentral.youtube+0.1.0.bolt"
)

# Timeout for curl operations (in seconds)
CURL_TIMEOUT=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓ SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗ ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠ WARNING]${NC} $1"
}

log_test_start() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}TEST: $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

log_test_result() {
    local test_name="$1"
    local result="$2"
    ((TOTAL_TESTS++))
    
    if [ "$result" = "PASS" ]; then
        ((PASSED_TESTS++))
        log_success "$test_name"
    elif [ "$result" = "SKIP" ]; then
        ((SKIPPED_TESTS++))
        log_warning "$test_name (skipped)"
    else
        ((FAILED_TESTS++))
        log_error "$test_name"
    fi
}

# JSON-RPC call helper function
jsonrpc_call() {
    local method="$1"
    local params="$2"
    
    local payload="{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"${method}\",
        \"params\": ${params}
    }"
    
    log_info "Calling JSON-RPC method: ${method}"
    log_info "Payload: ${payload}"
    
    local response=$(curl -s \
        -H 'Content-Type: application/json' \
        --data "${payload}" \
        --connect-timeout ${CURL_TIMEOUT} \
        --max-time $((CURL_TIMEOUT + 5)) \
        "${JSONRPC_URL}" 2>/dev/null)
    
    echo "${response}"
}

# Check if plugin is active
check_plugin_active() {
    local response=$(jsonrpc_call "Controller.1.status" "{\"callsign\": \"${PLUGIN_NAME}\"}")
    
    if echo "${response}" | grep -q "\"state\":\"activated\""; then
        return 0
    fi
    
    if echo "${response}" | grep -q "\"success\":true"; then
        return 0
    fi
    
    return 1
}

# Get status of service
check_service_active() {
    if command -v systemctl &> /dev/null; then
        if systemctl is-active --quiet "${PACKAGEMANAGER_SERVICE}"; then
            return 0
        fi
    fi
    return 1
}

# ============================================================================
# MAIN TEST SEQUENCE
# ============================================================================

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  PackageManager Plugin Validation & Installation Script    ║"
    echo "║  Device: ${DEVICE_IP}:${JSONRPC_PORT}"
    echo "║  Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # ========================================================================
    # STEP 1: Verify Device Connectivity
    # ========================================================================
    log_test_start "Step 1: Verify Device Connectivity"
    
    log_info "Testing connectivity to ${DEVICE_IP}:${JSONRPC_PORT}..."
    
    if timeout ${CURL_TIMEOUT} curl -s "${JSONRPC_URL}" > /dev/null 2>&1; then
        log_test_result "Device Connectivity" "PASS"
    else
        log_test_result "Device Connectivity" "FAIL"
        log_error "Cannot reach device at ${JSONRPC_URL}"
        exit 1
    fi
    
    # ========================================================================
    # STEP 2: Verify/Start PackageManager Service
    # ========================================================================
    log_test_start "Step 2: Verify/Start PackageManager Service"
    
    log_info "Checking service status: ${PACKAGEMANAGER_SERVICE}"
    
    if check_service_active; then
        log_success "Service ${PACKAGEMANAGER_SERVICE} is active"
        log_test_result "Service Status Check" "PASS"
    else
        if command -v systemctl &> /dev/null; then
            log_warning "Service ${PACKAGEMANAGER_SERVICE} not active, attempting to start..."
            
            if systemctl start "${PACKAGEMANAGER_SERVICE}" 2>/dev/null; then
                sleep 2
                if check_service_active; then
                    log_success "Service ${PACKAGEMANAGER_SERVICE} started successfully"
                    log_test_result "Service Activation" "PASS"
                else
                    log_error "Failed to verify service activation"
                    log_test_result "Service Activation" "FAIL"
                fi
            else
                log_warning "Cannot start service via systemctl (may not have permissions), continuing..."
                log_test_result "Service Activation" "SKIP"
            fi
        else
            log_warning "systemctl not available, skipping service check"
            log_test_result "Service Activation" "SKIP"
        fi
    fi
    
    sleep 1
    
    # ========================================================================
    # STEP 3: Verify Plugin Status via JSON-RPC
    # ========================================================================
    log_test_start "Step 3: Verify Plugin Status (${PLUGIN_NAME})"
    
    log_info "Checking plugin activation status via JSON-RPC..."
    
    if check_plugin_active; then
        log_success "Plugin ${PLUGIN_NAME} is active"
        log_test_result "Plugin Status Check" "PASS"
    else
        log_error "Plugin ${PLUGIN_NAME} is not active"
        log_test_result "Plugin Status Check" "FAIL"
        log_warning "Some operations may fail without active plugin"
    fi
    
    sleep 1
    
    # ========================================================================
    # STEP 4: Download Packages
    # ========================================================================
    log_test_start "Step 4: Download Packages"
    
    declare -a DOWNLOAD_IDS
    DOWNLOAD_COUNT=0
    
    for idx in "${!PACKAGES[@]}"; do
        package_url="${PACKAGES[$idx]}"
        package_num=$((idx + 1))
        
        echo ""
        log_info "[$package_num/${#PACKAGES[@]}] Downloading: ${package_url}"
        
        # Extract package name from URL for better logging
        package_name=$(basename "${package_url}")
        
        # Call download API
        local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.download" \
            "{\"url\": \"${package_url}\"}")
        
        log_info "Download response: ${response}"
        
        # Parse download ID from response
        if echo "${response}" | grep -q "downloadId"; then
            download_id=$(echo "${response}" | grep -o '"downloadId":"[^"]*"' | head -1 | cut -d'"' -f4)
            
            if [ -n "${download_id}" ]; then
                log_success "Package downloaded successfully - ID: ${download_id}"
                DOWNLOAD_IDS[$DOWNLOAD_COUNT]="${download_id}"
                ((DOWNLOAD_COUNT++))
                log_test_result "Download Package (${package_name})" "PASS"
            else
                log_error "Failed to extract downloadId from response"
                log_test_result "Download Package (${package_name})" "FAIL"
            fi
        else
            # Check for alternate response format
            if echo "${response}" | grep -q "\"result\""; then
                # Extract from result object
                download_id=$(echo "${response}" | grep -o '"downloadId"[^}]*' | head -1)
                if [ -n "${download_id}" ]; then
                    download_id=$(echo "${download_id}" | grep -o '"[^"]*"$' | tr -d '"')
                    log_success "Package downloaded - ID: ${download_id}"
                    DOWNLOAD_IDS[$DOWNLOAD_COUNT]="${download_id}"
                    ((DOWNLOAD_COUNT++))
                    log_test_result "Download Package (${package_name})" "PASS"
                else
                    log_error "Failed to parse downloadId"
                    log_test_result "Download Package (${package_name})" "FAIL"
                fi
            else
                log_error "API error or unexpected response format"
                log_test_result "Download Package (${package_name})" "FAIL"
                log_info "Full response: ${response}"
            fi
        fi
        
        sleep 1
    done
    
    # ========================================================================
    # STEP 5: Verify Package Download Status
    # ========================================================================
    if [ ${DOWNLOAD_COUNT} -gt 0 ]; then
        log_test_start "Step 5: Verify Package Download Status"
        
        for idx in "${!DOWNLOAD_IDS[@]}"; do
            download_id="${DOWNLOAD_IDS[$idx]}"
            package_num=$((idx + 1))
            
            echo ""
            log_info "[$package_num/${#DOWNLOAD_IDS[@]}] Checking status of download: ${download_id}"
            
            local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.getProgress" \
                "{\"downloadId\": \"${download_id}\"}")
            
            log_info "Progress response: ${response}"
            
            if echo "${response}" | grep -q "percent"; then
                percent=$(echo "${response}" | grep -o '"percent":[0-9]*' | cut -d':' -f2)
                log_success "Download Progress: ${percent}%"
                log_test_result "Download Progress Check (ID: ${download_id})" "PASS"
            else
                log_warning "Could not retrieve progress status"
                log_test_result "Download Progress Check (ID: ${download_id})" "SKIP"
            fi
            
            sleep 1
        done
    else
        log_warning "No packages downloaded, skipping progress check"
    fi
    
    # ========================================================================
    # STEP 6: Install Downloaded Packages
    # ========================================================================
    if [ ${DOWNLOAD_COUNT} -gt 0 ]; then
        log_test_start "Step 6: Install Downloaded Packages"
        
        INSTALL_COUNT=0
        
        for idx in "${!DOWNLOAD_IDS[@]}"; do
            download_id="${DOWNLOAD_IDS[$idx]}"
            package_url="${PACKAGES[$idx]}"
            package_name=$(basename "${package_url}")
            package_id=$(echo "${package_name}" | cut -d'+' -f1)
            package_version=$(echo "${package_name}" | cut -d'+' -f2 | cut -d'.' -f1-3)
            
            echo ""
            log_info "[$((idx+1))/${#DOWNLOAD_IDS[@]}] Installing package: ${package_name}"
            log_info "  Package ID: ${package_id}"
            log_info "  Version: ${package_version}"
            log_info "  Download ID: ${download_id}"
            
            # Call install API
            local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.install" \
                "{\"packageId\": \"${package_id}\", \"version\": \"${package_version}\", \"fileLocator\": \"${download_id}\"}")
            
            log_info "Install response: ${response}"
            
            if echo "${response}" | grep -q "\"result\""; then
                log_success "Package installation initiated - ID: ${download_id}"
                ((INSTALL_COUNT++))
                log_test_result "Install Package (${package_name})" "PASS"
            else
                if echo "${response}" | grep -q "\"success\":true"; then
                    log_success "Package installation successful"
                    ((INSTALL_COUNT++))
                    log_test_result "Install Package (${package_name})" "PASS"
                else
                    log_error "Package installation failed"
                    log_test_result "Install Package (${package_name})" "FAIL"
                    log_info "Full response: ${response}"
                fi
            fi
            
            sleep 1
        done
        
        # ====================================================================
        # STEP 7: Setup Completion Summary
        # ====================================================================
        log_test_start "Setup Completion Summary"
        
        log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        log_info "Total Operations: $((DOWNLOAD_COUNT + INSTALL_COUNT))"
        log_success "Downloads: ${DOWNLOAD_COUNT}/${#PACKAGES[@]}"
        
        if [ ${INSTALL_COUNT} -gt 0 ]; then
            log_success "Installations: ${INSTALL_COUNT}/${DOWNLOAD_COUNT}"
        else
            log_warning "No installations completed"
        fi
        
        log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        if [ ${INSTALL_COUNT} -eq ${DOWNLOAD_COUNT} ]; then
            log_test_result "Overall Installation Status" "PASS"
        else
            log_test_result "Overall Installation Status" "FAIL"
        fi
    fi
    
    # ========================================================================
    # FINAL TEST REPORT
    # ========================================================================
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                    FINAL TEST REPORT                       ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    if [ ${TOTAL_TESTS} -gt 0 ]; then
        SUCCESS_PERCENT=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        
        echo "Total Tests:     ${TOTAL_TESTS}"
        echo -e "Passed:          ${GREEN}${PASSED_TESTS}${NC}"
        echo -e "Failed:          ${RED}${FAILED_TESTS}${NC}"
        echo -e "Skipped:         ${YELLOW}${SKIPPED_TESTS}${NC}"
        echo "Success Rate:    ${SUCCESS_PERCENT}%"
    else
        echo "No tests executed"
    fi
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    
    if [ ${FAILED_TESTS} -eq 0 ] && [ ${PASSED_TESTS} -gt 0 ]; then
        echo "║         ✓ ALL TESTS PASSED - Setup Successful          ║"
        echo "╚════════════════════════════════════════════════════════╝"
        return 0
    else
        echo "║      ✗ SOME TESTS FAILED - Please review logs         ║"
        echo "╚════════════════════════════════════════════════════════╝"
        return 1
    fi
}

# ============================================================================
# ENTRY POINT
# ============================================================================

if [ $# -eq 0 ]; then
    echo "Usage: $0 <device_ip> [jsonrpc_port]"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.29.123           # Uses default port 9998"
    echo "  $0 192.168.29.123 9998      # Explicit port"
    echo ""
    echo "Default values:"
    echo "  Device IP:   127.0.0.1"
    echo "  JSONRPC Port: 9998"
    echo ""
    exit 0
fi

main
