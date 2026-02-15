# PackageManager Plugin Validation Scripts

This directory contains independent validation scripts to validate PackageManager plugins both locally and on RDK devices.

## Scripts Overview

### 1. `validate_packagemanager_plugins.sh`
**Bash shell script for device-side plugin validation**

Validates PackageManager plugins on RDK devices via JSONRPC protocol.

#### Features
- Device connectivity validation
- Plugin availability checking
- Plugin activation testing
- Basic API functionality testing
- Generates validation report
- No TDK framework dependencies

#### Usage

```bash
# Basic usage (connects to localhost:9998)
./validate_packagemanager_plugins.sh

# Connect to specific device
./validate_packagemanager_plugins.sh -h 192.168.1.100

# Specify custom JSONRPC port
./validate_packagemanager_plugins.sh -h 192.168.1.100 -p 9998

# Verbose output for debugging
./validate_packagemanager_plugins.sh -h 192.168.1.100 --verbose

# Get help
./validate_packagemanager_plugins.sh --help
```

#### Options
```
-h, --host HOSTNAME/IP    Device hostname or IP (default: localhost:9998)
-p, --port PORT           JSONRPC port (default: 9998)
-d, --device-ip IP        Device IP address (default: 127.0.0.1)
--verbose                 Enable verbose output
--help                    Show help message
```

#### Output
- Console output with color-coded status indicators
- `plugin_validation_report.txt` - Detailed validation report

#### Requirements
- `curl` - For JSONRPC communication
- `jq` (optional) - For JSON parsing

#### Example Output
```
================================================
PackageManager Plugin Validator v1.0
================================================

ℹ Configuration:
ℹ   Device IP: 192.168.1.100
ℹ   JSONRPC Port: 9998
ℹ   Verbose: false

✓ curl is available
✓ Successfully connected to device

✓ Plugin org.rdk.PackageManagerRDKEMS is available
✓ Plugin activation successful

✓ getList API is functional
✓ getStorageDetails API responded
✓ packageState API responded

================================================
Validation Complete
================================================
✓ PackageManager plugin validation completed successfully!
```

---

### 2. `validate_packagemanager_local.py`
**Python script for local environment validation**

Validates local test environment without requiring device connectivity.

#### Features
- Configuration file validation (JSON parsing)
- Python dependency checking
- Test script structure validation
- API definition verification
- Box type consistency checking
- Generates JSON validation report
- No device connectivity required

#### Usage

```bash
# Run all checks
python3 validate_packagemanager_local.py

# Check configuration files only
python3 validate_packagemanager_local.py --check-config

# Check test scripts only
python3 validate_packagemanager_local.py --check-scripts

# Check Python dependencies
python3 validate_packagemanager_local.py --check-deps

# Generate detailed report
python3 validate_packagemanager_local.py --generate-report

# Verbose output
python3 validate_packagemanager_local.py --verbose

# Combine multiple checks
python3 validate_packagemanager_local.py --check-config --check-scripts --verbose
```

#### Options
```
--check-config       Validate configuration files
--check-scripts      Validate test script structure
--check-deps         Check Python dependencies
--generate-report    Generate full compatibility report
--verbose            Enable verbose output
--help               Show help message
```

#### Output
- Console output with color-coded status indicators
- `plugin_validation_report_local.json` - Detailed JSON report

#### Requirements
- Python 3.6+
- Standard library modules (no external dependencies)

#### Example Output
```
============================================================
PackageManager Plugin Local Validator v1.0
============================================================

ℹ Working directory: /path/to/local_testing
ℹ PackageManager directory: /path/to/PackageManager

============================================================
Checking Configuration Files
============================================================

✓ Found ai_2_0_cpe.json
✓ ai_2_0_cpe.json is valid JSON
✓ Found ai2_0_utils.py

============================================================
Checking Python Dependencies
============================================================

✓ Python module 'requests' available
✓ Python module 'json' available
✓ Python module 'sys' available
...

============================================================
Checking PackageManager Test Scripts
============================================================

ℹ Scanning: /path/to/PackageManager

✓ Found 55 RDKV_PackageManager_*.py scripts
✓ Found 6 PackageMgr_DAC_*.py scripts

============================================================
Validation Complete
============================================================
✓ Local validation completed successfully!
```

