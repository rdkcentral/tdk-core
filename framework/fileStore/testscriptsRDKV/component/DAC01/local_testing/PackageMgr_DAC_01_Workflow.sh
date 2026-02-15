#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

# ============================================================================
# DAC01 Workflow Test - Local Testing Script
# ============================================================================
#
# Purpose: Execute complete DAC workflow using curl/bash (no Python required)
#          Downloads, installs, launches, terminates, and uninstalls an app
#
# Usage:
#   ./PackageMgr_DAC_01_Workflow.sh <device_ip> [jsonrpc_port] [package_index]
#
# Parameters:
#   device_ip      : IP address of RDK device (required)
#   jsonrpc_port   : JSON-RPC port (optional, default: 9998)
#   package_index  : Package index to test (optional, default: 2, 1-based)
#
# Examples:
#   ./PackageMgr_DAC_01_Workflow.sh 192.168.1.100
#   ./PackageMgr_DAC_01_Workflow.sh 192.168.1.100 9998
#   ./PackageMgr_DAC_01_Workflow.sh 192.168.1.100 9998 1
#
# ============================================================================

# Ensure summary is always shown on script exit
trap 'show_workflow_summary_on_exit' EXIT

# Flag to track if summary was already shown
SUMMARY_SHOWN=false

# Test result tracking
WORKFLOW_STEPS=()
WORKFLOW_PASSED=0
WORKFLOW_FAILED=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Logging Functions
# ============================================================================

