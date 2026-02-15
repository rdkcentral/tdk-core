# AppManager Test Cases Documentation

## Overview

This directory contains the complete test suite for the **AppManager RDK Services API** component for RDKV (RDK Video) platforms. The suite comprises **34 comprehensive test cases** organized into 9 functional categories, covering all major AppManager APIs including application lifecycle management, system properties, data management, and more.

## Quick Start

### View Test Cases

1. **Summary Overview (Markdown)**: See [TEST_CASES_SUMMARY.md](TEST_CASES_SUMMARY.md)
   - Organized by category with descriptions
   - API coverage matrix
   - Test type distribution

2. **CSV Format**: See [test_cases.csv](test_cases.csv)
   - Easy to parse for automation
   - Can be imported into spreadsheets
   - All 34 test cases with metadata

3. **JSON Format**: See [test_cases.json](test_cases.json)
   - Structured data for programmatic access
   - Category organization
   - API method details

### Run Tests

Execute the test suite using the provided shell script:

```bash
# Run all tests
./run_appmanager_tests.sh all

# Show test coverage summary
./run_appmanager_tests.sh coverage

# Run specific test category
./run_appmanager_tests.sh category control
./run_appmanager_tests.sh category system
./run_appmanager_tests.sh category data

# Show help
./run_appmanager_tests.sh help
```

---

## Test Suite Structure

### Test Categories

| Category | Tests | APIs Covered | Purpose |
|----------|-------|-------------|---------|
| **Plugin Activation** | 1 | `activate` | Plugin initialization and activation |
| **App Control** | 10 | `launchApp`, `preloadApp`, `closeApp`, `terminateApp`, `killApp` | Launch, preload, close, and terminate applications |
| **App Query** | 4 | `isInstalled`, `getInstalledApps`, `getLoadedApps` | Check app status and enumerate applications |
| **App Communication** | 2 | `sendIntent` | Send intents/commands to apps |
| **System App Mgmt** | 4 | `startSystemApp`, `stopSystemApp` | Manage system-level applications |
| **Data Management** | 3 | `clearAppData`, `clearAllAppData` | Clear application data |
| **App Metadata** | 2 | `getAppMetadata` | Retrieve app metadata |
| **App Properties** | 4 | `getAppProperty`, `setAppProperty` | Get/set app configuration properties |
| **Resource Limits** | 4 | `getMaxRunningApps`, `getMaxHibernatedApps`, `getMaxHibernatedFlashUsage`, `getMaxInactiveRamUsage` | Query system resource limits |

### Total Coverage

- **34 Test Cases** across **21 Unique APIs**
- **16 Positive Tests** - Valid inputs, normal operation
- **12 Negative Tests** - Invalid inputs, error handling
- **6 Query/Property Tests** - System property queries

---

## Test Files Structure

### Individual Test Files

Each test file follows the naming pattern:
```
RDKV_AppManager_<Number>_<ApiName>[_<TestType>].py
```

Examples:
- `RDKV_AppManager_01_Activate.py` - Plugin activation
- `RDKV_AppManager_02_LaunchApp_Positive.py` - Launch app test (valid scenario)
- `RDKV_AppManager_03_LaunchApp_Negative.py` - Launch app test (error scenario)
- `RDKV_AppManager_31_GetMaxRunningApps.py` - Resource property query

### Metadata Format

Each test file contains XML metadata defining:
- `test_case_id`: Unique test identifier (e.g., TC_AppManager_launchApp)
- `name`: Human-readable test name
- `test_type`: Classification (Positive, Negative, Query, Property, Activation)
- `api_or_interface_used`: The specific API method (e.g., org.rdk.AppManager.1.launchApp)
- `test_objective`: What the test validates
- `expected_output`: Expected behavior/results

Example metadata:
```xml
<test_case_id>TC_AppManager_launchApp</test_case_id>
<test_objective>Test AppManager launchApp API - Positive scenarios</test_objective>
<test_type>Positive</test_type>
<api_or_interface_used>org.rdk.AppManager.1.launchApp</api_or_interface_used>
<expected_output>launchApp API should return appropriate responses for Positive scenarios</expected_output>
```

---

## Complete Test Listing

### 1. Plugin Activation (1 test)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 01 | TC_AppManager_activate | RDKV_AppManager_01_Activate | Activation | activate |

