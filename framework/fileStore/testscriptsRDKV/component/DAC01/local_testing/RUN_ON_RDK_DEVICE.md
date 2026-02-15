# Running PackageManager Validation on RDK RPi Device from Windows

## Overview

The validation script can now be deployed and executed directly on RDK devices via SSH. This guide explains how to run it from Windows PowerShell.

## Prerequisites

### Windows Requirements
- **PowerShell or Command Prompt**
- **SSH Client** (built-in on Windows 10+ or install PuTTY/Git Bash)
- **Network connectivity** to RDK device

### RDK Device Requirements
- **IP Address** (e.g., 192.168.29.164)
- **SSH enabled** (usually available by default)
- **Credentials** (typically `root` user, ask for password if needed)
- **Thunder/RDK services** running

## Method 1: Using SSH with Windows PowerShell (Recommended)

### Step 1: Verify SSH is Available
```powershell
# Test SSH connectivity
ssh -V

# If not found, install using:
# - Windows 10+: Use built-in OpenSSH
# - Windows 8.1 or earlier: Install Git Bash or PuTTY
```

### Step 2: Deploy and Run Script on Device
```powershell
# From the local_testing directory
cd "D:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\DAC01\local_testing"

# Deploy to RDK device (replace IP with your device IP)
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

### Step 3: Review Results
```powershell
# Check the generated report
cat plugin_validation_report_device.txt

# Or open in notepad
notepad plugin_validation_report_device.txt
```

---

## Method 2: Manual SSH Execution

If the automated deployment doesn't work:

### Step 1: Copy Script to Device
```powershell
# Copy script via SCP
scp ".\validate_packagemanager_plugins.sh" root@192.168.29.164:/tmp/

# If prompted, enter device password
```

### Step 2: SSH into Device
```powershell
# SSH to device
ssh root@192.168.29.164

# You should now be in the device shell
```

### Step 3: Run Script on Device
```bash
# Once SSH'd into device, run:
cd /tmp
chmod +x validate_packagemanager_plugins.sh
./validate_packagemanager_plugins.sh --verbose

# Or run with custom settings
./validate_packagemanager_plugins.sh -h localhost -p 9998 --verbose
```

### Step 4: Review Report
```bash
# View report on device
cat plugin_validation_report.txt

# Or copy back to Windows
# (In PowerShell on Windows, open new window and run:)
# scp root@192.168.29.164:/tmp/plugin_validation_report.txt .
```

---

## Method 3: Using Git Bash on Windows

If PowerShell SSH doesn't work:

### Step 1: Install Git Bash
- Download from: https://git-scm.com/download/win
- Install with default options (includes SSH)

### Step 2: Open Git Bash Terminal
```bash
# Git Bash provides Unix-like environment on Windows
# You can run normal bash commands
```

### Step 3: Navigate to Script
```bash
cd /d/Project/TDK/testCodeRepo/tdk-core/framework/fileStore/testscriptsRDKV/component/DAC01/local_testing
```

### Step 4: Deploy Script
```bash
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

---

## Example Usage Scenarios

### Scenario 1: Quick Validation on Device
```powershell
# Deploy and validate in one command
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
```

### Scenario 2: Custom Port
```powershell
# If using custom JSONRPC port
ssh root@192.168.29.164 "bash -c 'cd /tmp && ./validate_packagemanager_plugins.sh -p 8998'"
```

### Scenario 3: Verbose Debug Output
```powershell
# Deploy with verbose output for troubleshooting
bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164 --verbose
```

---

## Troubleshooting

### "ssh: command not found"
- **Windows 10+**: Use built-in SSH (update system)
- **Older Windows**: Install PuTTY or Git Bash
- **Alternative**: Use PuTTY GUI instead of command line

### "Permission denied (publickey,password)"
- **Solution**: Enter device password when prompted
- **Check credentials**: Verify username (usually `root`)
- **SSH key**: If using SSH keys, ensure proper setup

