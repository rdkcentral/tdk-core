# PackageManager Plugin Validation Scripts - Index

## 📁 Location
`framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/`

## 📋 Files Created

### Core Validation Scripts

#### 1. **validate_packagemanager_plugins.sh**
- **Type:** Bash Shell Script (7.2 KB)
- **Executable:** Yes (shell script)
- **Purpose:** Remote device plugin validation via JSONRPC
- **Dependencies:** curl, bash
- **Requires Device:** Yes
- **Output:** Console + `plugin_validation_report.txt`

**Capabilities:**
- Tests device connectivity
- Validates plugin availability
- Tests plugin activation
- Verifies API functionality
- Color-coded console output
- Auto-generates validation report

**Key Commands:**
```bash
./validate_packagemanager_plugins.sh                    # Local device
./validate_packagemanager_plugins.sh -h 192.168.1.100  # Remote device
./validate_packagemanager_plugins.sh --verbose          # Debug mode
./validate_packagemanager_plugins.sh --help            # Help
```

---

#### 2. **validate_packagemanager_local.py**
- **Type:** Python 3 Script (9.1 KB)
- **Executable:** Yes (python3)
- **Purpose:** Local environment validation
- **Dependencies:** Python 3.6+ (standard library only)
- **Requires Device:** No
- **Output:** Console + `plugin_validation_report_local.json`

**Capabilities:**
- Validates configuration files (JSON)
- Checks Python dependencies
- Inspects test script structure
- Verifies API definitions
- Validates box type consistency
- Generates JSON report
- Fully offline operation

**Key Commands:**
```bash
python3 validate_packagemanager_local.py                    # All checks
python3 validate_packagemanager_local.py --check-config    # Config only
python3 validate_packagemanager_local.py --check-scripts   # Scripts only
python3 validate_packagemanager_local.py --check-deps      # Dependencies
python3 validate_packagemanager_local.py --verbose         # Debug mode
python3 validate_packagemanager_local.py --help           # Help
```

---

### Documentation Files

#### 3. **README_VALIDATION_SCRIPTS.md**
- **Type:** Markdown Documentation (8.3 KB)
- **Purpose:** Complete user guide
- **Content:**
  - Detailed script descriptions
  - Usage examples
  - Options reference
  - Output samples
  - Troubleshooting guide
  - Configuration reference
  - API method checklist
  - CI/CD integration examples

---

#### 4. **VALIDATION_SUMMARY.md**
- **Type:** Markdown Summary (5.8 KB)
- **Purpose:** High-level overview
- **Content:**
  - What's new
  - Validation workflow
  - Checks performed
  - Use cases
  - Requirements
  - Quick commands
  - Next steps

---

#### 5. **QUICKSTART.sh**
- **Type:** Bash Quick Reference (2.1 KB)
- **Purpose:** Display quick start guide
- **Usage:** `bash QUICKSTART.sh`
- **Content:**
  - Available scripts overview
  - Basic usage examples
  - Common commands
  - Documentation reference

---

## 🚀 Quick Start

### Option 1: Local Validation (No Device)
```bash
cd framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/
python3 validate_packagemanager_local.py
```

### Option 2: Device Validation (Requires Device)
```bash
cd framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/
./validate_packagemanager_plugins.sh -h <device-ip>
```

### Option 3: Show Quick Start
```bash
cd framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/
bash QUICKSTART.sh
```

---

## 📊 Validation Coverage

### Local Validation (Python)
- ✅ Configuration files (JSON syntax)
- ✅ Python environment
- ✅ Test script structure
- ✅ API definitions
- ✅ Box type consistency
- ✅ Directory structure

### Device Validation (Shell)
- ✅ Network connectivity
- ✅ Plugin presence
- ✅ Plugin activation
- ✅ API responses:
  - getList
  - getStorageDetails
  - packageState

---

## 🔧 Requirements

### Shell Script (validate_packagemanager_plugins.sh)
| Requirement | Type | Status |
|------------|------|--------|
| Bash 4.0+ | Required | Standard on Linux/Mac |
| curl | Required | Command: `curl --version` |
| jq | Optional | For JSON parsing |
| RDK Device | Required | For full validation |

### Python Script (validate_packagemanager_local.py)
| Requirement | Type | Status |
|------------|------|--------|
| Python 3.6+ | Required | Check: `python3 --version` |
| Standard library | Included | No external packages |
| Device | Not Required | Can run offline |