---

## Workflow

### Step 1: Local Validation (No Device Required)
```bash
python3 validate_packagemanager_local.py --generate-report
```
This validates:
- Configuration file integrity
- Test script structure
- Python environment
- API definitions
- Box type consistency

### Step 2: Device Validation (Device Required)
```bash
./validate_packagemanager_plugins.sh -h <device-ip> --verbose
```
This validates:
- Device connectivity
- Plugin availability
- Plugin activation
- Basic API functionality

### Step 3: Review Reports
- Check `plugin_validation_report_local.json` for local validation results
- Check `plugin_validation_report.txt` for device validation results

---

## Troubleshooting

### Local Validation Issues

**Issue: `Python module not available` warning**
- Solution: Install missing package with `pip3 install <package>`

**Issue: JSON validation fails**
- Solution: Check config file syntax with `python3 -m json.tool ai_2_0_cpe.json`

**Issue: Scripts not found**
- Solution: Ensure you're running from the correct directory
- Check `PackageManager/` directory exists

### Device Validation Issues

**Issue: Connection refused**
- Solution: Check device IP and port
- Verify device is reachable: `ping <device-ip>`
- Confirm JSONRPC service is running

**Issue: Plugin not found**
- Solution: Verify plugin is installed on device
- Check Thunder/RDK services are running
- Review device logs

**Issue: API failures**
- Solution: Ensure plugin is activated
- Check plugin version compatibility
- Review device logs for error details

---

## Integration with TDK Framework

These scripts are **independent** but complement the full TDK test suite:

| Validation | Local Script | TDK Framework |
|-----------|-------------|---------------|
| Quick checks | ✓ Fast | ✗ Slow |
| Device required | ✗ No | ✓ Yes |
| Full API testing | ✗ Basic | ✓ Complete |
| Detailed reports | ✓ JSON/Text | ✓ XML/HTML |
| CI/CD integration | ✓ Easy | ✓ Harder |

### Using with CI/CD
```bash
#!/bin/bash
# Validate environment before running tests
python3 validate_packagemanager_local.py --generate-report || exit 1

# Run TDK tests if device available
if [ ! -z "$DEVICE_IP" ]; then
    ./validate_packagemanager_plugins.sh -h $DEVICE_IP || exit 1
    python3 /path/to/tdk/tests/run_packagemanager_tests.py
fi
```

---

## Configuration Reference

### `ai_2_0_cpe.json` Structure
```json
{
  "packageManager": {
    "jsonRpcPort": 9998,
    "preferJsonRpc": true,
    "maxDownloads": 2,
    "maxInstalls": 2,
    "testData": {
      "pluginName": "org.rdk.PackageManagerRDKEMS",
      "pluginVersion": "1",
      "testAppUrl": "https://...",
      "testAppId": "test_app"
    }
  }
}
```

### Expected Box Types
All scripts should have:
```xml
<box_types>
  <box_type>RPI-Client</box_type>
  <box_type>Video_Accelerator</box_type>
</box_types>
```

---

## API Methods Validated

The validation scripts check for these PackageManager API methods:
1. download
2. install
3. uninstall
4. listPackages
5. packageState
6. getList
7. getMetadata
8. lock/unlock
9. pause/resume
10. cancel
11. getProgress
12. reset
13. setAuxMetadata/clearAuxMetadata
14. delete
15. getStorageDetails
16. getStorageInformation

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review generated validation reports
3. Run with `--verbose` flag for detailed output
4. Check device logs for server-side errors

---

## Version History

- **v1.0** (2026-01-14) - Initial release
  - Basic plugin validation
  - Configuration file checking
  - API definition verification
  - Report generation

---

Last Updated: 2026-01-14
