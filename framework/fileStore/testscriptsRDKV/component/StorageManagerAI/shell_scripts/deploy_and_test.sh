#!/bin/bash
# Quick deployment and testing script for validateStorageMgr.sh on RDK devices
# Usage: bash deploy_and_test.sh <device_ip> [device_user] [device_port]

DEVICE_IP="${1:-127.0.0.1}"
DEVICE_USER="${2:-root}"
DEVICE_PORT="${3:-22}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "StorageManager Test Suite - Device Deployment"
echo "=========================================="
echo ""

# Validate inputs
if [ -z "$DEVICE_IP" ]; then
    echo "[ERROR] Device IP is required"
    echo "Usage: bash $0 <device_ip> [device_user] [device_port]"
    exit 1
fi

echo "[INFO] Configuration:"
echo "  Device IP:   $DEVICE_IP"
echo "  Device User: $DEVICE_USER"
echo "  SSH Port:    $DEVICE_PORT"
echo ""

# Step 1: Test SSH connectivity
echo "[STEP 1] Testing SSH connectivity..."
if ssh -p $DEVICE_PORT ${DEVICE_USER}@${DEVICE_IP} "echo 'SSH connection successful'" 2>/dev/null | grep -q "successful"; then
    echo "[PASS] SSH connection successful"
else
    echo "[FAIL] Cannot connect to device. Check IP, user, and SSH access"
    exit 1
fi
echo ""

# Step 2: Copy test files to device
echo "[STEP 2] Copying test files to /opt/..."
scp -P $DEVICE_PORT -r "${SCRIPT_DIR}"/* ${DEVICE_USER}@${DEVICE_IP}:/opt/ 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[PASS] Files copied successfully"
else
    echo "[FAIL] Failed to copy files"
    exit 1
fi
echo ""

# Step 3: Make validateStorageMgr.sh executable
echo "[STEP 3] Setting permissions..."
ssh -p $DEVICE_PORT ${DEVICE_USER}@${DEVICE_IP} "chmod +x /opt/validateStorageMgr.sh && chmod +x /opt/StorageMgr_*.sh" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[PASS] Permissions set successfully"
else
    echo "[FAIL] Failed to set permissions"
    exit 1
fi
echo ""

# Step 4: Run tests on device
echo "[STEP 4] Running test suite on device..."
echo "=========================================="
ssh -p $DEVICE_PORT ${DEVICE_USER}@${DEVICE_IP} "bash /opt/validateStorageMgr.sh $DEVICE_IP"
TEST_EXIT_CODE=$?
echo "=========================================="
echo ""

# Step 5: Summary
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "[SUCCESS] All tests passed!"
    exit 0
else
    echo "[INFO] Some tests failed or encountered errors"
    echo "[INFO] Check the output above for details"
    exit 1
fi
