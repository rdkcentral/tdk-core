#!/bin/bash

##########################################################################
# PackageManager Plugin Validation Script for RDK Devices
# 
# Purpose: Validate PackageManager plugin availability and health on RDK device
# This script can run independently without full TDK framework
# Can be run on Linux/macOS or deployed to RDK device via SSH
#
# Usage: ./validate_packagemanager_plugins.sh [options]
#
# Options:
#   -h, --host HOSTNAME/IP          Device hostname or IP (default: localhost:9998)
#   -p, --port PORT                 JSONRPC port (default: 9998)
#   -d, --device-ip IP              Device IP address (default: 127.0.0.1)
#   --deploy-to-device [USER@HOST]  Copy script to RDK device and execute
#   --verbose                       Enable verbose output
#   --help                          Show this help message
#
# Examples:
#   # Local execution (connects to localhost)
#   ./validate_packagemanager_plugins.sh
#
#   # Connect to remote device
#   ./validate_packagemanager_plugins.sh -h 192.168.1.100
#
#   # Deploy and run on RDK device (requires SSH)
#   ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.1.100
#
##########################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
DEVICE_IP="127.0.0.1"
JSONRPC_PORT="9998"
VERBOSE=false
DEPLOY_MODE=false
SSH_TARGET=""
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME="validate_packagemanager_plugins.sh"

# Plugin names to validate
declare -a PLUGINS=(
    "org.rdk.PackageManagerRDKEMS"
    "org.rdk.PackageManager"
)

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_help() {
    head -n 28 "$0" | tail -n 24
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[DEBUG] $1${NC}"
    fi
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--host)
                DEVICE_IP="${2%%:*}"
                if [[ "$2" == *":"* ]]; then
                    JSONRPC_PORT="${2##*:}"
                fi
                shift 2
                ;;
            -p|--port)
                JSONRPC_PORT="$2"
                shift 2
                ;;
            -d|--device-ip)
                DEVICE_IP="$2"
                shift 2
                ;;
            --deploy-to-device)
                DEPLOY_MODE=true
                SSH_TARGET="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Send JSONRPC request to device
send_jsonrpc_request() {
    local plugin=$1
    local method=$2
    local params=${3:-"{}"}
    
    local request=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "${plugin}.1.${method}",
    "params": ${params}
}
EOF
)
    
    log_verbose "Request: $request"
    
    local response=$(curl -s -X POST \
        "http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc" \
        -H "Content-Type: application/json" \
        -d "$request" 2>/dev/null || echo '{"error":"connection_failed"}')
    
    log_verbose "Response: $response"
    echo "$response"
}

# Check if curl is available
check_dependencies() {
    print_header "Checking Dependencies"
    
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed. Please install curl to continue."
        exit 1
    fi
    print_success "curl is available"
    
    if ! command -v jq &> /dev/null; then
        print_warning "jq is not installed. Some features will be limited."
    else
        print_success "jq is available"
    fi
}

# Check and start Thunder/WPE services if needed
check_and_start_services() {
    print_header "Checking Thunder/WPE Services"
    
    # Check if we're on an RDK device
    if ! command -v systemctl &> /dev/null; then
        print_warning "systemctl not available - skipping service checks"
        return 0
    fi
    
    # Check if WPEFramework service exists
    if systemctl list-unit-files | grep -q "wpeframework"; then
        print_info "Checking WPEFramework service status..."
        
        if systemctl is-active --quiet wpeframework; then
            print_success "WPEFramework service is running"
            return 0
        else
            print_warning "WPEFramework service is not running"
            print_info "Attempting to start WPEFramework service..."
            
            if systemctl start wpeframework 2>/dev/null; then
                print_success "WPEFramework service started"
                print_info "Waiting for service to fully initialize (5 seconds)..."
                sleep 5
                return 0
            else
                print_error "Failed to start WPEFramework service"
                print_info "Try manually: sudo systemctl start wpeframework"
                return 1
            fi
        fi
    elif systemctl list-unit-files | grep -q "thunder"; then
        print_info "Checking Thunder service status..."
        
        if systemctl is-active --quiet thunder; then
            print_success "Thunder service is running"
            return 0
        else
            print_warning "Thunder service is not running"
            print_info "Attempting to start Thunder service..."
            
            if systemctl start thunder 2>/dev/null; then
                print_success "Thunder service started"
                print_info "Waiting for service to fully initialize (5 seconds)..."
                sleep 5
                return 0
            else
                print_error "Failed to start Thunder service"
                print_info "Try manually: sudo systemctl start thunder"
                return 1
            fi
        fi
    else
        print_warning "Neither WPEFramework nor Thunder service found"
        print_info "RDK services may be running under a different name"
        return 0
    fi
}

