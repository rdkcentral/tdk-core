# PackageManager Plugin Validation Scripts - Summary

**Location:** `framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/`

## What's New

Three new validation scripts have been created to validate PackageManager plugins independently:

### 1. **validate_packagemanager_plugins.sh**
- **Type:** Bash shell script
- **Purpose:** Validate plugins on RDK devices via JSONRPC
- **Device Required:** Yes
- **Dependencies:** curl (optional: jq)
- **Output:** Console + `plugin_validation_report.txt`

**Key Features:**
- Device connectivity validation
- Plugin availability checking
- Plugin activation testing
- API functionality testing
- JSONRPC-based remote validation

**Usage:**
```bash
./validate_packagemanager_plugins.sh -h 192.168.1.100 --verbose
```

---

### 2. **validate_packagemanager_local.py**
- **Type:** Python 3 script
- **Purpose:** Validate local test environment
- **Device Required:** No
- **Dependencies:** Python 3.6+ (standard library only)
- **Output:** Console + `plugin_validation_report_local.json`

**Key Features:**
- Configuration file validation
- Python dependency checking
- Test script structure validation
- API definition verification
- Box type consistency checking
- Fully offline validation

**Usage:**
```bash
python3 validate_packagemanager_local.py --generate-report
```

---

### 3. **README_VALIDATION_SCRIPTS.md**
- **Type:** Documentation
- **Content:** Complete user guide with:
  - Detailed usage instructions
  - Configuration reference
  - Troubleshooting guide
  - CI/CD integration examples
  - API method checklist

---

### 4. **QUICKSTART.sh**
- **Type:** Quick reference script
- **Content:** Usage examples and quick start guide

---

## Validation Workflow

### Option A: Local Validation Only (Recommended for CI/CD)
```bash
# Step 1: Validate local environment
python3 validate_packagemanager_local.py --generate-report

# Step 2: Review report
cat plugin_validation_report_local.json
```

### Option B: Device Validation (Requires RDK Device)
```bash
# Step 1: Validate plugin on device
./validate_packagemanager_plugins.sh -h <device-ip> --verbose

# Step 2: Review report
cat plugin_validation_report.txt
```

### Option C: Complete Validation (All Checks)
```bash
# Step 1: Local checks
python3 validate_packagemanager_local.py --verbose

# Step 2: Device checks (if available)
./validate_packagemanager_plugins.sh -h <device-ip> --verbose

# Step 3: Review both reports
cat plugin_validation_report_local.json
cat plugin_validation_report.txt
```

---

## Checks Performed

### Local Validation (Python script)
- ✓ Configuration file integrity (JSON parsing)
- ✓ Python module availability
- ✓ Test script structure validation
- ✓ API method definitions
- ✓ Box type consistency
- ✓ System tool availability (curl, jq)

### Device Validation (Shell script)
- ✓ Device connectivity
- ✓ Plugin availability
- ✓ Plugin activation
- ✓ API method functionality:
  - getList
  - getStorageDetails
  - packageState

---

## Output Examples

### Local Validation Report (JSON)
```json
{
  "timestamp": "2026-01-14T10:30:45.123456",
  "script_location": "/path/to/local_testing",
  "results": {
    "config": [...],
    "scripts": [...],
    "dependencies": [...],
    "apis": [...]
  },
  "summary": {
    "total_config_checks": 2,
    "total_script_checks": 3,
    "total_dependency_checks": 8,
    "total_api_checks": 14
  }
}
```

### Device Validation Report (Text)
```
PackageManager Plugin Validation Report
Generated: Mon Jan 14 10:30:45 2026
Device: 192.168.1.100:9998

PLUGINS CHECKED:
- org.rdk.PackageManagerRDKEMS
- org.rdk.PackageManager

NEXT STEPS:
1. If all checks passed, PackageManager is ready for testing
2. Run individual test scripts from the PackageManager directory
3. For detailed API testing, use the TDK test framework
```

---

## Integration with TDK

These scripts are **independent** but work well with TDK:

| Feature | Validation Scripts | TDK Framework |
|---------|-------------------|---------------|
| Speed | 🟢 Fast (< 1 min) | 🔴 Slow (5-10 min) |
| Device Required | 🔴 Optional | 🟢 Required |
| Detailed Testing | 🔴 Basic | 🟢 Complete |
| Reports | 🟢 JSON/Text | 🟢 XML/HTML |
| CI/CD Ready | 🟢 Yes | 🔴 Complex |

---

## Use Cases

### 1. **Developer Environment Setup**
```bash
# Validate local setup before running tests
python3 validate_packagemanager_local.py
```

### 2. **Pre-Test Validation**
```bash
# Ensure everything is ready
python3 validate_packagemanager_local.py && \
./validate_packagemanager_plugins.sh -h $DEVICE_IP
```

### 3. **CI/CD Pipeline**
```bash
# Quick environment check in build stage
python3 validate_packagemanager_local.py --check-config --check-deps

# Device check in test stage
./validate_packagemanager_plugins.sh -h $DEVICE_IP || exit 1
```

### 4. **Troubleshooting**
```bash
# Verbose output for debugging
python3 validate_packagemanager_local.py --verbose
./validate_packagemanager_plugins.sh -h $DEVICE_IP --verbose
```

---

## Requirements

### Shell Script Requirements
- **Bash 4.0+** - Standard on most Linux/macOS systems
- **curl** - For JSONRPC communication
- **jq** (optional) - For JSON parsing

### Python Script Requirements
- **Python 3.6+** - Core language requirement
- **No external dependencies** - Uses only Python standard library

### Device Validation Requirements
- **Network connectivity** - Must reach device
- **Thunder/RDK Services** - Must be running on device
- **JSONRPC port open** - Default 9998

---

## Files Summary

| File | Size | Type | Purpose |
|------|------|------|---------|
| validate_packagemanager_plugins.sh | ~7 KB | Bash | Device validation |
| validate_packagemanager_local.py | ~9 KB | Python | Local validation |
| README_VALIDATION_SCRIPTS.md | ~8 KB | Markdown | Complete documentation |
| QUICKSTART.sh | ~2 KB | Bash | Quick reference |
| VALIDATION_SUMMARY.md | This file | Markdown | Overview |

---

## Quick Commands Reference

```bash
# Local validation
python3 validate_packagemanager_local.py

# Device validation
./validate_packagemanager_plugins.sh -h 192.168.1.100

# Get help
./validate_packagemanager_plugins.sh --help
python3 validate_packagemanager_local.py --help

# Quick start
bash QUICKSTART.sh

# Read documentation
cat README_VALIDATION_SCRIPTS.md
```

---

## Next Steps

1. **Review Scripts**
   - Read `README_VALIDATION_SCRIPTS.md` for complete documentation
   - Run `QUICKSTART.sh` for usage examples

2. **Run Local Validation**
   ```bash
   python3 validate_packagemanager_local.py --generate-report
   ```

3. **Test on Device** (if available)
   ```bash
   ./validate_packagemanager_plugins.sh -h <your-device-ip>
   ```

4. **Review Reports**
   - Check `plugin_validation_report_local.json`
   - Check `plugin_validation_report.txt`

5. **Integrate with CI/CD**
   - Use in build/test pipelines
   - Automate validation before test runs
   - Parse JSON reports for automated decisions

---

## Support & Troubleshooting

See `README_VALIDATION_SCRIPTS.md` for:
- Detailed troubleshooting guide
- Configuration reference
- API method checklist
- CI/CD integration examples

---

**Created:** 2026-01-14  
**Version:** 1.0  
**Location:** `framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/`