---

## 📈 Output Files Generated

### Local Validation Output
- **File:** `plugin_validation_report_local.json`
- **Format:** JSON
- **Contains:** Configuration, scripts, dependencies, API checks
- **Usage:** Parse with JSON tools or Python

### Device Validation Output
- **File:** `plugin_validation_report.txt`
- **Format:** Plain text
- **Contains:** Device info, plugin status, test results
- **Usage:** Human-readable log file

---

## 🔗 Relationships

```
validate_packagemanager_plugins.sh
├─ Tests: RDK Device Connectivity
├─ Tests: Plugin Availability
├─ Tests: Plugin Activation
└─ Tests: API Functionality
    ├─ getList
    ├─ getStorageDetails
    └─ packageState

validate_packagemanager_local.py
├─ Validates: ai_2_0_cpe.json
├─ Validates: ai2_0_utils.py
├─ Checks: Python environment
├─ Inspects: RDKV_PackageManager_*.py scripts
├─ Inspects: PackageMgr_DAC_*.py scripts
└─ Reports: Compatibility status

Both Scripts
├─ Independent operation
├─ No TDK framework required
├─ Color-coded output
└─ Detailed reports
```

---

## 💡 Use Cases

### 1. **Developer Setup Validation**
```bash
# Validate environment before starting work
python3 validate_packagemanager_local.py
```

### 2. **Pre-Test Checklist**
```bash
# Quick check before running full tests
python3 validate_packagemanager_local.py --check-config
./validate_packagemanager_plugins.sh -h 192.168.1.100
```

### 3. **CI/CD Pipeline Integration**
```bash
# Build stage: validate environment
python3 validate_packagemanager_local.py --check-deps

# Test stage: validate device
./validate_packagemanager_plugins.sh -h $DEVICE_IP || exit 1
```

### 4. **Troubleshooting**
```bash
# Debug with verbose output
python3 validate_packagemanager_local.py --verbose
./validate_packagemanager_plugins.sh -h 192.168.1.100 --verbose
```

---

## 📚 Documentation Map

| Document | Purpose | Audience |
|----------|---------|----------|
| README_VALIDATION_SCRIPTS.md | Complete guide | Everyone |
| VALIDATION_SUMMARY.md | Overview | Quick reference |
| QUICKSTART.sh | Fast start | New users |
| This index | File organization | Developers |

---

## ✨ Features Summary

### Shell Script Features
- 🌐 JSONRPC communication
- 🔌 Plugin detection
- ⚡ Activation testing
- 📊 API validation
- 📝 Text reports
- 🎨 Color output
- 🐛 Debug mode

### Python Script Features
- 📁 File validation
- 🐍 Dependency checking
- 🔍 Structure inspection
- 📋 API verification
- ✔️ Consistency checks
- 📊 JSON reports
- 🎨 Color output

---

## 🚀 Next Steps

1. **Read Documentation**
   ```bash
   cat README_VALIDATION_SCRIPTS.md
   ```

2. **Run Local Validation**
   ```bash
   python3 validate_packagemanager_local.py --generate-report
   ```

3. **Test on Device** (if available)
   ```bash
   ./validate_packagemanager_plugins.sh -h <device-ip>
   ```

4. **Review Reports**
   ```bash
   cat plugin_validation_report_local.json
   cat plugin_validation_report.txt
   ```

5. **Integrate with CI/CD**
   - Copy scripts to build pipeline
   - Use JSON output for automated decisions
   - Reference examples in README

---

## 📞 Support

For help:
1. Check `README_VALIDATION_SCRIPTS.md` troubleshooting section
2. Run with `--verbose` flag
3. Review generated reports
4. Check device logs if device validation fails

---

## 📝 Version Information

| Component | Version | Date | Status |
|-----------|---------|------|--------|
| Shell Script | 1.0 | 2026-01-14 | ✅ Ready |
| Python Script | 1.0 | 2026-01-14 | ✅ Ready |
| Documentation | 1.0 | 2026-01-14 | ✅ Ready |
| Overall | 1.0 | 2026-01-14 | ✅ Released |

---

**Last Updated:** 2026-01-14  
**Created in:** `framework/fileStore/testscriptsRDKV/component/DAC01/local_testing/`