# Test device connectivity
test_connectivity() {
    print_header "Testing Device Connectivity"
    
    print_info "Attempting to connect to ${DEVICE_IP}:${JSONRPC_PORT}..."
    
    local response=$(send_jsonrpc_request "org.rdk.System" "getSystemVersions" "{}")
    log_verbose "Connectivity test response: $response"
    
    # Check for connection error
    if echo "$response" | grep -q "connection_failed"; then
        print_error "Cannot connect to device at ${DEVICE_IP}:${JSONRPC_PORT}"
        print_error "Connection failed - device unreachable"
        print_info "Troubleshooting:"
        print_info "  1. Verify device IP: ping ${DEVICE_IP}"
        print_info "  2. Check device is powered on"
        print_info "  3. Verify network connectivity"
        print_info "  4. Check Thunder/RDK Services are running"
        return 1
    fi
    
    # Check for valid response (has jsonrpc field)
    if echo "$response" | grep -q '"jsonrpc"'; then
        print_success "Successfully connected to device"
        log_verbose "Valid JSONRPC response received"
        return 0
    else
        print_error "Invalid response from device"
        print_warning "Response: $response"
        return 1
    fi
}

# Check plugin availability using Controller
check_plugin_availability() {
    print_header "Checking Plugin Availability"
    
    print_info "Querying available plugins via Controller..."
    local response=$(send_jsonrpc_request "org.rdk.System" "plugins" "{}")
    log_verbose "Plugins response: $response"
    
    # Check if we got a valid response
    if ! echo "$response" | grep -q '"jsonrpc"'; then
        print_warning "Could not retrieve plugins list"
        print_info "Note: org.rdk.System.plugins method may not be available on this device"
        print_info ""
        print_info "Manual curl command to test plugin availability:"
        print_info "curl -X POST http://127.0.0.1:9998/jsonrpc \\"
        print_info "  -H 'Content-Type: application/json' \\"
        print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"org.rdk.System.plugins\",\"params\":{}}'"
        print_info ""
        return 1
    fi
    
    for plugin in "${PLUGINS[@]}"; do
        log_verbose "Checking plugin: $plugin"
        
        if echo "$response" | grep -q "$plugin"; then
            print_success "Plugin $plugin is available"
        else
            print_warning "Plugin $plugin not found"
        fi
    done
    
    # Show what plugins are actually available
    print_info ""
    print_info "Available RDK plugins on device:"
    echo "$response" | grep -o 'org\.rdk\.[^"]*' | sort | uniq || print_info "Could not extract plugin list"
    
    # Show curl command used
    print_info ""
    print_info "Curl command used (for manual testing):"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"org.rdk.System.plugins\",\"params\":{}}'"
    print_info ""
}

# Activate plugin using Controller
activate_plugin() {
    local plugin=$1
    
    print_info "Activating plugin: $plugin"
    print_info "Curl command:"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"Controller.1.activate\",\"params\":{\"callsign\":\"$plugin\"}}'"
    print_info ""
    
    local response=$(send_jsonrpc_request "Controller" "activate" "{\"callsign\": \"$plugin\"}")
    log_verbose "Activate response: $response"
    
    if echo "$response" | grep -q '"result"'; then
        print_success "Plugin activated successfully"
        return 0
    else
        print_warning "Activation response: $response"
        return 1
    fi
}

