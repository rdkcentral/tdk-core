#!/bin/bash

##########################################################################
# RDK Device Setup and Validation Script
#
# Purpose: Quick setup and validation on RDK device
# - Checks/starts Thunder services
# - Validates PackageManager plugin
# - Generates detailed report
#
# Usage: bash setup_and_validate.sh [--auto-start] [--verbose]
#
##########################################################################

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
AUTO_START=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-start)
            AUTO_START=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

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

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_warning "Not running as root - some operations may fail"
        print_info "For full functionality, run: sudo bash setup_and_validate.sh"
    fi
}

# Check Thunder service status
check_thunder_status() {
    print_header "Checking Thunder/WPE Services"
    
    if ! command -v systemctl &> /dev/null; then
        print_error "systemctl not found - cannot check services"
        return 1
    fi
    
    # Check WPEFramework
    if systemctl list-unit-files | grep -q "wpeframework"; then
        print_info "WPEFramework service found"
        
        if systemctl is-active --quiet wpeframework; then
            print_success "WPEFramework is RUNNING"
            return 0
        else
            print_warning "WPEFramework is STOPPED"
            
            if [ "$AUTO_START" = true ]; then
                print_info "Attempting to start WPEFramework..."
                if sudo systemctl start wpeframework 2>/dev/null; then
                    print_success "WPEFramework started successfully"
                    sleep 3
                    return 0
                else
                    print_error "Failed to start WPEFramework"
                    return 1
                fi
            else
                print_info "Use --auto-start to start services automatically"
                return 1
            fi
        fi
    elif systemctl list-unit-files | grep -q "thunder"; then
        print_info "Thunder service found"
        
        if systemctl is-active --quiet thunder; then
            print_success "Thunder is RUNNING"
            return 0
        else
            print_warning "Thunder is STOPPED"
            
            if [ "$AUTO_START" = true ]; then
                print_info "Attempting to start Thunder..."
                if sudo systemctl start thunder 2>/dev/null; then
                    print_success "Thunder started successfully"
                    sleep 3
                    return 0
                else
                    print_error "Failed to start Thunder"
                    return 1
                fi
            else
                print_info "Use --auto-start to start services automatically"
                return 1
            fi
        fi
    else
        print_error "No Thunder/WPE services found"
        return 1
    fi
}

# Test JSONRPC connectivity
test_jsonrpc() {
    print_header "Testing JSONRPC Connectivity"
    
    print_info "Testing connection to 127.0.0.1:9998..."
    
    local response=$(curl -s -X POST "http://127.0.0.1:9998/jsonrpc" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.System.1.getSystemVersions","params":{}}' \
        2>/dev/null || echo '{"error":"connection_failed"}')
    
    if echo "$response" | grep -q "connection_failed"; then
        print_error "Cannot connect to JSONRPC service"
        return 1
    fi
    
    if echo "$response" | grep -q '"jsonrpc"'; then
        print_success "JSONRPC connection OK"
        
        # Extract system version
        local version=$(echo "$response" | grep -o '"stbVersion":"[^"]*' | cut -d'"' -f4)
        if [ -n "$version" ]; then
            print_info "System Version: $version"
        fi
        return 0
    else
        print_error "Invalid JSONRPC response"
        print_warning "Response: $response"
        return 1
    fi
}

# List available plugins
list_plugins() {
    print_header "Checking Available Plugins"
    
    print_info "Querying Thunder for available plugins..."
    
    local response=$(curl -s -X POST "http://127.0.0.1:9998/jsonrpc" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"Controller.1.plugins","params":{}}' \
        2>/dev/null || echo '{}')
    
    if echo "$response" | grep -q "PackageManager"; then
        print_success "PackageManager plugin is available"
    else
        print_warning "PackageManager plugin not found in plugins list"
    fi
    
    if [ "$VERBOSE" = true ]; then
        print_info "Available plugins:"
        echo "$response" | grep -o '"[^"]*":' | head -20
    fi
}

# Test PackageManager API
test_packagemanager_api() {
    print_header "Testing PackageManager API"
    
    local plugin="org.rdk.PackageManagerRDKEMS"
    
    print_info "Testing getList API..."
    local response=$(curl -s -X POST "http://127.0.0.1:9998/jsonrpc" \
        -H "Content-Type: application/json" \
        -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"${plugin}.1.getList\",\"params\":{}}" \
        2>/dev/null || echo '{}')
    
    if echo "$response" | grep -q "result\|success"; then
        print_success "getList API is functional"
    else
        print_warning "getList API response: $response"
    fi
}

# Generate summary report
generate_report() {
    print_header "Generating Report"
    
    local report_file="/tmp/rdk_device_status_report.txt"
    
    cat > "$report_file" <<EOF
RDK Device Status Report
Generated: $(date)
Hostname: $(hostname)

SYSTEM INFORMATION:
- Device: $(cat /etc/hostname 2>/dev/null || echo "Unknown")
- Kernel: $(uname -r)
- Uptime: $(uptime -p 2>/dev/null || uptime)

THUNDER/WPE SERVICES:
EOF
    
    if systemctl is-active --quiet wpeframework; then
        echo "- WPEFramework: RUNNING ($(systemctl show -p Version --value wpeframework 2>/dev/null || echo 'Version unknown'))" >> "$report_file"
    elif systemctl is-active --quiet thunder; then
        echo "- Thunder: RUNNING" >> "$report_file"
    else
        echo "- Services: NOT RUNNING" >> "$report_file"
    fi
    
    cat >> "$report_file" <<EOF

JSONRPC SERVICE:
- Port: 9998
- Status: $(curl -s http://127.0.0.1:9998/jsonrpc >/dev/null 2>&1 && echo "RESPONDING" || echo "NOT RESPONDING")

PACKAGEMANAGER PLUGIN:
- Name: org.rdk.PackageManagerRDKEMS
- Status: Check getList API result above

RECOMMENDATIONS:
1. Keep Thunder/WPE services running for continuous operation
2. Enable auto-start: systemctl enable wpeframework
3. Monitor logs: journalctl -u wpeframework -f

Report saved to: $report_file
EOF
    
    print_success "Report saved to: $report_file"
    cat "$report_file"
}

# Main execution
main() {
    print_header "RDK Device Setup & Validation v1.0"
    
    echo ""
    print_info "Options: Auto-Start=$AUTO_START, Verbose=$VERBOSE"
    echo ""
    
    check_root
    
    if ! check_thunder_status; then
        if [ "$AUTO_START" = false ]; then
            print_error "Thunder services not running"
            print_info "Run with --auto-start to start services automatically"
            print_info "Or run manually: sudo systemctl start wpeframework"
            exit 1
        fi
    fi
    
    if ! test_jsonrpc; then
        print_error "Cannot reach JSONRPC service"
        print_info "Wait a few seconds and try again"
        exit 1
    fi
    
    list_plugins
    test_packagemanager_api
    generate_report
    
    print_header "Setup & Validation Complete"
    print_success "Device is ready for PackageManager testing!"
}

main "$@"