### 2. App Control (10 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 02 | TC_AppManager_launchApp | RDKV_AppManager_02_LaunchApp_Positive | Positive | launchApp |
| 03 | TC_AppManager_launchApp | RDKV_AppManager_03_LaunchApp_Negative | Negative | launchApp |
| 04 | TC_AppManager_preloadApp | RDKV_AppManager_04_PreloadApp_Positive | Positive | preloadApp |
| 05 | TC_AppManager_preloadApp | RDKV_AppManager_05_PreloadApp_Negative | Negative | preloadApp |
| 06 | TC_AppManager_closeApp | RDKV_AppManager_06_CloseApp_Positive | Positive | closeApp |
| 07 | TC_AppManager_closeApp | RDKV_AppManager_07_CloseApp_Negative | Negative | closeApp |
| 08 | TC_AppManager_terminateApp | RDKV_AppManager_08_TerminateApp_Positive | Positive | terminateApp |
| 09 | TC_AppManager_terminateApp | RDKV_AppManager_09_TerminateApp_Negative | Negative | terminateApp |
| 10 | TC_AppManager_killApp | RDKV_AppManager_10_KillApp_Positive | Positive | killApp |
| 11 | TC_AppManager_killApp | RDKV_AppManager_11_KillApp_Negative | Negative | killApp |

### 3. App Query (4 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 12 | TC_AppManager_isInstalled | RDKV_AppManager_12_IsInstalled_Positive | Positive | isInstalled |
| 13 | TC_AppManager_isInstalled | RDKV_AppManager_13_IsInstalled_Negative | Negative | isInstalled |
| 14 | TC_AppManager_getInstalledApps | RDKV_AppManager_14_GetInstalledApps | Query | getInstalledApps |
| 15 | TC_AppManager_getLoadedApps | RDKV_AppManager_15_GetLoadedApps | Query | getLoadedApps |

### 4. App Communication (2 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 16 | TC_AppManager_sendIntent | RDKV_AppManager_16_SendIntent_Positive | Positive | sendIntent |
| 17 | TC_AppManager_sendIntent | RDKV_AppManager_17_SendIntent_Negative | Negative | sendIntent |

### 5. System App Management (4 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 18 | TC_AppManager_startSystemApp | RDKV_AppManager_18_StartSystemApp_Positive | Positive | startSystemApp |
| 19 | TC_AppManager_startSystemApp | RDKV_AppManager_19_StartSystemApp_Negative | Negative | startSystemApp |
| 20 | TC_AppManager_stopSystemApp | RDKV_AppManager_20_StopSystemApp_Positive | Positive | stopSystemApp |
| 21 | TC_AppManager_stopSystemApp | RDKV_AppManager_21_StopSystemApp_Negative | Negative | stopSystemApp |

### 6. Data Management (3 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 22 | TC_AppManager_clearAppData | RDKV_AppManager_22_ClearAppData_Positive | Positive | clearAppData |
| 23 | TC_AppManager_clearAppData | RDKV_AppManager_23_ClearAppData_Negative | Negative | clearAppData |
| 24 | TC_AppManager_clearAllAppData | RDKV_AppManager_24_ClearAllAppData | Query | clearAllAppData |

### 7. App Metadata (2 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 25 | TC_AppManager_getAppMetadata | RDKV_AppManager_25_GetAppMetadata_Positive | Positive | getAppMetadata |
| 26 | TC_AppManager_getAppMetadata | RDKV_AppManager_26_GetAppMetadata_Negative | Negative | getAppMetadata |

### 8. App Properties (4 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 27 | TC_AppManager_getAppProperty | RDKV_AppManager_27_GetAppProperty_Positive | Positive | getAppProperty |
| 28 | TC_AppManager_getAppProperty | RDKV_AppManager_28_GetAppProperty_Negative | Negative | getAppProperty |
| 29 | TC_AppManager_setAppProperty | RDKV_AppManager_29_SetAppProperty_Positive | Positive | setAppProperty |
| 30 | TC_AppManager_setAppProperty | RDKV_AppManager_30_SetAppProperty_Negative | Negative | setAppProperty |

### 9. Resource Limits (4 tests)