### "Host unreachable"
- **Check device IP**: `ping 192.168.29.164`
- **Check device is on**: Power on RDK device
- **Check network**: Verify same network as Windows PC
- **Check firewall**: Disable Windows Firewall or allow SSH

### "SSH not available on device"
- **Enable SSH on device**: Check RDK device settings
- **Check services**: On device, verify: `systemctl status sshd`
- **Ask device admin**: May need to enable SSH access

### Script Deployment Fails
- **Manual method**: Use SCP/SSH directly (Method 2 above)
- **Path issues**: Ensure script path is correct
- **Device storage**: Check `/tmp/` has space (device should have ~100MB free)

---

## SSH Connection Details

### Connection Format
```
ssh [USERNAME]@[DEVICE_IP]
scp [FILE] [USERNAME]@[DEVICE_IP]:[PATH]
```

### Common Values
| Parameter | Example | Notes |
|-----------|---------|-------|
| USERNAME | root | Default RDK user |
| DEVICE_IP | 192.168.29.164 | Your RDK device IP |
| PATH | /tmp/ | Temporary directory |
| PORT | 22 | Default SSH port |

### Testing Connection
```powershell
# Test SSH
ssh root@192.168.29.164 "echo 'Connected!'"

# Should output: Connected!
# If fails, SSH is not working
```

---

## Script Deployment Flow

```
Windows PC
    │
    ├─ parse_arguments()
    │   └─ Check for --deploy-to-device flag
    │
    ├─ deploy_to_device()
    │   ├─ Check SSH available
    │   ├─ Test SSH connectivity
    │   ├─ Copy script via SCP
    │   ├─ Make executable via SSH
    │   └─ Execute on device
    │
    └─ RDK Device
         │
         ├─ check_dependencies()
         ├─ test_connectivity()
         ├─ check_plugin_availability()
         ├─ test_plugin_activation()
         ├─ test_basic_apis()
         ├─ generate_summary()
         │
         └─ Return results to Windows
```

---

## Output Files

After deployment, you'll have:

### On RDK Device (Automatic Cleanup)
- `/tmp/validate_packagemanager_plugins.sh` - Deleted after execution
- `/tmp/plugin_validation_report.txt` - Copied back to Windows

### On Windows PC
- `plugin_validation_report_device.txt` - Validation results from device

---

## Advanced Options

### Run with Specific Parameters
```powershell
# Custom port
ssh root@192.168.29.164 "./validate_packagemanager_plugins.sh -p 8998"

# Verbose output
ssh root@192.168.29.164 "./validate_packagemanager_plugins.sh --verbose"

# Combine options
ssh root@192.168.29.164 "./validate_packagemanager_plugins.sh -h 127.0.0.1 -p 9998 --verbose"
```

### Keep Script on Device (for repeated runs)
```bash
# Instead of automatic cleanup, keep script:
scp ./validate_packagemanager_plugins.sh root@192.168.29.164:/root/

# Later, run again:
ssh root@192.168.29.164 "/root/validate_packagemanager_plugins.sh --verbose"
```

---

## Next Steps

1. **Verify Connectivity**
   ```powershell
   ping 192.168.29.164
   ssh root@192.168.29.164 "uname -a"
   ```

2. **Deploy Script**
   ```powershell
   bash ./validate_packagemanager_plugins.sh --deploy-to-device root@192.168.29.164
   ```

3. **Review Results**
   ```powershell
   cat plugin_validation_report_device.txt
   ```

4. **Troubleshoot if Needed**
   - Check report for failures
   - Run with `--verbose` for detailed output
   - Review device logs for errors

---

## Support

For issues:
1. Verify network connectivity to device
2. Test SSH manually: `ssh root@<device-ip> "echo test"`
3. Check RDK device logs for service errors
4. Review troubleshooting section above
5. Run with `--verbose` flag for detailed output

---

**Last Updated:** 2026-01-14  
**Script Version:** 1.0 with SSH Deployment Support