# Test plugin methods by calling actual APIs
test_plugin_activation() {
    print_header "Testing PackageManager Plugin Methods"
    
    local plugin="org.rdk.PackageManagerRDKEMS"
    
    print_info "Testing plugin: $plugin"
    print_info "Attempting to call listPackages method..."
    print_info ""
    print_info "Curl command:"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.listPackages\"}'"
    print_info ""
    
    local response=$(curl -s -X POST "http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc" \
        -H "Content-Type: application/json" \
        -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.listPackages\"}")
    log_verbose "listPackages response: $response"
    
    # Check for success
    if echo "$response" | grep -q '"result"'; then
        print_success "Plugin is accessible - listPackages returned results"
        print_info "Response: $response"
        return 0
    elif echo "$response" | grep -q '"error"'; then
        # Extract error message (BusyBox compatible)
        local error_msg=$(echo "$response" | grep -o '"message":"[^"]*' | sed -n '1p' | cut -d'"' -f4)
        local error_code=$(echo "$response" | grep -o '"code":[^,}]*' | sed -n '1p' | cut -d':' -f2)
        
        print_warning "Response: $response"
        print_warning "Plugin method returned error (Code: $error_code): $error_msg"
        return 1
    fi
    
    print_warning "Unexpected response from plugin: $response"
    return 1
}
    log_verbose "getList response: $response"
    
    # Check for success (has result field or error field with code)
    if echo "$response" | grep -q '"result"'; then
        print_success "Plugin is accessible - getList returned results"
        print_info "Response: $response"
        return 0
    elif echo "$response" | grep -q '"error"'; then
        # Extract error message (BusyBox compatible)
        local error_msg=$(echo "$response" | grep -o '"message":"[^"]*' | sed -n '1p' | cut -d'"' -f4)
        local error_code=$(echo "$response" | grep -o '"code":[^,}]*' | sed -n '1p' | cut -d':' -f2)
        
        print_warning "Response: $response"
        
        if [ "$error_code" = "2" ]; then
            print_error "Plugin method call failed: Service is not active (Code: 2)"
            print_warning "The RDK Service/Thunder framework may not have the plugin activated"
            print_info "On device, check:"
            print_info "  1. Thunder/RDK services status: systemctl status wpeframework"
            print_info "  2. Check device logs: tail -f /opt/logs/*.log"
            print_info "  3. List loaded plugins: curl -X POST http://127.0.0.1:9998/jsonrpc -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"org.rdk.System.plugins\",\"params\":{}}'"
        elif [ "$error_code" = "-32602" ]; then
            print_warning "Invalid method or parameters (Code: -32602): $error_msg"
            print_info "The plugin may not support 'getList' or requires different parameters"
        else
            print_warning "Plugin method returned error (Code: $error_code): $error_msg"
        fi
        return 1
    fi
    
    # Check for timeout or no response
    if [ -z "$response" ]; then
        print_error "No response from device when calling plugin method"
        print_warning "Possible causes:"
        print_warning "  - Plugin is not loaded"
        print_warning "  - Device is unresponsive"
        print_warning "  - Network timeout"
        return 1
    fi
    
    print_warning "Unexpected response from plugin: $response"
    return 1
}

# Test basic API methods
test_basic_apis() {
    print_header "Testing PackageManager API Examples"
    
    local plugin="org.rdk.PackageManagerRDKEMS"
    
    print_info ""
    print_info "Example API calls for reference:"
    print_info ""
    
    print_info "1. Download API:"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.download\",\"params\":{\"url\":\"<package-url>\"}}'"
    print_info ""
    
    print_info "2. Install API:"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.install\",\"params\":{\"packageId\":\"<pkg-id>\",\"version\":\"<version>\",\"fileLocator\":\"<file-path>\"}}'"
    print_info ""
    
    print_info "3. Get Status API:"
    print_info "curl -X POST http://${DEVICE_IP}:${JSONRPC_PORT}/jsonrpc \\"
    print_info "  -H 'Content-Type: application/json' \\"
    print_info "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.getStatus\",\"params\":{\"id\":\"<operation-id>\"}}'"
    print_info ""
}

# Generate summary report
generate_summary() {
    print_header "Validation Summary"
    
    cat > "${SCRIPT_DIR}/plugin_validation_report.txt" <<EOF
PackageManager Plugin Validation Report
Generated: $(date)
Device: ${DEVICE_IP}:${JSONRPC_PORT}

SYSTEM INFORMATION:
- Device IP: ${DEVICE_IP}
- JSONRPC Port: ${JSONRPC_PORT}
- Script Location: ${SCRIPT_DIR}

PLUGINS CHECKED:
EOF
    
    for plugin in "${PLUGINS[@]}"; do
        echo "- $plugin" >> "${SCRIPT_DIR}/plugin_validation_report.txt"
    done
    
    cat >> "${SCRIPT_DIR}/plugin_validation_report.txt" <<EOF

NEXT STEPS:
1. If all checks passed, PackageManager is ready for testing
2. Run individual test scripts from the PackageManager directory
3. For detailed API testing, use the TDK test framework

TROUBLESHOOTING:
- Connection Issues: Verify device IP and port are correct
- Plugin Not Found: Check Thunder/RDK Services are running
- API Failures: Ensure plugin is properly activated
- For more info: Review Thunder/RDK device logs

Report saved to: ${SCRIPT_DIR}/plugin_validation_report.txt
EOF
    
    cat "${SCRIPT_DIR}/plugin_validation_report.txt"
}