| # | Test ID | Test Name | Type | API |
|---|---------|-----------|------|-----|
| 31 | TC_AppManager_getMaxRunningApps | RDKV_AppManager_31_GetMaxRunningApps | Property | getMaxRunningApps |
| 32 | TC_AppManager_getMaxHibernatedApps | RDKV_AppManager_32_GetMaxHibernatedApps | Property | getMaxHibernatedApps |
| 33 | TC_AppManager_getMaxHibernatedFlashUsage | RDKV_AppManager_33_GetMaxHibernatedFlashUsage | Property | getMaxHibernatedFlashUsage |
| 34 | TC_AppManager_getMaxInactiveRamUsage | RDKV_AppManager_34_GetMaxInactiveRamUsage | Property | getMaxInactiveRamUsage |

---

## API Method Reference

### Complete API Coverage

**21 Unique APIs Tested:**

1. **org.rdk.AppManager.1.activate** - Initialize AppManager plugin
2. **org.rdk.AppManager.1.launchApp** - Launch an application
3. **org.rdk.AppManager.1.preloadApp** - Preload an application for faster startup
4. **org.rdk.AppManager.1.closeApp** - Close a running application gracefully
5. **org.rdk.AppManager.1.terminateApp** - Terminate an application forcefully
6. **org.rdk.AppManager.1.killApp** - Kill an application immediately
7. **org.rdk.AppManager.1.isInstalled** - Check if an app is installed
8. **org.rdk.AppManager.1.getInstalledApps** - Get list of installed applications
9. **org.rdk.AppManager.1.getLoadedApps** - Get list of currently loaded applications
10. **org.rdk.AppManager.1.sendIntent** - Send an intent to an application
11. **org.rdk.AppManager.1.startSystemApp** - Start a system application
12. **org.rdk.AppManager.1.stopSystemApp** - Stop a system application
13. **org.rdk.AppManager.1.clearAppData** - Clear data for a specific app
14. **org.rdk.AppManager.1.clearAllAppData** - Clear data for all apps
15. **org.rdk.AppManager.1.getAppMetadata** - Get metadata for an application
16. **org.rdk.AppManager.1.getAppProperty** - Get a property value for an app
17. **org.rdk.AppManager.1.setAppProperty** - Set a property value for an app
18. **org.rdk.AppManager.1.getMaxRunningApps** - Get max concurrent running apps limit
19. **org.rdk.AppManager.1.getMaxHibernatedApps** - Get max hibernated apps limit
20. **org.rdk.AppManager.1.getMaxHibernatedFlashUsage** - Get max hibernation storage
21. **org.rdk.AppManager.1.getMaxInactiveRamUsage** - Get max inactive RAM usage

---

## Prerequisites

All tests require the following:

1. **TDK Environment**
   - TDK Agent should be up and running
   - TDK Framework properly configured
   - Valid device connection

2. **AppManager Plugin**
   - AppManager plugin should be available
   - Plugin should be activated for test execution
   - Version compatible with RDK2.0

3. **Device Configuration**
   - Supported box types: RPI-Client, Video_Accelerator
   - RDK2.0 or compatible version
   - Required applications installed on device

4. **Test Stub**
   - librdkservicesstub.so available
   - Proper library paths configured

---

## Test Validations

Each test case validates:

1. **Response Structure**
   - Proper JSON/XML formatting
   - Required fields present
   - Data type correctness

2. **Error Handling**
   - Appropriate error codes returned
   - Invalid inputs rejected
   - Error messages descriptive

3. **State Changes**
   - Applications state transitions correct
   - Properties updated as expected
   - Data cleared successfully

4. **Data Integrity**
   - Returned data accuracy
   - Completeness of lists/arrays
   - No data corruption

5. **Status Codes**
   - Success status for valid requests
   - Failure status for invalid requests
   - Appropriate error codes

---

## File Formats

### Documents Available

1. **TEST_CASES_SUMMARY.md** (10+ KB)
   - Comprehensive markdown guide
   - Organized by category
   - API reference table
   - Statistics and summaries

2. **test_cases.csv** (5+ KB)
   - All 34 test cases in CSV format
   - Easy parsing for automation
   - Importable to spreadsheets
   - Headers: Test_Number, Test_ID, Test_Name, File_Name, Test_Type, API_Method, Category, Objective, Key_Assertions

3. **test_cases.json** (15+ KB)
   - Structured JSON format
   - Category organization
   - API method details
   - Configuration metadata

4. **run_appmanager_tests.sh** (Executable)
   - Complete test execution script
   - Category-based test grouping
   - Result reporting
   - Log file generation

---

## Using Test Data in Shell Scripts

### CSV Integration Example