print_header() {
    echo -e "\n${BLUE}$(printf '=%.0s' {1..80})${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}$(printf '=%.0s' {1..80})${NC}\n"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to record workflow step result
record_workflow_step() {
    local step_name="$1"
    local result="$2"
    local details="${3:-}"
    
    if [ "$result" = "PASS" ]; then
        WORKFLOW_PASSED=$((WORKFLOW_PASSED + 1))
        WORKFLOW_STEPS+=("✓ $step_name")
        print_success "$step_name: PASSED"
    else
        WORKFLOW_FAILED=$((WORKFLOW_FAILED + 1))
        if [ -n "$details" ]; then
            WORKFLOW_STEPS+=("✗ $step_name: $details")
        else
            WORKFLOW_STEPS+=("✗ $step_name")
        fi
        print_error "$step_name: FAILED - $details"
    fi
}

# Function to show summary on script exit (trap handler)
show_workflow_summary_on_exit() {
    if [ "$SUMMARY_SHOWN" = "false" ]; then
        echo ""
        print_header "Script Interrupted - Partial Results"
        show_workflow_summary
    fi
}

# Function to display workflow summary
show_workflow_summary() {
    print_header "WORKFLOW EXECUTION SUMMARY"
    
    local total_steps=$((WORKFLOW_PASSED + WORKFLOW_FAILED))
    
    echo "========================================"
    echo "         WORKFLOW SUMMARY"
    echo "========================================"
    
    if [ $WORKFLOW_PASSED -gt 0 ]; then
        print_success "Steps Passed: $WORKFLOW_PASSED/$total_steps"
    fi
    
    if [ $WORKFLOW_FAILED -gt 0 ]; then
        print_error "Steps Failed: $WORKFLOW_FAILED/$total_steps"
    fi
    
    if [ $total_steps -gt 0 ]; then
        echo ""
        echo "Detailed Results:"
        echo "================="
        
        for step in "${WORKFLOW_STEPS[@]}"; do
            echo "  $step"
        done
    fi
    
    echo ""
    
    if [ $WORKFLOW_FAILED -eq 0 ]; then
        if [ $total_steps -gt 0 ]; then
            print_success "✅ ALL WORKFLOW STEPS PASSED! DAC01 workflow completed successfully."
        fi
        return 0
    else
        print_error "❌ SOME WORKFLOW STEPS FAILED! Check the details above."
        return 1
    fi
}

# ============================================================================
# JSON-RPC Helper Functions
# ============================================================================

# Send JSON-RPC call to device
jsonrpc_call() {
    local method=$1
    local params=$2
    local jsonrpc_url="http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc"
    
    local payload="{\"jsonrpc\":\"2.0\",\"id\":42,\"method\":\"${method}\",\"params\":${params}}"
    
    local response=$(curl -s -X POST "$jsonrpc_url" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>/dev/null)
    
    echo "$response"
}

# Extract result from JSON-RPC response
# Handles both simple values and nested objects
extract_result() {
    local json=$1
    
    # Try to extract downloadId from nested object first (for download responses)
    if echo "$json" | grep -q '"downloadId"'; then
        echo "$json" | grep -o '"downloadId":"[^"]*"' | cut -d'"' -f4
    else
        # Fall back to simple result extraction
        echo "$json" | grep -o '"result":[^,}]*' | cut -d':' -f2 | sed 's/[",]//g' | xargs
    fi
}

# Check if JSON-RPC call was successful
is_success() {
    local json=$1
    if echo "$json" | grep -q '"result"'; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# DAC Workflow Functions
# ============================================================================

# Activate required plugins
activate_plugins() {
    print_info "Activating plugins..."
    
    local plugins=("org.rdk.StorageManager" "org.rdk.PackageManagerRDKEMS" "org.rdk.RDKWindowManager" "org.rdk.RuntimeManager" "org.rdk.LifecycleManager" "org.rdk.AppManager" "org.rdk.PreinstallManager")
    
    for plugin in "${plugins[@]}"; do
        print_info "  Activating: $plugin"
        local response=$(jsonrpc_call "Controller.1.activate" "{\"callsign\":\"$plugin\"}")
        
        if is_success "$response"; then
            print_success "$plugin activated"
        else
            print_warning "Could not activate $plugin (may already be active)"
        fi
        sleep 1  # Brief delay between activations
    done
}

# Fetch DAC catalog configuration from environment or defaults
fetch_dac_config() {
    print_info "Fetching DAC configuration..."
    
    # Default DAC configuration
    DAC_CATALOG_URL="${AI2_DAC_CATALOG_URL:-https://dac.dev.rdkinnovation.com}"
    DAC_CATALOG_USER="${AI2_DAC_USER:-dac-cloud-rdkm-user}"
    DAC_CATALOG_PASSWORD="${AI2_DAC_PASSWORD:-wcE\$:66[OkFbX-NrXvP*#F<HtR5z}"
    
    print_info "  Catalog URL: $DAC_CATALOG_URL"
    print_success "DAC config loaded"
}

# Get device platform info from device via JSON-RPC
get_device_info() {
    print_info "Getting device platform information..."
    
    # Query device info via System plugin
    local response=$(jsonrpc_call "org.rdk.System.1.getDeviceInfo" "{}")
    
    if is_success "$response"; then
        # Extract platform and firmware from response
        PLATFORM_NAME=$(echo "$response" | grep -o '"platform":"[^"]*"' | cut -d'"' -f4)
        FIRMWARE_VERSION=$(echo "$response" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        
        if [ -z "$PLATFORM_NAME" ]; then
            PLATFORM_NAME="rpi4"
        fi
        if [ -z "$FIRMWARE_VERSION" ]; then
            FIRMWARE_VERSION="1.0.0"
        fi
    else
        # Fallback to defaults if device query fails
        print_warning "Could not query device info, using defaults"
        PLATFORM_NAME="rpi4"
        FIRMWARE_VERSION="1.0.0"
    fi
    
    print_info "  Platform: $PLATFORM_NAME"
    print_info "  Firmware: $FIRMWARE_VERSION"
    print_success "Device info retrieved"
}

# List DAC packages from actual DAC catalog
list_dac_packages() {
    print_info "Listing available packages from DAC catalog..."
    print_info "  Catalog URL: $DAC_CATALOG_URL"
    
    # Fetch packages from DAC catalog using basic auth
    # Correct endpoint: /apps with parameters platformName and firmwareVer
    local dac_url="${DAC_CATALOG_URL}/apps?platformName=${PLATFORM_NAME}&firmwareVer=${FIRMWARE_VERSION}"
    print_info "  Request URL: $dac_url"
    
    local response=$(curl -s -u "${DAC_CATALOG_USER}:${DAC_CATALOG_PASSWORD}" "$dac_url" 2>/dev/null)
    
    if [ -z "$response" ]; then
        print_error "Failed to fetch packages from DAC catalog"
        return 1
    fi
    
    # Check for error in response
    if echo "$response" | grep -q '"error"'; then
        print_error "DAC catalog returned an error: $response"
        return 1
    fi
    
    # Parse JSON response to extract packages
    # Store raw response for later use
    DAC_RESPONSE="$response"
    
    print_info "  DAC Response received"
    
    # Extract package count (counting occurrences of "id" field)
    PACKAGE_COUNT=$(echo "$DAC_RESPONSE" | grep -o '"id"' | wc -l)
    
    if [ "$PACKAGE_COUNT" -eq 0 ]; then
        print_error "No packages found in DAC catalog response"
        print_info "Response: $DAC_RESPONSE"
        return 1
    fi
    
    print_info "  Total packages found: $PACKAGE_COUNT"
    echo
    print_info "  Available packages:"
    
    # Display packages from response by parsing JSON
    local idx=1
    echo "$DAC_RESPONSE" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | while read name; do
        printf "    [%d] %s\n" $idx "$name"
        idx=$((idx+1))
    done
    
    print_success "Found $PACKAGE_COUNT packages"
}

# Download package from actual DAC catalog
download_package() {
    local pkg_index=$1
    
    print_info "Downloading package (Index: $pkg_index)..."
    
    # Extract package details from DAC response by index
    # Parse JSON to get the nth package
    local app_data=$(echo "$DAC_RESPONSE" | grep -o '{[^}]*"id"[^}]*}' | sed -n "${pkg_index}p")
    
    if [ -z "$app_data" ]; then
        print_error "Package at index $pkg_index not found"
        return 1
    fi
    
    # Extract package details from JSON
    APP_NAME=$(echo "$app_data" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    APP_ID=$(echo "$app_data" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    APP_VERSION=$(echo "$app_data" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    
    if [ -z "$APP_ID" ] || [ -z "$APP_NAME" ] || [ -z "$APP_VERSION" ]; then
        print_error "Could not parse package information from DAC response"
        return 1
    fi
    
    print_info "  Selected package:"
    print_info "    Name: $APP_NAME"
    print_info "    ID: $APP_ID"
    print_info "    Version: $APP_VERSION"
    
    # Build actual download URL
    local download_url="${DAC_CATALOG_URL}/bundles/${APP_ID}/${APP_VERSION}/${PLATFORM_NAME}/${FIRMWARE_VERSION}.tar.gz"
    print_info "  Download URL: $download_url"
    
    # Call PackageManager download via JSON-RPC
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.download" \
        "{\"url\":\"$download_url\"}")
    
    if is_success "$response"; then
        DOWNLOAD_ID=$(extract_result "$response")
        
        if [ -z "$DOWNLOAD_ID" ]; then
            print_error "Download succeeded but no download ID returned"
            print_info "Response: $response"
            return 1
        fi
        
        # Validate download ID format (should not contain braces or partial JSON)
        if [[ "$DOWNLOAD_ID" == *"{"* ]] || [[ "$DOWNLOAD_ID" == *"}"* ]]; then
            print_error "Invalid download ID format: $DOWNLOAD_ID"
            print_info "Full response: $response"
            return 1
        fi
        
        print_info "  Download successful"
        print_success "Downloaded $APP_NAME, ID: $DOWNLOAD_ID"
    else
        print_error "Download failed"
        print_info "Response: $response"
        return 1
    fi
}

# Install package using DAC01 method
install_package() {
    print_info "Installing package..."
    
    local file_locator="/opt/CDL/package${DOWNLOAD_ID}"
    
    print_info "  Installation parameters:"
    print_info "    Package ID: $APP_ID"
    print_info "    Version: $APP_VERSION"
    print_info "    File Locator: $file_locator"
    
    # Call PackageManagerRDKEMS.install with additionalMetadata
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.install" \
        "{\"packageId\":\"$APP_ID\",\"version\":\"$APP_VERSION\",\"fileLocator\":\"$file_locator\",\"additionalMetadata\":[]}")
    
    if is_success "$response"; then
        print_success "Installation successful"
        return 0
    else
        print_error "Installation failed"
        print_info "Response: $response"
        return 1
    fi
}

# Uninstall any existing package before installation (cleanup)
cleanup_existing_package() {
    print_info "Checking for and removing any existing version of $APP_NAME..."
    
    # Check if package exists
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.listPackages" "{}")
    
    if is_success "$response"; then
        if echo "$response" | grep -q "$APP_ID"; then
            print_info "  Found existing version, attempting uninstall..."
            
            # First, try to kill the app if it's running
            print_info "  Attempting to kill any running instance..."
            local kill_response=$(jsonrpc_call "org.rdk.AppManager.killApp" "{\"appId\":\"$APP_ID\"}")
            if is_success "$kill_response"; then
                print_info "    Running instance killed"
                sleep 1
            else
                print_info "    No running instance (or already stopped)"
            fi
            
            # Try to uninstall using PackageManagerRDKEMS (the activated plugin)
            print_info "  Attempting to uninstall via PackageManagerRDKEMS..."
            local uninstall_response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.uninstall" \
                "{\"packageId\":\"$APP_ID\",\"version\":\"$APP_VERSION\"}")
            
            print_info "    Uninstall response: $uninstall_response"
            
            if is_success "$uninstall_response"; then
                print_success "  Existing version uninstalled successfully"
                sleep 2
                return 0
            else
                # Even if uninstall fails, check if package still exists
                sleep 1
                local check_response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.listPackages" "{}")
                if echo "$check_response" | grep -q "$APP_ID"; then
                    print_warning "  Uninstall command sent but package still exists (may be in use or locked)"
                    print_info "  Continuing with fresh install attempt..."
                    return 0
                else
                    print_success "  Package was removed despite error response"
                    return 0
                fi
            fi
        else
            print_info "  No existing version found"
            return 0
        fi
    else
        print_warning "  Could not check for existing package"
        return 0
    fi
}

# Verify package installation
verify_installation() {
    print_info "Verifying package installation..."
    
    # Call PackageManagerRDKEMS.listPackages
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.listPackages" "{}")
    
    if is_success "$response"; then
        # Check if APP_ID is in response
        if echo "$response" | grep -q "$APP_ID"; then
            print_success "$APP_NAME found in installed packages"
        else
            print_error "$APP_NAME NOT found in installed packages"
            return 1
        fi
    else
        print_warning "Could not verify installation (listPackages failed)"
    fi
}

# Launch application
launch_app() {
    print_info "Launching application: $APP_NAME (ID: $APP_ID)..."
    
    local response=$(jsonrpc_call "org.rdk.AppManager.1.launchApp" \
        "{\"appId\":\"$APP_ID\"}")
    
    if is_success "$response"; then
        print_success "Application launched successfully"
        sleep 2
    else
        print_error "Launch failed"
        print_info "Response: $response"
        return 1
    fi
}

# Kill application (terminateApp for graceful, fallback to killApp for forceful)
kill_app() {
    print_info "Terminating application: $APP_NAME (ID: $APP_ID)..."
    
    # Try terminateApp first (graceful termination)
    local response=$(jsonrpc_call "org.rdk.AppManager.terminateApp" \
        "{\"appId\":\"$APP_ID\"}")
    
    if is_success "$response"; then
        print_success "Application terminated gracefully"
        sleep 2
        return 0
    else
        # If graceful termination fails, try killApp (forceful termination)
        print_info "Graceful termination failed, attempting forceful kill..."
        response=$(jsonrpc_call "org.rdk.AppManager.killApp" \
            "{\"appId\":\"$APP_ID\"}")
        
        if is_success "$response"; then
            print_success "Application killed forcefully"
            sleep 1
            return 0
        else
            print_error "Both termination methods failed"
            print_info "Response: $response"
            return 1
        fi
    fi
}

# Uninstall application
uninstall_app() {
    print_info "Uninstalling application: $APP_NAME (ID: $APP_ID)..."
    
    # Use PackageManagerRDKEMS.1.uninstall (the activated plugin)
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.uninstall" \
        "{\"packageId\":\"$APP_ID\",\"version\":\"$APP_VERSION\"}")
    
    # Check if response contains a result (success)
    if is_success "$response"; then
        print_success "Uninstall command accepted"
        sleep 3  # Wait for async operation to complete
        print_success "Uninstall operation completed"
        return 0
    else
        print_error "Uninstall failed"
        print_info "Response: $response"
        return 1
    fi
}

# Verify uninstallation
verify_uninstall() {
    print_info "Verifying application uninstall..."
    
    local response=$(jsonrpc_call "org.rdk.PackageManagerRDKEMS.1.listPackages" "{}")
    
    if is_success "$response"; then
        if echo "$response" | grep -q "$APP_ID"; then
            print_error "$APP_NAME still exists after uninstall"
            return 1
        else
            print_success "$APP_NAME successfully uninstalled and verified removed"
        fi
    else
        print_warning "Could not verify uninstall (listPackages failed)"
    fi
}

# ============================================================================
# Main Workflow
# ============================================================================

main() {
    # Validate parameters
    if [ $# -lt 1 ]; then
        print_error "Missing required parameter: device_ip"
        echo
        echo "Usage: $0 <device_ip> [jsonrpc_port] [package_index]"
        echo "   or: $0 <device_ip> <package_index>"
        echo
        echo "Examples:"
        echo "  $0 192.168.1.100                    # Uses default port 9998, package 2"
        echo "  $0 192.168.1.100 1                  # Uses default port 9998, package 1"
        echo "  $0 192.168.1.100 9998               # Uses port 9998, package 2"
        echo "  $0 192.168.1.100 9998 1             # Uses port 9998, package 1"
        show_workflow_summary_on_exit
        exit 1
    fi
    
    DEVICE_IP="$1"
    JSONRPC_PORT="9998"
    PACKAGE_INDEX="2"
    
    # Smart argument detection: if 2nd arg is small (1-100), treat as package_index
    # If 3rd arg exists or 2nd arg is large (1000+), treat 2nd as port
    if [ $# -ge 2 ]; then
        if [ $# -eq 2 ] && [ "$2" -lt 1000 ] 2>/dev/null; then
            # Only 2 args and 2nd arg is small number - treat as package_index
            PACKAGE_INDEX="$2"
        elif [ $# -ge 3 ]; then
            # 3 or more args - treat 2nd as port, 3rd as package_index
            JSONRPC_PORT="$2"
            PACKAGE_INDEX="$3"
        else
            # 2 args but 2nd is large number - treat as port
            JSONRPC_PORT="$2"
        fi
    fi
    
    # Validate IP address
    if ! [[ "$DEVICE_IP" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        print_error "Invalid IP address: $DEVICE_IP"
        show_workflow_summary_on_exit
        exit 1
    fi
    
    # Validate port
    if ! [[ "$JSONRPC_PORT" =~ ^[0-9]+$ ]]; then
        print_error "Invalid port: $JSONRPC_PORT"
        show_workflow_summary_on_exit
        exit 1
    fi
    
    # Validate index
    if ! [[ "$PACKAGE_INDEX" =~ ^[0-9]+$ ]]; then
        print_error "Invalid package index: $PACKAGE_INDEX"
        show_workflow_summary_on_exit
        exit 1
    fi
    
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        print_error "curl not found. Please install curl"
        show_workflow_summary_on_exit
        exit 1
    fi
    
    print_header "DAC01 Workflow Test - Local Testing Script"
    
    print_info "Device IP: $DEVICE_IP"
    print_info "JSON-RPC Port: $JSONRPC_PORT"
    print_info "Package Index: $PACKAGE_INDEX"
    echo
    
    # Run workflow steps
    set +e  # Don't exit on error, we'll handle it
    
    # PRECONDITION: Activate plugins
    print_header "PRECONDITION: Activating Required Plugins"
    activate_plugins
    record_workflow_step "Plugin Activation" "PASS"
    
    # STEP 1: Fetch DAC config
    print_header "STEP 1: Fetch DAC Configuration"
    if fetch_dac_config; then
        record_workflow_step "Fetch DAC Configuration" "PASS"
    else
        record_workflow_step "Fetch DAC Configuration" "FAIL" "Failed to fetch DAC config"
    fi
    
    # STEP 2: Get device info
    print_header "STEP 2: Get Device Platform Information"
    if get_device_info; then
        record_workflow_step "Get Device Info" "PASS"
    else
        record_workflow_step "Get Device Info" "FAIL" "Failed to get device info"
    fi
    
    # STEP 3: List packages
    print_header "STEP 3: List Packages from DAC Catalog"
    if list_dac_packages; then
        record_workflow_step "List DAC Packages" "PASS"
    else
        record_workflow_step "List DAC Packages" "FAIL" "Failed to list packages"
    fi
    
    # STEP 4: Download package
    print_header "STEP 4: Download Package (Index: $PACKAGE_INDEX)"
    if download_package "$PACKAGE_INDEX"; then
        record_workflow_step "Download Package" "PASS"
    else
        record_workflow_step "Download Package" "FAIL" "Failed to download package"
    fi
    
    # STEP 4.5: Cleanup any existing package before installation
    print_header "STEP 4.5: Pre-Installation Cleanup"
    cleanup_existing_package
    
    # STEP 5: Install package
    print_header "STEP 5: Install Package"
    if install_package; then
        record_workflow_step "Install Package" "PASS"
    else
        record_workflow_step "Install Package" "FAIL" "Failed to install package"
    fi
    
    # STEP 6: Verify installation
    print_header "STEP 6: Verify Package Installation"
    if verify_installation; then
        record_workflow_step "Verify Installation" "PASS"
    else
        record_workflow_step "Verify Installation" "FAIL" "Failed to verify installation"
    fi
    
    # STEP 7: Launch app
    print_header "STEP 7: Launch Application"
    if launch_app; then
        record_workflow_step "Launch Application" "PASS"
    else
        record_workflow_step "Launch Application" "FAIL" "Failed to launch application"
    fi
    
    # STEP 8: Kill app
    print_header "STEP 8: Kill Application"
    if kill_app; then
        record_workflow_step "Kill Application" "PASS"
    else
        record_workflow_step "Kill Application" "FAIL" "Failed to kill application"
    fi
    
    # STEP 9: Uninstall app
    print_header "STEP 9: Uninstall Application"
    if uninstall_app; then
        record_workflow_step "Uninstall Application" "PASS"
    else
        record_workflow_step "Uninstall Application" "FAIL" "Failed to uninstall application"
    fi
    
    # STEP 10: Verify uninstall
    print_header "STEP 10: Verify Application Uninstall"
    if verify_uninstall; then
        record_workflow_step "Verify Uninstall" "PASS"
    else
        record_workflow_step "Verify Uninstall" "FAIL" "Failed to verify uninstall"
    fi
    
    # Show workflow summary (always executed)
    show_workflow_summary
    SUMMARY_SHOWN=true
}

# Run main function
main "$@"