# Deploy script to RDK device via SSH
deploy_to_device() {
    print_header "Deploying to RDK Device"
    
    if [ -z "$SSH_TARGET" ]; then
        print_error "SSH target not specified"
        print_info "Usage: $0 --deploy-to-device root@192.168.1.100"
        exit 1
    fi
    
    print_info "Deploying script to device: $SSH_TARGET"
    
    # Check if SSH is available
    if ! command -v ssh &> /dev/null; then
        print_error "SSH is not installed. Cannot deploy to device."
        print_info "Install SSH client to use --deploy-to-device option"
        exit 1
    fi
    
    # Extract device IP from SSH target
    local target_ip="${SSH_TARGET##*@}"
    
    print_info "Checking device connectivity via SSH..."
    if ! ssh -o ConnectTimeout=5 "$SSH_TARGET" "echo 'SSH connection OK'" &>/dev/null; then
        print_error "Cannot reach device at $SSH_TARGET via SSH"
        print_info "Troubleshooting:"
        print_info "  1. Verify device IP: $target_ip"
        print_info "  2. Verify device is reachable: ping $target_ip"
        print_info "  3. Verify SSH is enabled on device"
        print_info "  4. Verify credentials: ssh $SSH_TARGET"
        exit 1
    fi
    print_success "SSH connection established"
    
    # Copy script to device
    print_info "Copying script to device..."
    scp -q "$0" "$SSH_TARGET:/tmp/$SCRIPT_NAME" 2>/dev/null
    if [ $? -ne 0 ]; then
        print_error "Failed to copy script to device"
        exit 1
    fi
    print_success "Script copied to device"
    
    # Make script executable on device
    print_info "Making script executable on device..."
    ssh "$SSH_TARGET" "chmod +x /tmp/$SCRIPT_NAME" 2>/dev/null
    print_success "Script is executable"
    
    # Run script on device
    print_header "Executing Validation on Device"
    print_info "Running validation script on device: $SSH_TARGET"
    echo ""
    
    # Execute with parameters
    ssh "$SSH_TARGET" "/tmp/$SCRIPT_NAME --verbose" 2>/dev/null
    
    # Check for results and copy back
    print_info "Retrieving validation report from device..."
    if ssh "$SSH_TARGET" "test -f /tmp/plugin_validation_report.txt" 2>/dev/null; then
        scp -q "$SSH_TARGET:/tmp/plugin_validation_report.txt" "${SCRIPT_DIR}/plugin_validation_report_device.txt" 2>/dev/null
        print_success "Report retrieved from device"
        print_info "Saved to: ${SCRIPT_DIR}/plugin_validation_report_device.txt"
    fi
    
    # Cleanup on device
    ssh "$SSH_TARGET" "rm -f /tmp/$SCRIPT_NAME /tmp/plugin_validation_report.txt" 2>/dev/null
    
    print_header "Deployment Complete"
    print_success "Device validation completed successfully!"
}

# Main execution
main() {
    print_header "PackageManager Plugin Validator v1.0"
    
    parse_arguments "$@"
    
    # Check if deploying to device
    if [ "$DEPLOY_MODE" = true ]; then
        deploy_to_device
        exit 0
    fi
    
    print_info "Configuration:"
    print_info "  Device IP: ${DEVICE_IP}"
    print_info "  JSONRPC Port: ${JSONRPC_PORT}"
    print_info "  Verbose: ${VERBOSE}"
    print_info "  Mode: Local execution"
    
    check_dependencies
    
    # Check and start services if running on RDK device
    if ! check_and_start_services; then
        print_warning "Service check failed, but continuing with connectivity test"
    fi
    
    if ! test_connectivity; then
        print_error "Validation failed: Cannot connect to device"
        print_info "To deploy to RDK device, use: $0 --deploy-to-device root@<device-ip>"
        exit 1
    fi
    
    check_plugin_availability
    
    # Activate the plugin before testing
    print_header "Activating PackageManager Plugin"
    activate_plugin "org.rdk.PackageManagerRDKEMS"
    
    test_plugin_activation
    test_basic_apis
    generate_summary
    
    print_header "Validation Complete"
    print_success "PackageManager plugin validation completed successfully!"
}

# Run main function
main "$@"