```bash
#!/bin/bash

# Read test cases from CSV
while IFS=',' read -r test_num test_id test_name file_name test_type api_method category objective assertions; do
    echo "Running test: $test_name (Type: $test_type)"
    # Execute test
    python3 "${TEST_DIR}/${file_name}.py"
done < test_cases.csv | tail -n +2  # Skip header
```

### JSON Integration Example

```bash
#!/bin/bash

# Parse test cases from JSON
jq '.appManagerTestSuite.testCategories | to_entries[] | .value.tests[]' test_cases.json | while read -r test; do
    test=$(echo "$test" | tr -d '"')
    echo "Running: $test"
    python3 "${TEST_DIR}/${test}.py"
done
```

---

## Execution Examples

### Run All Tests
```bash
./run_appmanager_tests.sh all
```

### Run Specific Categories
```bash
# App control tests (launch, preload, close, terminate, kill)
./run_appmanager_tests.sh category control

# System app management tests
./run_appmanager_tests.sh category system

# Data management tests
./run_appmanager_tests.sh category data

# Property tests
./run_appmanager_tests.sh category property
```

### Check Coverage
```bash
./run_appmanager_tests.sh coverage
```

### Expected Output
```
[INFO] Checking prerequisites...
[PASS] All test files present
[INFO] ===========================================
[INFO] Running Test Suite: Plugin Activation
[INFO] ===========================================
[INFO] Running test: RDKV_AppManager_01_Activate (Category: Activation)
[PASS] Test passed: RDKV_AppManager_01_Activate
...
```

---

## Test Statistics

- **Total Tests**: 34
- **Total APIs**: 21
- **Total Categories**: 9
- **Test Execution Time**: ~60 seconds per test (34 tests = ~34 minutes total)
- **Pass Rate Target**: 100%

### Distribution

| Type | Count | % |
|------|-------|---|
| Positive Tests | 16 | 47% |
| Negative Tests | 12 | 35% |
| Query/Property Tests | 6 | 18% |

---

## Troubleshooting

### Common Issues

1. **Test File Not Found**
   - Verify all `.py` files are in the correct directory
   - Check file permissions
   - Ensure no file name typos

2. **AppManager Plugin Not Active**
   - Start the device with AppManager enabled
   - Verify plugin activation via device logs
   - Check TDK Agent connectivity

3. **Test Failures**
   - Review `test_results/appmanager_test_execution.log`
   - Check `test_results/failed_tests.txt`
   - Verify device app configuration

4. **Missing Applications**
   - Ensure required test applications are installed
   - Check device storage space
   - Verify application permissions

---

## Integration with CI/CD

### Jenkins Example

```groovy
stage('AppManager Tests') {
    steps {
        sh '''
            cd framework/fileStore/testscriptsRDKV/component/AppManager/
            chmod +x run_appmanager_tests.sh
            ./run_appmanager_tests.sh all
        '''
        archiveArtifacts artifacts: 'test_results/**'
        junit 'test_results/test_summary.txt'
    }
}
```

### GitLab CI Example

```yaml
appmanager_tests:
  script:
    - cd framework/fileStore/testscriptsRDKV/component/AppManager/
    - chmod +x run_appmanager_tests.sh
    - ./run_appmanager_tests.sh all
  artifacts:
    paths:
      - test_results/
  reports:
    junit: test_results/test_summary.txt
```

---

## Documentation Files Reference

| File | Purpose | Format | Size |
|------|---------|--------|------|
| TEST_CASES_SUMMARY.md | Detailed test documentation | Markdown | 10+ KB |
| test_cases.csv | Machine-readable test list | CSV | 5+ KB |
| test_cases.json | Structured test data | JSON | 15+ KB |
| run_appmanager_tests.sh | Test execution script | Bash | 8+ KB |
| README.md | This file | Markdown | 12+ KB |

---

## Support

For questions or issues:
1. Review TEST_CASES_SUMMARY.md for detailed descriptions
2. Check test file XML metadata for specific test details
3. Review device logs for execution failures
4. Verify prerequisites are met
5. Check TDK Agent connectivity

---

## Version Information

- **Test Suite Version**: 1.0
- **Component**: AppManager
- **Platform**: RDKV (RDK Video)
- **RDK Version**: RDK2.0
- **Release Version**: M128
- **Last Updated**: February 9, 2025

---

*For the most current test information, always refer to the individual test files in this directory.*
